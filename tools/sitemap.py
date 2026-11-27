#!/usr/bin/env python3
"""Write sitemap.xml, with every lastmod taken from git rather than from memory.

Until 2026-08-29 this file was maintained by hand. It carried three dates,
2026-07-26, 2026-08-03 and 2026-08-10, for a site whose pages had been edited
on the 28th and the 29th, and it had gone stale the ordinary way: a page is
edited, the sitemap is not, and nothing anywhere notices.

WHAT LASTMOD IS ALLOWED TO MEAN

It is a claim about the page, so it has to be about the page. The naive answer,
the date of the last commit that touched the file, is wrong here in a way that
matters: a footer regeneration writes all thirty pages in one commit, and a
sitemap where everything changed today is a sitemap a crawler learns to ignore.

So this asks a narrower question. It strips the blocks that other generators
own, the footer, the top bar, the JSON-LD, the corridor rail and the asset
version query, and then walks the file's history backwards while the stripped
content still matches what is on disk. The oldest commit that still matches is
the commit where the page BECAME what it is, and its date is the lastmod.

WHICH WAY THIS ERRS, SAID OUT LOUD

Towards dates that are too new, never too old. A blob from before a marker
existed cannot have that block stripped out of it, so it compares as different
and the walk stops there. A page whose content really has not moved since July
may therefore be dated to the day its footer markers arrived. That is a claim
that the page changed more recently than it did, which costs a crawl; the
opposite error would hide a change, which costs a reader.

WHERE THE CLOCK COMES IN, AND WHY IT HAS TO

A page whose content matches no commit is one that has been edited and not
committed yet, and it takes today's date. That is the only clock in here, and
it is what lets the tool agree with itself across the commit that introduces a
change: run this, commit the page and the sitemap together, and the next run
finds that commit at the head of the history and computes the same date the
file already holds. Dating it from the newest existing commit instead would be
deterministic and would fail the gate on every single content edit, because the
commit being made is the one that has not happened yet.

So the output is stable for any committed tree, which is what CI and the gate
see, and moves with the day only while an edited page is still uncommitted.

Run from the repo root:  python3 tools/sitemap.py
"""
import datetime
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://it-rat.com"

# The blocks other generators own. A commit that changed only these did not
# change the page, and every one of them lands on all thirty pages at once.
GENERATED = [
    (r"<!-- footer:auto -->.*?<!-- /footer:auto -->", "footer"),
    (r"<!-- seo:auto -->.*?<!-- /seo:auto -->", "json-ld"),
    (r'<header class="topbar">.*?</header>', "top bar"),
    (r'<div class="foot-groups">.*?\n      </div>', "footer, home page copy"),
    (r'<div class="rail rv" id="svc-rail">.*?\n    </div>', "corridor rail"),
    (r"\?v=e\d+", "asset version"),
]
# The visible FAQ is deliberately NOT here. faq.py writes it, but what it
# writes is copy a reader reads, so a new answer is a change to the page.


def strip(text):
    for pattern, _ in GENERATED:
        text = re.sub(pattern, "", text, flags=re.S)
    return text


# Where to ask git. Normally the repository this file lives in; the freshness
# half of scripts/generated-blocks.sh copies the tracked tree to a temporary
# directory with no .git in it and points this at the real one, so the copy can
# still be dated. Both read the same file contents, so both get the same answer.
#
# It is an environment variable rather than a symlinked .git because only the
# two read-only commands below use it. A symlink would hand every future line
# of every generator a writable handle on the real repository, which is a large
# hazard to leave lying around for a small convenience.
GIT_ROOT = pathlib.Path(os.environ.get("IT_RAT_GIT_ROOT", ROOT))


def git(*args):
    r = subprocess.run(["git", "-C", str(GIT_ROOT), *args],
                       capture_output=True, text=True)
    return r.stdout


def pages():
    """Every page that asks to be indexed. Found, not listed.

    noindex is the site's own way of saying a page is not for search: the two
    redirects, the console and the 404 carry it. Reading that rather than
    keeping a list here is what stops this file from going stale the way the
    one it replaces did.
    """
    out = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("demo/"):
            continue
        # Never published: the Pages upload drops every dot path. A stray git
        # worktree under .claude/ once put 56 pages in here.
        if any(part.startswith(".") for part in p.relative_to(ROOT).parts):
            continue
        if "noindex" in p.read_text(encoding="utf-8", errors="ignore"):
            continue
        out.append(rel)
    if len(out) < 10:
        sys.exit(f"found {len(out)} indexable pages, which cannot be right. "
                 "Refusing to write a sitemap that drops the site.")
    return out


def registry(name):
    js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    block = re.search(r"const %s = \[(.*?)\n\];" % name, js, re.S)
    if not block:
        sys.exit(f"assets/site.js: no {name} registry, so the order cannot be read")
    return [m.group(1) for m in re.finditer(r'href:"([^"]+)"', block.group(1))]


def last_content_change(rel, today):
    """The date the page's own content last changed, ignoring generated blocks.

    Walks the history newest first while the stripped blob still equals what is
    on disk. The OLDEST commit that still matches is the one where the page
    became what it is, and that is the answer.

    A page whose content matches no commit at all is one edited and not yet
    committed, and it takes today's date. That is the only place a clock enters
    this, and it is what makes the sequence work: edit the page, run this, and
    commit both together. The commit is then dated today, so the next run finds
    it at the head of the history and computes the same date the file already
    holds. Without it the tool could never agree with itself across the commit
    that introduces the change, and the gate would fail on every content edit.
    """
    log = git("log", "--format=%H %cs", "--", rel).splitlines()
    here = strip((ROOT / rel).read_text(encoding="utf-8"))
    answer = today
    for line in log:
        sha, date = line.split()
        blob = git("show", f"{sha}:{rel}")
        if not blob or strip(blob) != here:
            break
        answer = date
    return answer


def main():
    # A shallow clone has one commit, so every page would look as though its
    # content arrived at HEAD and the whole file would be dated to the last
    # deploy. That is a wrong answer rather than a missing one, which is the
    # worse of the two, so it refuses. actions/checkout defaults to depth 1 and
    # the Pages workflow asks for depth 0 because of this line.
    if git("rev-parse", "--is-shallow-repository").strip() == "true":
        sys.exit("this is a shallow clone, so the history a lastmod is read from is not "
                 "here.\nRefusing to date thirty pages to the last deploy. "
                 "Fetch the full history (fetch-depth: 0).")

    today = datetime.date.today().isoformat()
    rel_pages = pages()

    # Registry order first, because that is the order the site itself puts them
    # in, then everything else alphabetically. A crawler reads none of this;
    # the order exists so a human can read the diff.
    order = ["index.html"] + registry("STACK") + registry("SIDE")
    ranked = [p for p in order if p in rel_pages]
    ranked += sorted(p for p in rel_pages if p not in ranked)
    missing = [p for p in rel_pages if p not in ranked]
    assert not missing, missing

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             "<!-- Written by tools/sitemap.py. Every lastmod is the date the page's own",
             "     content last changed, read out of git with the generated blocks masked,",
             "     so a footer sweep across all thirty pages does not date them all to",
             "     today. Edit the page, then run the tool. -->",
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel in ranked:
        loc = f"{SITE}/" if rel == "index.html" else f"{SITE}/{rel}"
        lines.append(f"  <url><loc>{loc}</loc>"
                     f"<lastmod>{last_content_change(rel, today)}</lastmod></url>")
    lines.append("</urlset>")
    text = "\n".join(lines) + "\n"

    dest = ROOT / "sitemap.xml"
    before = dest.read_text(encoding="utf-8") if dest.exists() else ""
    if before != text:
        dest.write_text(text, encoding="utf-8")
    print(f"sitemap.xml: {len(ranked)} pages, "
          f"{'written' if before != text else 'unchanged'}")


if __name__ == "__main__":
    main()

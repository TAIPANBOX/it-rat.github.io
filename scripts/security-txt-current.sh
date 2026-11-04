#!/usr/bin/env bash
#
# Fails when /.well-known/security.txt is missing, has expired, or would never
# reach the live site.
#
# WHY THIS EXISTS
#
# An expired security.txt says the contact can no longer be trusted, and nothing
# about it looks wrong until a researcher reads the date. The second fault is
# quieter: actions/upload-pages-artifact drops every path starting with a dot
# unless include-hidden-files is true, so the file can be committed, pass review
# and still answer 404 on it-rat.com. This script reads the workflow for that
# reason, not only the file.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - <<'PY'
import datetime as dt, os, sys

path = ".well-known/security.txt"
workflow = ".github/workflows/pages.yml"
canonical = "https://it-rat.com/.well-known/security.txt"

def fail(msg):
    print("FAIL: " + msg)
    sys.exit(1)

if not os.path.exists(path):
    fail(path + " is missing, so this gate measured nothing")

fields = {}
for line in open(path, encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    key, _, value = line.partition(":")
    fields.setdefault(key.strip(), value.strip())

for name in ("Contact", "Expires", "Canonical"):
    if not fields.get(name):
        fail(path + " has no " + name + " field")

if not fields["Contact"].startswith(("mailto:", "https://")):
    fail("Contact must be a mailto: or https: URI, found " + fields["Contact"])
if fields["Canonical"] != canonical:
    fail("Canonical must be " + canonical + ", found " + fields["Canonical"])

try:
    expires = dt.datetime.fromisoformat(fields["Expires"].replace("Z", "+00:00"))
except ValueError:
    fail("Expires is not a date: " + fields["Expires"])
left = (expires - dt.datetime.now(dt.timezone.utc)).days
if left < 0:
    fail("security.txt expired on " + fields["Expires"])
if left > 366:
    fail("Expires is more than a year ahead (RFC 9116 says less): " + fields["Expires"])

if "include-hidden-files: true" not in open(workflow, encoding="utf-8").read():
    fail(workflow + " does not set include-hidden-files: true, so .well-known never ships")

print("OK: security.txt is valid for %d more days and the upload keeps it." % left)
PY

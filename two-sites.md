<!-- https://it-rat.com/two-sites.html -->

# Two sites, one control plane, no VPN

> Sites reach one hub over outbound HTTPS through one narrow door: every site by name, one policy everywhere, and a quiet site never mistaken for a dead one.

A team with agents in more than one place wants one view of what they spend and one place to set what they may do, and it does not want to install and run a VPN to get it. **Here the sites reach the hub over ordinary outbound HTTPS, through one narrow door, each with a key that names it.** One script on the hub, one command per site, four variables at each site's gateway, and every site shows up by name, obeys the same policy within seconds and stays visible while it is quiet.

## One hub, a gateway at every site.

**The hub** is the cluster that runs the control plane, the policy plane and its store. **A site** is wherever agents run: another cluster, a single box, a machine in an office. Each site keeps its own gateway, so every model call is still priced, budgeted and policy-checked next to the agent that makes it, and nothing about a call waits on a round trip to the hub.

What travels to the hub is what a gateway already produces: its telemetry, and its questions to the policy plane. It travels out of the site, over HTTPS, to one public entry on the hub. Nothing at the site accepts a connection from outside, and nothing at the hub is reachable except that entry.

**The entry is deliberately narrow.** It is a small proxy with a free certificate in front of the hub's planes, and it routes exactly the eight paths a remote gateway calls. Everything else answers 404 at the edge, the console included, so the entry cannot become a second way into the parts an operator uses.

One of the eight lets a site's gateway read back what its own runs have spent, so a restart or a move to another hub does not start every run at zero. It reads only that site's runs, and after a move the site's new key must carry the same site name the old hub recorded. It was measured on release binaries behind a stand-in for the entry, not yet behind the real one on a live hub.

## Three steps.

### Open the entry on the hub

One script applies the entry, waits for the cloud to hand it an address, derives a name for that address, waits until both certificates are issued, and prints the two addresses a site needs. It is not part of the default install: a cluster that never runs it publishes nothing new.

### Give each site its own keys

One command per site mints two keys: one the control plane accepts only for pushing and reading, bound to that site's name, and one the policy plane accepts for reading decisions. It writes them to a file only the operator can read and prints no secret. Asked again for a site that already has keys, it refuses rather than minting a second pair.

### Point the site's gateway at the hub

At the site, four variables on the gateway: where the control plane is and its key, where the policy plane is and its key. That is the whole change. Calls keep flowing through the same gateway, and from then on its spend appears at the hub under the site's name and its calls are decided by the hub's policy.

## One view, one policy, and a quiet site that is not mistaken for a dead one.

**Every site by name.** The control plane lists each site with its spend, its calls and when it last reported, and labels every run with the site it came from.

**One policy, everywhere.** A rule written once at the hub applies at every site's gateway within seconds, and lifting it lifts it everywhere.

**A quiet site stays visible.** A gateway with nothing to report still sends a heartbeat every 30 seconds, so a site with no traffic and a site that has gone down no longer look the same.

**A cut link fails the way you chose.** A site that loses the hub keeps its telemetry queued and replays it when the link returns, and a kill issued at the hub stops a site's run within seconds.

## What the runs showed.

On 2026-09-26 and 2026-09-27, a hub of three virtual machines on a public cloud and a second site on a small box at home, the site reaching the hub only by outbound HTTPS:

- **From the public internet, the entry answered exactly as designed in 16 cases out of 16:** the site's calls with its key succeeded, a call with no key was refused, and the console and every other path answered 404 at the edge.

- **The entry came up with both certificates in 66 seconds** after the load balancer existed.

- **One policy written once at the hub** refused calls at both sites' gateways, and both answered again within 5 seconds of its removal.

- **With the home site cut off from the hub,** its gateway refused in 255 ms, the hub was untouched, and the site's telemetry was queued and replayed with nothing lost when the link came back.

- **A run killed through the hub** was refused at the site within 4 seconds.

- **With the site idle,** its last report at the hub aged from 34 to 286 seconds in four minutes without the heartbeat; with it, it never passed 22 seconds.

## Where this sits.

[From zero to your first alert](https://it-rat.com/first-alert.html) is the single-machine start, [what runs where and what it costs](https://it-rat.com/what-runs-where.html) covers the cluster shapes a hub runs on, and [what is proven here](https://it-rat.com/what-is-proven.html) is where each of these runs is recorded. Everything named here is Apache-2.0 and runs on infrastructure you own.

## What people ask before connecting a second site

**Q: Does a site need a VPN or an open inbound port?**
No. A site only makes outbound HTTPS calls to one public entry on the hub, the same kind of connection an agent already makes to its model provider. Nothing at the site accepts a connection from outside, so there is no tunnel to run, no firewall hole to open and no client to install on anyone's machine.

**Q: Does every model call now travel through the hub?**
No. Each site keeps its own gateway, and the call goes from that gateway straight to the provider, priced and budgeted next to the agent that made it. What reaches the hub is the gateway's telemetry and its questions to the policy plane, not the prompts and not the provider traffic.

**Q: How does the hub know which site it is talking to?**
From the key the site pushed with. Each site gets its own pair of keys, bound to its name, and the hub never takes a site's word about who it is. That also means a copied key is that site, so the key file belongs wherever the site's other secrets live.

**Q: What happens at a site when the link to the hub drops?**
What you configured. With the policy plane set to fail closed, the site's gateway refuses calls until the hub is back, which is what a governed fleet should do. Its telemetry is kept in a queue meanwhile and sent when the link returns; in our run nothing was lost.

**Q: How do I tell a quiet site from a dead one?**
By its heartbeat. A gateway with nothing to report still checks in every 30 seconds by default, so the hub shows when each site last reported whether or not it had traffic. Without the heartbeat, an idle site in our run looked nearly five minutes stale; with it, never more than 22 seconds.

**Q: What does the public entry cost?**
The software costs nothing. The entry is a load balancer, and your cloud bills it by the hour for as long as it exists, at that cloud's published rate. It is not part of the default install, so a cluster that never opens it pays nothing extra, and taking it down with the launcher's own script removes the billed part first.

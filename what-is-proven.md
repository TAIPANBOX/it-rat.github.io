<!-- https://it-rat.com/what-is-proven.html -->

# What is proven and what is not

> How to read a validation claim: what was measured on this stack, what the measurement does not cover, and the conclusions we published and had to withdraw.

Governance software is in the awkward position of asking to be trusted about trust. So this page is not a scoreboard. It is the method: what a measurement on this stack actually established, what it deliberately does not cover, and the conclusions we published and then had to take back. **The withdrawn ones are the useful part**, because a project that only records its successes is a project whose claims cannot be checked.

## A number that cannot fail is not evidence.

The single most useful habit in this project came out of a boring observation: a check that cannot produce a red result will report green forever, and nobody will notice, because green is what everyone expected.

So the rule is that a passing measurement is only worth reading next to a run where the same measurement fails. The record plane's durability sweep is the cleanest example. Eight hundred million shard ticks across four hundred thousand seeded runs, roughly twelve million injected crashes, zero durability violations. On its own that number is worth very little. The same sweep is then run again with the simulated disk allowed to lie about flushing, and **17,869 of 20,000 seeds fail**. The first number is only evidence because the second one exists.

The rule stopped being about measurements and became about the checks themselves on 2026-08-09, when a harness was put into twenty of the twenty-six repositories that plants each gate's own fault and requires the failure. **Eight gates could not produce one.** Every one had the same silhouette: a counter or a scan reading an empty subject as a clean one, so renaming a directory turned a check on eleven things into a check on nothing while the wording stayed confident. One of them held the only promise its repository makes to a stranger, that a local demo does not publish a money plane onto whatever network the laptop is on, and it was judging zero addresses.

It keeps earning its place. On 2026-08-20 the same harness was pointed at a dependency check written that morning, and reported it toothless: the check read as "every crate has its own justification" and could not hold that, because a comment covering a pair of crates is one decision and deleting a comment in the middle merely merges two groups. The claim was narrowed to what it actually holds, in the script, in the invariant and in the case. Narrowing the claim is the cheaper half of that; the expensive half is that nothing else would have said so.

The same shape applies to everything below. Where a claim has no companion failure, it says so.

## Seven claims and what each one stops short of.

Every figure here was produced by a run with a command and a date behind it, recorded in that repository's own validation file. The line under each is not a disclaimer, it is part of the claim.

### 120 processes killed mid-write, not one acknowledged record lost

Forty each on apfs, ext4 and xfs, killed with SIGKILL while writing, and every sequence number that had been reported as acknowledged survived. That is the sentence the whole design rests on, and it was tested by something other than the simulator that was written to believe it.

### About 2,450 decisions per second per pod, at a p50 of 3.2 ms

Measured on live five-node clusters on three clouds between 25 and 27 July 2026, with no throughput cliff out to 256 concurrent callers on dedicated cores, and a freeze reaching live traffic in one round trip. Every decision is audited rather than sampled, at about 426 bytes each.

### All 500 questions of a public benchmark, not a fixture we wrote

Recall was measured on LongMemEval-S in full, with every turn of every question's history ingested as its own episode, 246,738 in total, and no LLM anywhere in the loop. The per-question records are published alongside the numbers so the table can be recomputed rather than believed.

### 25,586 real Linux binaries scanned, plus a live TLS endpoint

Not a fixture directory: an actual filesystem's worth of ELF binaries, a real container image, and a live handshake against a public endpoint whose certificate was correctly flagged as quantum-vulnerable under the NCSC migration timeline.

### Proven on a five-node cluster, then attacked the same night

Every plane answered, the shared event log bound across nodes, and an agent frozen from the browser stayed frozen after the policy plane's pod was restarted. Then the same cluster was attacked, and four real holes came out: a pod that labelled itself as the console deleted a freeze using a literal development bearer while the console still displayed the agent as frozen, secrets were readable in plaintext straight out of the datastore, the kubelet API was open to the internet on every node, and the gateway never asked the policy plane anything.

### A box behind a home router governed two clouds at once, then took sixteen failures

On 2026-09-17 the single-machine installer went onto a small Debian 13 box behind carrier-grade NAT, its gateway published only on a tunnel address. Two clusters standing in for a customer's, one in AWS and one in GCP, joined the tunnel and ran their agents through the box to the real Anthropic API: seventeen calls each, then a 402 on the eighteenth, interleaved on one event log. The box told the clouds apart by key and by identity, froze one of them with a single policy while the other kept running, and ran the FinOps crew through a second door of its own until a monthly cap stopped it. Both cloud accounts were empty afterwards, by direct query, and the day cost USD 0.18.

### One cluster on three kinds of processor, then a second site with no VPN

On 2026-09-26 the cluster launcher built one cluster from AMD, Intel and Ampere machines across three zones, in 13 minutes 46 seconds from bare VMs. Every plane moved onto the two Arm nodes in 49 seconds and back onto x86 in 111, the policy database's volume following it. A rolling upgrade under a probe asking every quarter second lost 1 health check of 256, and three later rolling restarts lost none of 825. That night and the next morning, a hub of three cloud VMs took a second site at home that reached it only over outbound HTTPS: one policy written at the hub refused calls at both sites, a run killed at the hub was refused at the site within 4 seconds, and a cut link failed closed at the site in 255 ms, its telemetry replayed afterwards with nothing lost. On 2026-09-27, on a three-node cluster at home, a delegated agent revoked mid-run was refused 2.2 seconds later, the OpenAI-compatible door priced and budgeted real calls, the console's own copilot ran through the stack's gateway under a budget, and the network sensor on an x86 kernel caught an agent reaching PyPI directly.

## Sixteen ways to break it, and what each one did.

Each tile is one injected failure on the box above, with the customer's agents still calling. The colour is the outcome, not the severity: green held as designed, red found something, amber found something that was fixed on main within a day and has shipped in the single-machine release since stack-single v1.1.6.

The run froze at step seven and no plane said anything, at five seconds or at sixty. Absence was undetected; a stalled-run detector now exists.

The agent timed out, resumed afterwards under the same run, and the box saw nothing at all. Same gap, same fix.

Every call refused 403 in 0.3 s, fail-closed, one dependency event per call; the first call after the restart allowed.

Decisions continued from memory, which is right. The health check stayed 200 and a policy write hung instead of refusing; a readiness route and a 3 s deadline followed.

Egress blocked: 502 in 53 ms with an event. A retired model id: 404 with an event. A revoked key: 401 passed through and no event, by design.

Three identical tool calls among the last ten: 402 loop_detected before the provider was asked, at zero spend.

Not a loop by that definition, so the budget caught it instead. Written down so nobody files it as a bug.

The gateway kept enforcing; three calls' telemetry were dropped rather than queued and the fleet view kept the hole. A bounded replay queue followed.

Eight refusals under distinct runs inside two seconds after the hour's twentieth mail: one notice saying eight, all eight lines on the log.

Twenty-eight minutes of high and critical events with no mail and no second notice. A critical now passes the ceiling and the rest is summarised every ten minutes.

It caught up from its cursor, 52 records verified, no gap; the console's own lines refused as foreign, as designed.

The gateway came back exited and stayed down: Docker bound the port before the tunnel held the address. The installer now orders the two; the second reboot was back in 40 s.

Every volume survived. The gateway's in-memory run and unit ledgers did not (26 runs to zero, the month restarted), so a monthly cap could be spent twice. The month is now re-seeded from the control plane.

One byte flipped in a copy of a sealed pack: NOT VERIFIED. The untouched pack verified. The record does what it is for.

Accepted with no event while delegation verification was off. The record holds 32; both doors now refuse more, before anything is forwarded.

An hour forward, then NTP back: nothing changed on the tunnel or in the calls within three minutes. The clock that would matter is the box's own, not injected.

Two things the tiles do not show. The control plane's own incidents never reached the notifier or the record on the released installer, because the control plane could not create its events file and said nothing about it; the installer now creates the file for it, and the images say so at startup. And the crew's runner reported its own estimate as spent, five times under what the gateway settled, because the gateway's price book lacked the model and fell back to its ceiling rate. Both are in the repositories' validation files with their dates.

## Three things we published and had to withdraw.

Each of these was wrong in a way that a reader could have acted on, which is the only kind worth listing.

We published that throughput collapses past 64 concurrent callers and that a fleet should be designed against that limit. **It does not.** Neither dedicated-core cloud loses any throughput out to 256 concurrent on either chip generation; only latency grows. The collapse was a property of a shared-vCPU instance, which is to say it was a noisy neighbour rather than the software. The retraction is published next to the claim it replaces rather than quietly replacing it.

Our first comparison put one hyperscaler 62% ahead of the other. That gap was a chip generation wearing a cloud costume: the faster run used a newer instance family because the equivalent part on the other cloud was quota-blocked on a new account. **On matched silicon the two are 1.2% apart** and their p50 latencies differ by a hundredth of a millisecond.

We predicted that shared storage would be expensive on both hyperscalers. It is expensive on one and negligible on the other: the same 5 GiB event log is USD 1.80 a month on one and USD 194.56 on the other, because the second sells the capacity by the terabyte. The prediction was wrong in one direction and right in the other, **by a factor of 108**, and the correction is the more useful number.

There is a fourth worth naming that is not a number at all. Pointed at real object stores, one storage adapter failed three separate ways while its entire test suite was green: it sent two `Host` headers, it could not read a response from a peer that closes TLS abruptly, and it sent one cloud's headers to another cloud that refuses them. All three had the same cause. **The fakes in the tests were written from the same reading of the same documentation as the client**, so they agreed with the client's mistakes. The fix was not three fixes; it was teaching the fake to refuse what a compliant server refuses.

## What nobody has established yet.

This list is deliberately visible rather than tidy, and it is the section worth reading first if you are evaluating rather than browsing.

- **One machine has lost power, once.** Everything else about durability is established against process death. On 2026-09-23 a small box running the single-machine install had its plug pulled with two agents calling: it came back by itself, every container restarted, the record's packs from before and after the cut both verified, and no event line was torn. One cut on one box is a data point, not a claim about hardware in general.

- **No external audit of the cryptographic layer.** The primitives match their published vectors and two independent implementations of the verifier agree, which is a different and weaker claim than somebody outside this project having reviewed it.

- **Six of the nine shipped pre-production drills have never been fired at a real gateway.** They were written after the campaigns that produced the published "no gaps" result, and that result covers the three that were.

- **No years of simulated time, and no second I/O backend** to compare the first against.

- **The detectors have not been driven at production scale.** They fire correctly on seeded fleets and against real event data, which is not the same as an estate's worth of identities.

- **The federation completeness rule is specified and its transport is unbuilt.** The rule exists; the wires do not.

- **The figures on this site go stale, and did again this month.** Eleven of them name a source repository, the command that produces them and the date somebody last ran it, and a gate refuses a page that states a number nobody owns. That gate cannot tell you an owned number is still true, and on 2026-08-20 five of the eleven were not: two test counts out by six and ten, a detector count out by two, a trap count out by three, and a release a whole version behind. None was wrong when written. Re-measuring now costs one command rather than an afternoon, which is the actual fix; being more careful was never available.

Every figure quoted anywhere on this site or in these repositories is meant to carry three things: what produced it, when, and what it is a claim about. A measurement stays true about its moment and is not automatically true about the present, which is why a date is part of a number rather than decoration on it. If you find one here without those, that is a defect and worth telling us about.

## The same questions work on anybody's claims.

- **Has the check ever produced a red result?** A suite with no demonstrated failure reports the same thing whether or not it is working.

- **What is the limit stated next to the number?** If a claim arrives without one, the limit exists and somebody chose not to write it down.

- **Was the benchmark theirs or the field's?** A benchmark written by the vendor measures agreement with the vendor's assumptions.

- **Which reading of the metric is being quoted?** Most retrieval and accuracy numbers have a generous reading and a strict one, and only one of them gets printed.

- **What did the run not cover?** A cluster run that proves deployment shape is often quoted as though it proved throughput.

- **Has anything been withdrawn?** A project with no retractions has either published nothing checkable or has not checked.

- **Can somebody outside the project verify it?** Evidence you have to be trusted about is a statement, not evidence.

## Where this sits.

The numbers behind every claim here live in each repository's own validation file, next to the command that produced it. [What runs where and what it costs](https://it-rat.com/what-runs-where.html) is where most of the cluster figures come from, [one incident, end to end](https://it-rat.com/one-incident-end-to-end.html) is the behaviour they describe, and [the guides index](https://it-rat.com/guides.html) has the rest. All of it is Apache-2.0, including the write-ups that record what went wrong.

## What people ask about the evidence

**Q: What makes a validation number worth anything?**
A companion run where the same check fails. A check that cannot produce a red result reports green forever and nobody notices, because green is what everyone expected. The durability sweep is the clearest case here: zero violations across four hundred thousand seeded runs means very little on its own, and means a great deal beside the same sweep with a lying disk, where 17,869 of 20,000 seeds fail.

**Q: What has been measured on real infrastructure rather than in a simulator?**
Process-kill durability across three filesystems, policy-plane throughput on live five-node clusters on three clouds, recall on a full public benchmark rather than a fixture, a crypto scan over 25,586 real binaries and a live TLS endpoint, an adversarial pass against a running cluster that found four real holes, and, on 2026-09-17, the whole stack on a small box behind a home router governing agents in AWS and GCP at the same time through sixteen injected failures. Each has a limit published beside it, and the limit is part of the claim rather than a disclaimer under it.

**Q: What has this project got wrong and had to withdraw?**
Three published conclusions. That throughput collapses past 64 concurrent callers, which turned out to be a shared-vCPU instance rather than the software. That one hyperscaler was 62% faster, which was a chip generation rather than a cloud. And a prediction that shared storage would be expensive on both, which was wrong on one by a factor of 108. All three retractions are published next to the claims they replace. A project with no retractions has either published nothing checkable or has not checked.

**Q: What has not been established yet?**
Power has been pulled from a running machine once, on one small box, so durability is still mainly a claim about process death rather than power loss. There has been no external audit of the cryptographic layer. Six of the nine shipped pre-production drills have never been fired at a real gateway. The detectors have not been driven at production scale, and the federation completeness rule is specified with its transport unbuilt.

**Q: Why publish the things that went wrong?**
Because a repository whose history only records its successes is a repository whose claims cannot be checked. The deployment ledger for the cluster now holds 118 entries and 51 of them are our own mistakes rather than platform behaviour, and that ratio is what makes the other classifications worth believing.

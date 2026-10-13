<!-- https://it-rat.com/what-runs-where.html -->

# What runs where and what it costs

> One machine, a five-node cluster, or three clouds: the measured shapes of this stack, their throughput, and the storage line that changes by 108x.

Governance software is bought on its promises and lived with on its bill. So this page is the operational half: the four shapes this stack has been measured in, what each one did under load, and the numbers that came out of putting the same manifests on Hetzner, AWS and GCP between 25 and 27 July 2026, then the whole stack on a box behind a home router on 2026-09-17 with the agents in two clouds at once. Six clusters across three clouds, all destroyed afterwards. **Two of the findings contradicted things we had already published**, and both are below with the correction attached.

## Pick by blast radius, not by fashion.

The same binaries, the same ports, the same wiring. What changes is who can reach them and what happens when a machine dies.

*shape one*

### One machine

Compose on a box you own. The gateway publishes to loopback by default, so a machine that just ran an install script does not acquire an internet-facing enforcement plane because nobody typed anything. Opening it to the agents you actually have is one variable.

Survives a reboot, has a console behind its own tunnel, and is a real deployment rather than a demo. Most teams should start here and many should stop here.

*shape two*

### A five-node cluster

The same stack as Kubernetes manifests: plain YAML and a kustomization, applied with one `kubectl -k`, no Helm. Default-deny networking, then exactly the paths the stack needs.

It buys you node failure tolerance and costs you a shared-storage decision that a single machine hides completely. That decision is the next section.

*shape three*

### The same, on a hyperscaler

One line of Kubernetes configuration differs between the three clouds, and it is a Calico encapsulation mode: a Google VPC has no layer 2 at all, so on GCP the encapsulation becomes unconditional. On AWS the equivalent fix was one Terraform line and the Kubernetes side stayed byte for byte identical to Hetzner.

You are paying for managed everything, and the bill reflects it.

*shape four*

### A box at your premises, the agents in the clouds

The whole stack on a small machine behind your own router, carrier-grade NAT and all, with the gateway published only on a tunnel address. Nothing from the internet reaches the box; the agents come in over the tunnel, from wherever they run. Measured on 2026-09-17: the installer in 61 seconds on Debian 13 with Docker already present, direct WireGuard paths of 23 and 29 ms from AWS and GCP, both clouds refused on their eighteenth call, one cloud frozen by one policy while the other kept running.

The failure matrix below ran on this shape. Sixteen cases, and the reboot is the one to read first.

## One box at home, two clouds, and the day we tried to break it.

This is a replay, and it says so: the shapes and the numbers are the 2026-09-17 record, the timing is compressed. A small Debian box behind carrier-grade NAT holds the whole stack, its gateway on a tunnel address only. Two clusters, one in AWS and one in GCP, join the tunnel and run their agents through it to the real provider. Pick what happens.

## One storage row differs by a factor of 108.

The planes in this stack do not call each other. They append to a shared NDJSON event log, and everything downstream reads it. On one machine that coupling is invisible, because everything shares a filesystem. On Kubernetes it is the deployment's whole shape: pods on different nodes do not share a filesystem, and the default k3s storage class is single-node.

So the event directory needs a **ReadWriteMany** volume, and that is the line where the three clouds stop resembling each other. Same 5 GiB of event log, same manifests:

| shared event log, 5 GiB | what provides it | per month |
|---|---|---|
| Hetzner | Longhorn, in cluster | **EUR 0** |
| AWS | EFS, billed per GiB stored | **USD 1.80** |
| GCP | Filestore, which bills a whole TiB | **USD 194.56** |

Nothing about the software changed. One cloud sells the thing by the gigabyte you use, the other sells it by the terabyte you must buy, and a 5 GiB requirement lands in a 1 TiB minimum. It is the single largest price difference between the clouds in this whole exercise, and it appears on none of the comparison pages anybody writes, because it only shows up when you know your workload needs shared storage at all.

The point generalises past this stack: **the expensive line in a cloud bill is rarely the compute**. It is the one resource whose pricing model does not match the shape of your requirement.

Coupling planes through a file is the reason this decision exists at all, and the right fix is not a cleverer volume. It is for the event log to become a real append-only service, so the filesystem stops being an interface. That is a change to the stack rather than to its deployment, so it is named as future work rather than pretended away.

## Two hyperscalers, one machine.

The policy plane is the busiest thing in the stack, because it answers on every governed call. So it is what got benchmarked, on matched silicon: AMD EPYC Milan, 8 vCPU and 16 GiB, on all three.

|  | Hetzner CPX42 (shared cores) | AWS c6a.2xlarge | GCP c2d-highcpu-8 |
|---|---|---|---|
| peak decisions/s per pod | 2,344 | **2,449** | **2,479** |
| p50 at 8 concurrent | 3.9 ms | **3.21 ms** | **3.22 ms** |
| past 64 concurrent | collapse to 1,059 | no collapse, 2,331 at 256 | no collapse, 2,353 at 256 |
| audit bytes per decision | 393 | 427.6 | 426.4 |

### On the same silicon the two hyperscalers are the same machine

2,449 against 2,479 decisions per second is 1.2% apart, and the p50 differs by one hundredth of a millisecond. That is worth saying because our own first comparison put AWS 62% ahead, and that gap was a chip generation wearing a cloud costume: the earlier AWS run used a newer part because the equivalent GCP part was quota-blocked on a new account. Once both ran Milan, the difference disappeared. **If a benchmark makes two clouds look different, check the instance families before you believe it.**

### The number we had to withdraw

We published that throughput collapses past 64 concurrent callers and that a fleet should be designed against that cliff. It does not, and it should not. Neither dedicated-core cloud loses anything out to 256 concurrent on either chip generation; throughput holds and only latency grows. The collapse was a property of a **shared-vCPU instance**, which is to say it was a neighbour, not the software. The retraction sits next to the original claim in the source rather than replacing it quietly.

### The newest generation is the fastest measured here

For reference, the same benchmark on AWS Genoa reached 4,028 decisions per second at a p50 of 1.92 ms. It returns 64% more throughput than Milan. Anyone sizing this for cost per unit of governance should reach for the newest generation available to them, and a quota that blocks it is a price increase in disguise.

### The audit volume belongs to the software, and it is the line that grows on its own

427.6 and 426.4 bytes per decision on two different clouds from the same binary. That is the number to plan against, because every decision is audited rather than sampled: at a thousand governed calls a minute it is about 614 MB a day, and it is the only part of running this that grows without anyone deciding to grow it.

## What it cost to run, where we can show it.

The fourth shape, for comparison: the box is yours and costs nothing metered. On 2026-09-17 the two small VMs standing in for the customer's clusters ran 63 minutes each, about USD 0.11 together, and the real model calls came to USD 0.066, of which one call by the FinOps crew was USD 0.058. The whole run, with the failure matrix, was about USD 0.18, and both accounts read back empty by API before the day ended.

They verified the deployment shape and the services coming up correctly on three clouds, and they benchmarked the policy plane. They did not drive the detectors at scale, produce quality numbers, or fire pre-production drills: those planes were left deliberately unseeded, so nothing about them is claimed from these runs. Separately, the storage figures are published rates rather than invoices, so treat them as what the provider says it will charge.

## Which shape, honestly.

Start on **one machine** unless you can name the thing a cluster buys you. Node failure tolerance is a real answer; matching the rest of your estate is a real answer; "we run Kubernetes" is a habit rather than a requirement, and it costs you a shared-storage decision the single machine does not have.

If you do go to a cluster, the cheap way and the expensive way differ by roughly ten times on compute and by a hundred times on one storage line, for identical manifests. That is not an argument against hyperscalers, which are buying you things this comparison does not measure. It is an argument for knowing which of those things you are actually using.

And whichever you pick, **plan for the audit volume rather than the compute**. The compute is a decision you make once. The 426 bytes per decision accrue whether or not anybody looks.

- **Does anything need shared storage?** If yes, price that line first: it is where the clouds stop resembling each other.

- **Is the benchmark you were shown silicon-fair?** A chip generation looks exactly like a cloud advantage until somebody checks the instance family.

- **How many bytes of audit per governed action?** Multiply by your call rate before you agree to retention.

- **What does it cost per hour, not per month?** Clusters get created for an afternoon and forgotten for a week.

- **Was the shared-vCPU instance the thing you measured?** A collapse under concurrency is a neighbour until proven otherwise.

- **Can you destroy it and prove the account is empty?** If teardown is not verified, the running cost is open-ended. The 2026-09-17 run ended that way: instances, disks, addresses and volumes listed by direct API query on both clouds, all empty, before the report was written.

## Where this sits.

This is the infrastructure view. [One incident, end to end](https://it-rat.com/one-incident-end-to-end.html) is the same stack seen from a failure rather than a bill, [FinOps for AI](https://it-rat.com/finops-for-ai.html) is the discipline the money plane belongs to, and [the guides index](https://it-rat.com/guides.html) has the rest. The manifests, the Terraform and the teardown are Apache-2.0 and public, including the write-ups every number here came from.

## What people ask about running it

**Q: Do I need Kubernetes to run this?**
No, and most teams should not start there. The same binaries, ports and wiring run as containers on one machine you own, with the gateway published to loopback by default so an install does not quietly create an internet-facing enforcement plane. A cluster buys node failure tolerance and matches an estate that already runs Kubernetes. It also costs you a shared-storage decision the single machine hides completely.

**Q: Why does the shared storage line differ so much between clouds?**
Because the planes couple through a shared NDJSON event log rather than through APIs, so on Kubernetes that directory needs a ReadWriteMany volume. Nothing about the software changes. One provider sells the capacity you use and the other sells a minimum you must buy, and a 5 GiB requirement lands inside a 1 TiB block.

**Q: Is one cloud faster than the other for this?**
Not measurably. On matched silicon the policy plane reached 2,449 decisions per second on AWS and 2,479 on GCP, which is 1.2% apart, with p50 latencies of 3.21 ms and 3.22 ms. An earlier comparison of ours put AWS 62% ahead, and that was a chip generation rather than a cloud: the AWS run used a newer instance family because the equivalent GCP part was quota-blocked. If a benchmark makes two clouds look different, check the instance families first.

**Q: Does throughput really collapse past 64 concurrent callers?**
No, and we published that it did before measuring it properly. Neither dedicated-core cloud loses throughput out to 256 concurrent on either chip generation; only latency grows. The collapse was a property of a shared-vCPU instance, which is to say a noisy neighbour rather than the software. The correction is published alongside the original claim.

**Q: How much storage does the audit trail actually need?**
About 426 bytes per governed decision, measured at 427.6 and 426.4 on two different clouds from the same binary, because every decision is audited rather than sampled. At a thousand governed calls a minute that is roughly 614 MB a day. It is the line worth planning against, because it is the only one that grows without anybody deciding to grow it.

**Q: What does a cluster cost per hour rather than per month?**
About EUR 0.20 an hour on Hetzner, USD 2.16 on AWS and USD 1.91 on GCP for five nodes at 8 vCPU and 16 GB. The hourly figure is the one that matters, because clusters get created for an afternoon and forgotten: on AWS a six hour session is about USD 13 and leaving it up for a month is about USD 1,575.

**Q: Can the stack sit in my own building while the agents run in a cloud?**
Yes, and it has been measured that way. On 2026-09-17 the single-machine installer went onto a small Debian box behind a home router on carrier-grade NAT, with the gateway published only on a tunnel address; two clusters, one in AWS and one in GCP, joined the tunnel and ran their agents through the box to the real provider, 23 and 29 ms away. Nothing from the internet reaches such a box; the agents come in over the tunnel. The same day a failure matrix of sixteen cases ran on it, and the reboot found the one thing the installer now fixes for you: on a tunnel address, Docker has to start after the tunnel.

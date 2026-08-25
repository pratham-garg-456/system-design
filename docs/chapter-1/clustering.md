# Clustering

At a high level, a computer cluster is a group of two or more computers, or nodes, that run in parallel to achieve a common goal. This allows workloads consisting of a high number of individual, parallelizable tasks to be distributed among the nodes in the cluster. As a result, these tasks can leverage the combined memory and processing power of each computer to increase overall performance.

To build a computer cluster, the individual nodes should be connected to a network to enable internode communication. The software can then be used to join the nodes together and form a cluster. It may have a shared storage device and/or local storage on each node.

![cluster](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/clustering/cluster.png)

Typically, at least one node is designated as the leader node and acts as the entry point to the cluster. The leader node may be responsible for delegating incoming work to the other nodes and, if necessary, aggregating the results and returning a response to the user.

Ideally, a cluster functions as if it were a single system. A user accessing the cluster should not need to know whether the system is a cluster or an individual machine. Furthermore, a cluster should be designed to minimize latency and prevent bottlenecks in node-to-node communication.

## Types

Computer clusters can generally be categorized into three types:

- Highly available or fail-over
- Load balancing
- High-performance computing

!!! note "What each type is actually for"
    **Highly available / fail-over**: the goal isn't more capacity, it's not going down. Picture a bank's critical transaction database, you run a standby node that mirrors the primary and does nothing productive most of the time, its entire job is to be ready to take over the moment the primary fails.

    **Load balancing**: the goal is capacity/throughput. Multiple nodes actively share the workload simultaneously, this overlaps with plain load balancing, except these nodes are cluster-aware (they might coordinate directly or share state) rather than just blindly taking orders from a load balancer.

    **High-performance computing (HPC)**: a different shape of problem entirely, not "serve many independent requests" but "split ONE massive computation into pieces and solve it in parallel." Example: training a large ML model splits one giant computation across hundreds of GPUs that constantly exchange intermediate results (e.g. via NVIDIA's NCCL or MPI). Another example: animation studios like Pixar split a single movie's frame rendering across thousands of machines.

## Configurations

The two most commonly used high availability (HA) clustering configurations are active-active and active-passive.

### Active-Active

![active-active](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/clustering/active-active.png)

An active-active cluster is typically made up of at least two nodes, both actively running the same kind of service simultaneously. The main purpose of an active-active cluster is to achieve load balancing. A load balancer distributes workloads across all nodes to prevent any single node from getting overloaded. Because there are more nodes available to serve, there will also be an improvement in throughput and response times.

### Active-Passive

![active-passive](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/clustering/active-passive.png)

Like the active-active cluster configuration, an active-passive cluster also consists of at least two nodes. However, as the name _active-passive_ implies, not all nodes are going to be active. For example, in the case of two nodes, if the first node is already active, then the second node must be passive or on standby.

!!! note "Active-Active vs Active-Passive, the quick way to tell them apart"
    **Active-Passive** wastes capacity for the sake of safety, the standby node does nothing until something breaks, this is the failover pattern also used for redundant load balancers.

    **Active-Active** wastes nothing, all nodes serve traffic all the time, e.g. a 3-node Elasticsearch cluster where all 3 nodes are actively answering search queries right now, not one primary with two idle backups. But it's harder to build correctly, since multiple nodes might try to modify the same data at once, requiring a real coordination mechanism (like the Redis Cluster gossip protocol) to stay consistent.

## Advantages

Four key advantages of cluster computing are as follows:

- High availability
- Scalability
- Performance
- Cost-effective

## Load balancing vs Clustering

Load balancing shares some common traits with clustering, but they are different processes. Clustering provides redundancy and boosts capacity and availability. Servers in a cluster are aware of each other and work together toward a common purpose. But with load balancing, servers are not aware of each other. Instead, they react to the requests they receive from the load balancer.

We can employ load balancing in conjunction with clustering, but it also is applicable in cases involving independent servers that share a common purpose such as to run a website, business application, web service, or some other IT resource.

!!! note "The one-line distinction"
    Load balancing routes traffic to independent servers that don't know about each other, they just receive whatever the load balancer hands them and respond. Clustering makes a group of servers that DO know about each other and coordinate to act as a single logical system. Example: a Redis Cluster's nodes actively communicate over a gossip protocol to agree on which node owns which slice of data, and if you write a key that belongs to another node's slice, the node you contacted redirects you there, because it knows the cluster topology, not because a load balancer told it. Load balancing is often used in front of a cluster, they're complementary, not competing ideas.

## Leader Election

Once you have multiple cluster nodes that need to coordinate, a question comes up naturally: who's in charge? Someone has to make authoritative decisions, like which node owns this data, who writes go to, who decides a dead node should be replaced, and every node deciding independently would just cause disagreement.

Cluster nodes run an algorithm to automatically agree on a single **leader** (sometimes called primary or master), without a human manually assigning the role. If the leader dies, the remaining nodes detect this via a heartbeat and automatically elect a new leader among themselves, with no manual intervention.

!!! note "How this looks in practice"
    A **MongoDB replica set**: say 3 nodes, 1 primary and 2 secondaries. All writes go to the primary, same shape as database load balancing, one authoritative node for writes. The secondaries constantly replicate from the primary and send heartbeats to each other. If the primary crashes, the secondaries notice within seconds, hold an election (nodes vote, the one with the most up-to-date data typically wins), and one is automatically promoted to primary. The application reconnects to whichever node is now primary, no human touches anything.

    **Kubernetes** uses leader election among its own control-plane components too. Running multiple `kube-scheduler` instances for redundancy, only one is actually active (the leader) at a time, the others are ready to take over instantly if it dies. This is often implemented with **Raft**, a consensus algorithm designed to let a group of nodes agree on one leader even when some are slow or unreachable, also used by etcd, the database Kubernetes stores all its state in.

    Why this matters: it's what makes active-passive failover automatic instead of requiring a human to notice an outage at 3am and manually flip a switch. Load balancer failover, database primary/replica promotion, and general cluster coordination are all, underneath, applications of this same leader election idea.

## Challenges

The most obvious challenge clustering presents is the increased complexity of installation and maintenance. An operating system, the application, and its dependencies must each be installed and updated on every node.

This becomes even more complicated if the nodes in the cluster are not homogeneous. Resource utilization for each node must also be closely monitored, and logs should be aggregated to ensure that the software is behaving correctly.

Additionally, storage becomes more difficult to manage, a shared storage device must prevent nodes from overwriting one another and distributed data stores have to be kept in sync.

## Examples

Clustering is commonly used in the industry, and often many technologies offer some sort of clustering mode. For example:

- Containers (e.g. [Kubernetes](https://kubernetes.io), [Amazon ECS](https://aws.amazon.com/ecs))
- Databases (e.g. [Cassandra](https://cassandra.apache.org/_/index.html), [MongoDB](https://www.mongodb.com))
- Cache (e.g. [Redis](https://redis.io/docs/manual/scaling))

## Practice Questions

Test yourself. Click a question to reveal the answer.

??? question "1. What's the actual difference between clustering and just putting servers behind a load balancer?"
    With load balancing, the servers don't know about each other, they just receive whatever request the load balancer hands them. With clustering, the nodes ARE aware of each other, communicate directly, and coordinate to act as one logical system, e.g. agreeing on which node owns which slice of data. Load balancing is often used in front of a cluster, they're complementary.

??? question "2. Why does an HA/failover cluster's standby node do nothing most of the time, isn't that wasteful?"
    Yes, deliberately so, it's trading capacity for safety. Its only job is to be ready to take over instantly if the active node fails, so the tradeoff is worth it when the goal is avoiding downtime rather than maximizing throughput.

??? question "3. Why is an HPC cluster a fundamentally different problem from a load balancing cluster?"
    A load balancing cluster serves many independent requests, any node can handle any request on its own. An HPC cluster splits ONE massive computation into pieces that must be solved in parallel and constantly exchange intermediate results with each other, like training a single ML model across hundreds of GPUs.

??? question "4. In Active-Active vs Active-Passive, which is harder to build correctly and why?"
    Active-Active, because all nodes serve traffic simultaneously, so multiple nodes might try to modify the same data at the same time, requiring a real coordination mechanism to stay consistent. Active-Passive avoids this entirely since only one node is ever actually active at a time.

??? question "5. In a 3-node MongoDB replica set, what happens automatically if the primary crashes?"
    The secondaries detect the failure via heartbeat, hold an election among themselves (the node with the most up-to-date data typically wins), and one secondary is automatically promoted to primary, no human intervention needed.

??? question "6. What problem does leader election actually solve, and what's an example algorithm used to do it?"
    It lets a group of cluster nodes automatically agree on a single node to make authoritative decisions (e.g. who writes go to), and automatically re-elect a new leader if the current one dies, without a human manually intervening. Raft is a common consensus algorithm used for this, e.g. by etcd, the database Kubernetes stores its state in.

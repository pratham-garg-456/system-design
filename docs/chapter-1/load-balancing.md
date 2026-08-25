# Load Balancing

Load balancing lets us distribute incoming network traffic across multiple resources ensuring high availability and reliability by sending requests only to resources that are online. This provides the flexibility to add or subtract resources as demand dictates.

![load-balancing](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/load-balancing/load-balancer.png)

For additional scalability and redundancy, we can try to load balance at each layer of our system:

![load-balancing-layers](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/load-balancing/load-balancer-layers.png)

## But why?

Modern high-traffic websites must serve hundreds of thousands, if not millions, of concurrent requests from users or clients. To cost-effectively scale to meet these high volumes, modern computing best practice generally requires adding more servers.

A load balancer can sit in front of the servers and route client requests across all servers capable of fulfilling those requests in a manner that maximizes speed and capacity utilization. This ensures that no single server is overworked, which could degrade performance. If a single server goes down, the load balancer redirects traffic to the remaining online servers. When a new server is added to the server group, the load balancer automatically starts sending requests to it.

!!! note "In simple terms"
    Say you're running Instagram with just one server handling every request. That works for 100 users, but at real scale one machine physically can't handle the number of simultaneous connections, it'll run out of CPU, memory, or bandwidth. So instead you run the same backend code on many servers (say 50) and put a load balancer in front of them. Your phone's request never goes directly to a specific server, it goes to the load balancer, which picks one of the 50. This gets you **capacity** (50 servers handle far more users than 1) and **resilience** (if one server crashes, the load balancer just stops sending it traffic, and you never notice). A load balancer is really just a traffic cop sitting in front of a group of identical servers, deciding which one gets each incoming request.

## Workload distribution

This is the core functionality provided by a load balancer and has several common variations:

- **Host-based**: Distributes requests based on the requested hostname.
- **Path-based**: Using the entire URL to distribute requests as opposed to just the hostname.
- **Content-based**: Inspects the message content of a request. This allows distribution based on content such as the value of a parameter.

## Layers

Generally speaking, load balancers operate at one of the two levels:

### Network layer

This is the load balancer that works at the network's transport layer, also known as layer 4. This performs routing based on networking information such as IP addresses and is not able to perform content-based routing. These are often dedicated hardware devices that can operate at high speed.

A layer 4 load balancer only looks at the TCP/IP packet headers, source IP, destination IP, port. It does not open the packet and read the HTTP request inside, it just sees "a connection came in on port 443, forward these packets to Server 12," and every packet in that same connection goes to that same server from then on. It's fast precisely because it isn't inspecting content, like a mail sorter that only reads the zip code on the envelope and never opens the letter.

### Application layer

This is the load balancer that operates at the application layer, also known as layer 7. Load balancers can read requests in their entirety and perform content-based routing. This allows the management of load based on a full understanding of traffic.

A layer 7 load balancer terminates the connection itself, actually reads the HTTP request, the URL path, headers, cookies, even the body, and then decides where to forward it. That's what lets it do path-based routing (`/api/checkout` to payment servers, `/api/feed` to feed servers), route based on a session cookie, or terminate SSL/TLS once at the load balancer instead of making every backend server do it.

!!! note "AWS example"
    AWS actually sells these as two separate products. A **Network Load Balancer (NLB)** operates at layer 4, extremely fast, used when you just need raw throughput with no content-aware routing, e.g. a raw-TCP game server. An **Application Load Balancer (ALB)** operates at layer 7, used for a typical web app since you usually do want path-based or host-based routing. The tradeoff in one line: layer 4 is faster but dumber (can't see the request), layer 7 is slower but smarter (can route based on what the request actually contains).

## Types

Let's look at different types of load balancers:

### Software

Software load balancers usually are easier to deploy than hardware versions. They also tend to be more cost-effective and flexible, and they are used in conjunction with software development environments. The software approach gives us the flexibility of configuring the load balancer to our environment's specific needs. The boost in flexibility may come at the cost of having to do more work to set up the load balancer. Compared to hardware versions, which offer more of a closed-box approach, software balancers give us more freedom to make changes and upgrades.

Software load balancers are widely used and are available either as installable solutions that require configuration and management or as a managed cloud service.

### Hardware

As the name implies, a hardware load balancer relies on physical, on-premises hardware to distribute application and network traffic. These devices can handle a large volume of traffic but often carry a hefty price tag and are fairly limited in terms of flexibility.

Hardware load balancers include proprietary firmware that requires maintenance and updates as new versions, and security patches are released.

### DNS

DNS load balancing is the practice of configuring a domain in the Domain Name System (DNS) such that client requests to the domain are distributed across a group of server machines.

Unfortunately, DNS load balancing has inherent problems limiting its reliability and efficiency. Most significantly, DNS does not check for server and network outages, or errors. It always returns the same set of IP addresses for a domain even if servers are down or inaccessible.

!!! note "Why this actually bites"
    DNS has no idea if a server is alive, it just serves whatever records are configured. If a server goes fully down, DNS still hands out its IP to some fraction of users. Worse, DNS responses get cached (by routers, ISPs, OS) for a while based on the record's TTL, so even after you fix the record, some users keep hitting the dead server until their cache expires. This is why production systems don't rely on DNS alone, they use it to point to a small number of dedicated load balancers, which then do the actual health-aware routing to application servers.

## Global Server Load Balancing (GSLB)

Everything covered so far assumes one location, a load balancer picking among servers in the same data center. But what if the servers themselves are spread across multiple regions, e.g. one data center in Virginia (US) and one in Frankfurt (EU)? A regular load balancer can't help here, it only knows about the servers behind it in its own data center.

This is solved one level up, usually via **GeoDNS**: instead of a domain resolving to a fixed set of IPs, DNS looks at where the request is coming from (the client's IP address) and returns a different answer depending on location. A user in Germany querying `myapp.com` gets back the IP of the Frankfurt load balancer, a user in California gets the IP of a US-West load balancer. From there, the regular layer 4/7 load balancer we already covered takes over within that region.

!!! note "Why this matters: latency and disaster recovery"
    **Latency**: Netflix runs infrastructure in multiple AWS regions worldwide. Opening Netflix in India doesn't route every request all the way to a US data center, DNS-level geo-routing sends you to servers physically closer to you. Speed of light is a hard limit, so a round trip to a nearby region is meaningfully faster than one to a distant continent, noticeable for anything like video streaming or chat.

    **Disaster recovery**: if an entire region goes down, geo load balancing can detect the region failing its health checks and redirect all its traffic to a healthy region instead, so one region's outage doesn't take down the whole service globally. It's the same active-passive failover idea covered earlier, just applied at the scale of entire data centers instead of individual servers.

    Note this is routing by the user's physical/network location, a different problem from layer 7 content-based routing (by URL path), the two are often combined: geo-route to the nearest region first, then path-route within that region.

## Database Load Balancing

Everything so far assumes identical, interchangeable servers, which is why simple strategies like round robin or least connections work: any server can handle any request equally well. A database breaks that assumption, it holds state (the actual data), so you can't just spin up an empty copy and expect it to serve correct results.

The standard approach is **read replicas**. One **primary** (or "master") database handles all writes (`INSERT`/`UPDATE`/`DELETE`), and one or more **replica** databases continuously copy data from the primary (**replication**) and only handle reads (`SELECT`). A load balancer sits in front of the replica pool specifically, app servers send all writes to the single primary, but spread reads across the replicas using something like round robin.

!!! note "Read/write splitting and replication lag"
    Think of a social app like Twitter/X: reads massively outnumber writes, for every tweet posted, thousands of people scroll past it. You might run 1 primary and 10 read replicas, with a read/write splitting proxy (e.g. **ProxySQL** for MySQL, or a managed reader endpoint like **AWS RDS**'s) automatically sending writes to the primary and spreading reads across the 10 replicas.

    The catch: replication isn't instant, there's a small delay (**replication lag**) between a write landing on the primary and showing up on a replica. If a user posts a tweet and the app immediately reads it back from a replica that hasn't caught up yet, they might briefly not see their own tweet. This is a concrete example of **eventual consistency**, a tradeoff accepted in exchange for scaling reads horizontally. This only helps the read side, writes still have to go to one authoritative primary, which is itself a scaling bottleneck (the problem sharding solves).

## Routing Algorithms

Now, let's discuss commonly used routing algorithms. Think of it like a host seating people at a restaurant with several identical waiters, the host needs a rule for who takes the next table:

- **Round-robin**: Requests are distributed to application servers in rotation.
- **Weighted Round-robin**: Builds on the simple Round-robin technique to account for differing server characteristics such as compute and traffic handling capacity using weights that can be assigned via DNS records by the administrator.
- **Least Connections**: A new request is sent to the server with the fewest current connections to clients. The relative computing capacity of each server is factored into determining which one has the least connections.
- **Least Response Time**: Sends requests to the server selected by a formula that combines the fastest response time and fewest active connections.
- **Least Bandwidth**: This method measures traffic in megabits per second (Mbps), sending client requests to the server with the least Mbps of traffic.
- **Hashing**: Distributes requests based on a key we define, such as the client IP address or the request URL.

!!! note "Round Robin vs Least Connections vs Hashing"
    **Round Robin / Weighted Round Robin** are "blind" rotation, they don't look at real-time server load at all. Nginx uses plain round robin by default when configured with a list of backend servers; weighted round robin is what you'd use if you added newer, more powerful machines alongside older ones and want them to take a bigger share.

    **Least Connections** does look at real-time load, but it counts *connections*, not actual resource usage, which can be misleading. Picture a video streaming service: Server A has 1 connection open (someone streaming a 2-hour movie, sustained high bandwidth), Server B has 20 connections open (people quickly browsing a catalog page, each finishing in under a second). Pure Least Connections sees "1 < 20" and keeps sending new requests to Server A, even though it may be more loaded in real terms. **Least Response Time** fixes this by also factoring in how fast the server has actually been responding, and **Weighted Least Connections** fixes it by telling the load balancer up front that some servers or connection types are more expensive.

    **Hashing** isn't about load at all, it's about consistency: the same client always lands on the same server. This matters for **sticky sessions**, when a server stores session state in memory rather than a shared database, hashing the client's IP means the same user keeps landing back on the server that remembers e.g. their shopping cart.

## Advantages

Load balancing also plays a key role in preventing downtime, other advantages of load balancing include the following:

- Scalability
- Redundancy
- Flexibility
- Efficiency

## Redundant load balancers

As you must've already guessed, the load balancer itself can be a single point of failure. To overcome this, a second or `N` number of load balancers can be used in a cluster mode.

And, if there's a failure detection and the _active_ load balancer fails, another _passive_ load balancer can take over which will make our system more fault-tolerant.

![redundant-load-balancing](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/load-balancing/redundant-load-balancer.png)

!!! note "How failover actually works"
    The active load balancer handles all traffic normally, the passive one sits idle, constantly health-checking the active one via a heartbeat. If the active one stops responding, the passive one takes over, usually by claiming the same virtual IP address that DNS already points to, so from the client's perspective nothing changed, they were always talking to "the load balancer's IP," and now a different physical machine answers to it. Cloud load balancers like AWS's Application Load Balancer are actually run as a distributed, self-healing fleet across multiple availability zones under the hood, so there's no single machine whose death takes down your load balancing layer. If you run your own (e.g. HAProxy on your own VMs), you'd typically use something like `keepalived` to manage that active-passive failover yourself.

## Features

Here are some commonly desired features of load balancers:

- **Autoscaling**: Starting up and shutting down resources in response to demand conditions.
- **Sticky sessions**: The ability to assign the same user or device to the same resource in order to maintain the session state on the resource.
- **Healthchecks**: The ability to determine if a resource is down or performing poorly in order to remove the resource from the load balancing pool.
- **Persistence connections**: Allowing a server to open a persistent connection with a client such as a WebSocket.
- **Encryption**: Handling encrypted connections such as TLS and SSL.
- **Certificates**: Presenting certificates to a client and authentication of client certificates.
- **Compression**: Compression of responses.
- **Caching**: An application-layer load balancer may offer the ability to cache responses.
- **Logging**: Logging of request and response metadata can serve as an important audit trail or source for analytics data.
- **Request tracing**: Assigning each request a unique id for the purposes of logging, monitoring, and troubleshooting.
- **Redirects**: The ability to redirect an incoming request based on factors such as the requested path.
- **Fixed response**: Returning a static response for a request such as an error message.

!!! note "How health checks actually work"
    The load balancer periodically sends a small request to each backend server, e.g. every 5-10 seconds. The simplest kind just checks "can I open a TCP connection to this server?" A more thorough kind is an HTTP health check: it hits an endpoint like `GET /health` and expects a `200 OK` within some timeout. If a server fails a few checks in a row (not just one, a single blip could be a fluke), it's marked **unhealthy** and stops receiving new requests, it keeps getting checked in the background and rejoins the rotation automatically once it responds correctly again.

    A subtlety: a server can be "up" (passes a basic TCP check) but still functionally broken, e.g. its database connection is down, so every request it serves fails. A proper `/health` endpoint usually checks the app's actual dependencies internally and only returns `200` if everything it relies on is genuinely working, not just "the process is running." This is exactly the capability DNS load balancing lacks, DNS just hands out whatever IP is configured, dead or alive, while a real load balancer with health checks actively routes around failures.

!!! note "How autoscaling ties in"
    Autoscaling means the number of servers behind the load balancer isn't fixed, it grows and shrinks automatically based on real demand. You define a group of identical servers (AWS calls this an Auto Scaling Group) with a rule like "if average CPU crosses 70%, launch a new server." When that happens, the new server boots from a saved image and, critically, gets **registered with the load balancer**, which immediately starts including it in the rotation. When traffic drops, a server is **deregistered from the load balancer before it's terminated**, so in-flight requests aren't dropped onto a server about to disappear.

    Example: Instagram during the Super Bowl might see 5x normal traffic for a couple of hours. Instead of running enough servers for that rare peak year-round, you run a smaller baseline (say 50) and autoscaling grows the fleet to 250 for those hours, then shrinks back down. The load balancer itself doesn't change, it's still the same entry point, only the size of the pool behind it changes. Health checks remove unhealthy servers from an otherwise fixed-size pool; autoscaling changes the size of the pool itself.

## Examples

Following are some of the load balancing solutions commonly used in the industry:

- [Amazon Elastic Load Balancing](https://aws.amazon.com/elasticloadbalancing)
- [Azure Load Balancing](https://azure.microsoft.com/en-in/services/load-balancer)
- [GCP Load Balancing](https://cloud.google.com/load-balancing)
- [DigitalOcean Load Balancer](https://www.digitalocean.com/products/load-balancer)
- [Nginx](https://www.nginx.com)
- [HAProxy](http://www.haproxy.org)

## Practice Questions

Test yourself. Click a question to reveal the answer.

??? question "1. Why can't you just keep making one server bigger instead of using a load balancer?"
    Making one server bigger (vertical scaling) has a physical ceiling, there's a limit to how much CPU/memory one machine can have. Running the same backend on many servers behind a load balancer (horizontal scaling) gives you both more capacity and resilience, since a load balancer can route around a single crashed server.

??? question "2. What's the actual difference between Round Robin and Weighted Round Robin?"
    Round Robin cycles through servers in a fixed rotation regardless of their capacity. Weighted Round Robin gives some servers more turns than others based on an assigned weight, useful when the server fleet isn't uniform, e.g. some machines are more powerful than others.

??? question "3. A server has only 1 connection open while another has 20. Does Least Connections always send the next request to the first server, and is that always the right call?"
    It does send the next request there, since 1 < 20, but it's not always the right call. Least Connections counts connections, not actual load. If that 1 connection is a long-lived, high-bandwidth stream (e.g. video streaming) and the 20 are quick, cheap requests that finish in under a second, the first server may actually be more loaded in real terms. Least Response Time or Weighted Least Connections account for this by factoring in real response time or assigned weights, not just raw connection count.

??? question "4. What problem does IP hashing solve that Round Robin and Least Connections don't?"
    Consistency. Hashing isn't about balancing load, it's about making sure the same client always lands on the same server (sticky sessions), which matters when a server stores session state, like a shopping cart, in memory rather than a shared database.

??? question "5. Why can a layer 4 load balancer not do path-based routing, but a layer 7 one can?"
    A layer 4 load balancer only reads TCP/IP packet headers (source/destination IP, port), it never opens the packet to read the HTTP request inside. A layer 7 load balancer terminates the connection and actually reads the request, URL path, headers, cookies, so it can make decisions based on what's actually being requested.

??? question "6. Why doesn't DNS load balancing alone protect you if a server goes down?"
    DNS has no way to health-check servers, it just serves whatever IP records are configured, dead server or not. DNS responses are also cached by routers/ISPs/OS for the record's TTL duration, so even after fixing the record, some users keep hitting the dead server until their cache expires.

??? question "7. If the load balancer itself is a single point of failure, how do you avoid downtime when it dies?"
    Run two (or more) load balancers in an active-passive pair. The passive one constantly health-checks the active one, and if the active one fails, the passive one takes over by claiming the same virtual IP address the DNS record points to, so clients notice nothing. Managed cloud load balancers (like AWS's ALB) handle this redundancy for you automatically across multiple availability zones.

??? question "8. Why might a health check need to do more than just open a TCP connection to the server?"
    A server can be "up" (accepts a TCP connection) but still functionally broken, e.g. its database connection is down, so every request it serves fails. An HTTP health check that hits an endpoint like `/health` and checks the app's actual dependencies catches this, a plain TCP check doesn't.

??? question "9. In autoscaling, why does a server need to be deregistered from the load balancer *before* it's terminated, not after?"
    If it were terminated first, the load balancer could still be routing in-flight or new requests to a server that no longer exists, causing failed requests. Deregistering first drains it out of the rotation cleanly so no request gets dropped onto a server that's about to disappear.

??? question "10. Why can't a regular (single data center) load balancer route a user in Germany to a Frankfurt server and a user in California to a US-West server?"
    A regular load balancer only knows about the servers behind it in its own data center, it has no concept of other regions. Routing across regions happens one level up, usually via GeoDNS, which looks at the client's location and returns a different IP (pointing to a different region's load balancer) depending on where the request came from.

??? question "11. Why can't you load balance database writes the same way you load balance reads, by just spreading them across replicas?"
    Read replicas are copies of the primary's data, kept in sync through replication, which isn't instant. If writes went to multiple replicas independently, they'd diverge, there'd be no single source of truth. So writes must go to one authoritative primary, reads (which don't change data) can safely be spread across replicas, accepting a small replication lag as the tradeoff.

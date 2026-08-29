# Caching

_"There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton_

![caching](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/caching/caching.png)

A cache's primary purpose is to increase data retrieval performance by reducing the need to access the underlying slower storage layer. Trading off capacity for speed, a cache typically stores a subset of data transiently, in contrast to databases whose data is usually complete and durable.

Caches take advantage of the locality of reference principle _"recently requested data is likely to be requested again"._

!!! note "In simple terms"
    Think about a site like Reddit. Does the server really run a fresh database query every single time someone loads the front page? If it did, the database would get hammered, thousands of nearly-identical queries per second all asking for basically the same data, since the front page doesn't change every millisecond. A cache solves this by keeping a copy of that answer in fast memory (RAM) close to where it's needed, so the next 10,000 people get served the stored copy instantly instead of the server re-running the expensive query every time. The tradeoff, in one line: you're trading capacity for speed, a cache is small and can't hold everything like a database can, it only holds a subset, usually whatever is "hot" right now. When you open Instagram and your feed loads almost instantly, a lot of that speed comes from cached data, recently computed feed rankings, profile pictures, follower counts, served from something like Redis rather than the app re-querying the database and recomputing your feed from scratch every time.

## Caching and Memory

Like a computer's memory, a cache is a compact, fast-performing memory that stores data in a hierarchy of levels, starting at level one, and progressing from there sequentially. They are labeled as L1, L2, L3, and so on. A cache also gets written if requested, such as when there has been an update and new content needs to be saved to the cache, replacing the older content that was saved.

No matter whether the cache is read or written, it's done one block at a time. Each block also has a tag that includes the location where the data was stored in the cache. When data is requested from the cache, a search occurs through the tags to find the specific content that's needed in level one (L1) of the memory. If the correct data isn't found, more searches are conducted in L2.

If the data isn't found there, searches are continued in L3, then L4, and so on until it has been found, then, it's read and loaded. If the data isn't found in the cache at all, then it's written into it for quick retrieval the next time.

## Cache hit and Cache miss

### Cache hit

A cache hit describes the situation where content is successfully served from the cache. The tags are searched in the memory rapidly, and when the data is found and read, it's considered a cache hit.

**Cold, Warm, and Hot Caches**

A cache hit can also be described as cold, warm, or hot. In each of these, the speed at which the data is read is described.

A hot cache is an instance where data was read from the memory at the _fastest_ possible rate. This happens when the data is retrieved from L1.

A cold cache is the _slowest_ possible rate for data to be read, though, it's still successful so it's still considered a cache hit. The data is just found lower in the memory hierarchy such as in L3, or lower.

A warm cache is used to describe data that's found in L2 or L3. It's not as fast as a hot cache, but it's still faster than a cold cache. Generally, calling a cache warm is used to express that it's slower and closer to a cold cache than a hot one.

### Cache miss

A cache miss refers to the instance when the memory is searched, and the data isn't found. When this happens, the content is transferred and written into the cache.

!!! note "A walkthrough"
    Visiting a product page on Amazon you've never looked at before: first view is a cache miss, the servers have to query the database for the price, description, and reviews. Because that data just got fetched, it's written into the cache. If you or anyone else requests that same page again within the next few minutes, it's now a cache hit, served instantly from memory, no database query needed. A cache miss isn't free just because it "worked", it's strictly slower than even a cold hit, since it means going all the way to the original slow source. This is why hit rate (percentage of requests served from cache vs. missed) is such a commonly tracked metric, a low hit rate means the cache isn't actually helping much.

## Cache Invalidation

Cache invalidation is a process where the computer system declares the cache entries as invalid and removes or replaces them. If the data is modified, it should be invalidated in the cache, if not, this can cause inconsistent application behavior. There are three kinds of caching systems:

!!! note "Why this is genuinely hard"
    Say Amazon caches a product's price at $49.99. The seller drops the price to $39.99 in the database. If nothing tells the cache that price changed, it keeps confidently serving $49.99 to everyone, even though the real price is now $39.99. That's the invalidation problem, the cache doesn't automatically know the underlying data changed. The three strategies below are really about *when* the database and cache actually get synced relative to each other, and each trades write speed against consistency risk.

### Write-through cache

![write-through-cache](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/caching/write-through-cache.png)

Data is written into the cache and the corresponding database simultaneously.

**Pro**: Fast retrieval, complete data consistency between cache and storage.

**Con**: Higher latency for write operations.

!!! note "When to use it"
    Good for data where correctness really matters, e.g. that Amazon price, or a bank account balance, since cache and database are always guaranteed to be in sync.

### Write-around cache

![write-around-cache](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/caching/write-around-cache.png)

Where write directly goes to the database or permanent storage, bypassing the cache.

**Pro**: This may reduce latency.

**Con**: It increases cache misses because the cache system has to read the information from the database in case of a cache miss. As a result, this can lead to higher read latency in the case of applications that write and re-read the information quickly. Reads happen from slower back-end storage and experience higher latency.

!!! note "When to use it"
    Suits data that's written often but rarely re-read right away, e.g. logging analytics events, you write a ton of them, but you're not immediately re-reading the one you just wrote. If something is written and then immediately re-read before it's been cached, that read is a guaranteed miss.

### Write-back cache

![write-back-cache](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/caching/write-back-cache.png)

Where the write is only done to the caching layer and the write is confirmed as soon as the write to the cache completes. The cache then asynchronously syncs this write to the database.

**Pro**: This would lead to reduced latency and high throughput for write-intensive applications.

**Con**: There is a risk of data loss in case the caching layer crashes. We can improve this by having more than one replica acknowledging the write in the cache.

!!! note "When to use it"
    Used when write speed matters more than the small risk of loss, e.g. caching view counts on a video, losing a few views in a crash is a minor loss, not tragic. You would not use write-back for something like a financial transaction, where the risk of a lost, unsynced write is unacceptable.

## Eviction policies

Following are some of the most common cache eviction policies:

- **First In First Out (FIFO)**: The cache evicts the first block accessed first without any regard to how often or how many times it was accessed before.
- **Last In First Out (LIFO)**: The cache evicts the block accessed most recently first without any regard to how often or how many times it was accessed before.
- **Least Recently Used (LRU)**: Discards the least recently used items first.
- **Most Recently Used (MRU)**: Discards, in contrast to LRU, the most recently used items first.
- **Least Frequently Used (LFU)**: Counts how often an item is needed. Those that are used least often are discarded first.
- **Random Replacement (RR)**: Randomly selects a candidate item and discards it to make space when necessary.

!!! note "LRU vs LFU vs FIFO, concretely"
    **LRU** is by far the most common default (Redis supports it, browsers use something like it), because it aligns with locality of reference: if something hasn't been touched in a while, it's statistically less likely to be needed again soon. Example: a cache holding pages for Products A, B, C is full, and D is requested. LRU checks which of A, B, C was accessed *longest ago*, not created longest ago, and evicts that one. If B was viewed 10 seconds ago but A and C haven't been touched in 10 minutes, LRU evicts A or C, not B, even if B was cached first.

    **LFU** tracks *how often* something is accessed rather than how recently, and can outperform LRU when something is accessed rarely but consistently (e.g. a reference page checked once a day) vs. something that got a sudden one-time burst of traffic and went cold, LRU might accidentally keep the burst item just because it was recently touched, while LFU correctly identifies it as not actually a frequent visitor.

    **FIFO** is the simplest and dumbest, it evicts whichever item entered first, ignoring how often or recently it's been accessed since, so it can evict something still actively in use just because it arrived earliest.

    A related tool many real caches also use is **TTL (time-to-live)**, the same concept as [DNS record TTLs](domain-name-system-dns.md), where cached data is automatically considered stale and evicted after a fixed time regardless of access pattern, e.g. "cache this product price for at most 60 seconds," a simple, blunt way to bound how long stale data can possibly be served even without explicit invalidation logic.

## Distributed Cache

![distributed-cache](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/caching/distributed-cache.png)

A distributed cache is a system that pools together the random-access memory (RAM) of multiple networked computers into a single in-memory data store used as a data cache to provide fast access to data. While most caches are traditionally in one physical server or hardware component, a distributed cache can grow beyond the memory limits of a single computer by linking together multiple computers.

Concrete example: [Redis Cluster](clustering.md) is exactly this, instead of one Redis instance holding all cached data (limited by that one machine's RAM), the cached data is spread across many Redis nodes, and the cluster as a whole can hold far more than any single machine could. Each node holds a slice of the total data, and the nodes coordinate with each other (this is what makes them an actual cluster) to know who owns what.

## Global Cache

![global-cache](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/caching/global-cache.png)

As the name suggests, we will have a single shared cache that all the application nodes will use. When the requested data is not found in the global cache, it's the responsibility of the cache to find out the missing piece of data from the underlying data store.

Concrete example: picture 50 Instagram app servers behind a load balancer. Instead of each server keeping its own separate local cache (the same data cached 50 separate times, wastefully, and worse, one server could have stale data while another has fresh data for the same key), they all point to one shared cache layer. Any of the 50 servers checks the global cache first; if it's missing, the global cache fetches it from the database, stores it, and returns it, so now all 50 servers see that same cached copy.

!!! note "How distributed and global combine in practice"
    These aren't two competing choices, a real production setup is usually both at once, just viewed from two different angles.

    <figure class="img-figure">
    <div class="hand-diagram">
    <svg viewBox="0 0 1200 660" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Three application servers routing requests to a cache cluster of three nodes, which reads through to storage on a miss">
      <defs>
        <pattern id="hachureBlueCache" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
          <rect width="8" height="8" fill="#e7f5ff" />
          <line x1="0" y1="0" x2="0" y2="8" stroke="#4dabf7" stroke-width="1" />
        </pattern>
        <pattern id="hachureOrangeCache" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
          <rect width="8" height="8" fill="#fff4e6" />
          <line x1="0" y1="0" x2="0" y2="8" stroke="#ffa94d" stroke-width="1" />
        </pattern>
        <pattern id="hachureGreyCache" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
          <line x1="0" y1="0" x2="0" y2="8" stroke="#868e96" stroke-width="1" opacity="0.5" />
        </pattern>
        <marker id="arrowheadBlueCache" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
          <path d="M0,0 L10,5 L0,10 Z" fill="#1971c2" />
        </marker>
        <marker id="arrowheadGreyCache" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
          <path d="M0,0 L10,5 L0,10 Z" fill="#868e96" />
        </marker>
      </defs>
      <rect x="70" y="80" width="120" height="120" fill="url(#hachureBlueCache)" stroke="#1971c2" stroke-width="2" transform="rotate(45 130 140)" />
      <text x="130" y="146" text-anchor="middle" font-size="20" font-weight="600" fill="#1e1e1e">App1</text>
      <rect x="70" y="260" width="120" height="120" fill="url(#hachureBlueCache)" stroke="#1971c2" stroke-width="2" transform="rotate(45 130 320)" />
      <text x="130" y="326" text-anchor="middle" font-size="20" font-weight="600" fill="#1e1e1e">App2</text>
      <rect x="70" y="440" width="120" height="120" fill="url(#hachureBlueCache)" stroke="#1971c2" stroke-width="2" transform="rotate(45 130 500)" />
      <text x="130" y="506" text-anchor="middle" font-size="20" font-weight="600" fill="#1e1e1e">App3</text>
      <text x="130" y="600" text-anchor="middle" font-size="18" fill="#1e1e1e">Application servers</text>
      <line x1="215" y1="140" x2="548" y2="147" stroke="#868e96" stroke-width="1" opacity="0.3" />
      <line x1="215" y1="140" x2="548" y2="493" stroke="#868e96" stroke-width="1" opacity="0.3" />
      <line x1="215" y1="320" x2="548" y2="147" stroke="#868e96" stroke-width="1" opacity="0.3" />
      <line x1="215" y1="320" x2="548" y2="493" stroke="#868e96" stroke-width="1" opacity="0.3" />
      <line x1="215" y1="500" x2="548" y2="147" stroke="#868e96" stroke-width="1" opacity="0.3" />
      <line x1="215" y1="500" x2="548" y2="493" stroke="#868e96" stroke-width="1" opacity="0.3" />
      <line x1="215" y1="140" x2="548" y2="318" stroke="#1971c2" stroke-width="2.5" marker-end="url(#arrowheadBlueCache)" />
      <line x1="215" y1="500" x2="548" y2="322" stroke="#1971c2" stroke-width="2.5" marker-end="url(#arrowheadBlueCache)" />
      <text x="382" y="205" text-anchor="middle" font-size="16" fill="#1971c2">product:123</text>
      <text x="382" y="440" text-anchor="middle" font-size="16" fill="#1971c2">product:123</text>
      <rect x="520" y="60" width="260" height="520" rx="24" fill="none" stroke="#868e96" stroke-width="1.5" stroke-dasharray="6 6" />
      <rect x="550" y="90" width="200" height="110" rx="16" fill="url(#hachureOrangeCache)" stroke="#e8590c" stroke-width="2" />
      <text x="650" y="151" text-anchor="middle" font-size="20" font-weight="600" fill="#1e1e1e">Cache-A</text>
      <rect x="550" y="265" width="200" height="110" rx="16" fill="url(#hachureOrangeCache)" stroke="#e8590c" stroke-width="2" />
      <text x="650" y="326" text-anchor="middle" font-size="20" font-weight="600" fill="#1e1e1e">Cache-B</text>
      <rect x="550" y="440" width="200" height="110" rx="16" fill="url(#hachureOrangeCache)" stroke="#e8590c" stroke-width="2" />
      <text x="650" y="501" text-anchor="middle" font-size="20" font-weight="600" fill="#1e1e1e">Cache-C</text>
      <text x="650" y="608" text-anchor="middle" font-size="18" fill="#1e1e1e">Cache cluster (nodes coordinate)</text>
      <line x1="790" y1="145" x2="790" y2="495" stroke="#868e96" stroke-width="1.5" stroke-dasharray="4 4" />
      <line x1="790" y1="145" x2="750" y2="145" stroke="#868e96" stroke-width="1.5" stroke-dasharray="4 4" />
      <line x1="790" y1="320" x2="750" y2="320" stroke="#868e96" stroke-width="1.5" stroke-dasharray="4 4" />
      <line x1="790" y1="495" x2="750" y2="495" stroke="#868e96" stroke-width="1.5" stroke-dasharray="4 4" />
      <line x1="800" y1="320" x2="985" y2="320" stroke="#868e96" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrowheadGreyCache)" />
      <text x="893" y="300" text-anchor="middle" font-size="15" fill="#1e1e1e">on miss</text>
      <ellipse cx="1070" cy="286" rx="70" ry="16" fill="url(#hachureGreyCache)" stroke="#868e96" stroke-width="2" />
      <path d="M1000,286 v100 a70,16 0 0 0 140,0 v-100" fill="url(#hachureGreyCache)" stroke="#868e96" stroke-width="2" />
      <text x="1070" y="430" text-anchor="middle" font-size="18" font-weight="600" fill="#1e1e1e">Storage</text>
    </svg>
    </div>
    <figcaption>App1 and App3 both ask for <code>product:123</code> and both land on Cache-B, same deterministic hash, no coordination between the app servers needed. Cache-A, Cache-B, and Cache-C coordinate directly with each other, that's what makes them a cluster.</figcaption>
    </figure>

    Each cache key (like `product:123`) gets hashed, and that hash deterministically maps to exactly one physical node, say it always maps to Cache-B. When App1 asks for `product:123`, its client library computes that same hash and routes the request directly to Cache-B. Five minutes later, when App3 asks for `product:123`, it computes the identical hash and also routes to Cache-B, getting the exact same cached value App1 got. Neither app server had to know or coordinate with the other, that's the **global** part, one shared, consistent answer no matter which app server asks.

    The **distributed** part is that "the cache" isn't literally one machine, `product:123` lives on Cache-B, but `product:456` might hash to Cache-A instead. The total cached dataset is spread across all 3 machines' combined RAM.

    App1, App2, and App3 don't talk to each other, same as any load-balanced servers, they just each independently consult the cache layer. Cache-A, Cache-B, and Cache-C **do** talk to each other, agreeing on a shared slot map (which key ranges live where) and handling failover if one dies, that's what actually makes the cache layer a cluster. So there are two separate relationships here: app servers to cache cluster is a load-balancing-style relationship (no coordination between clients), while the cache nodes among themselves is a true clustering relationship (active coordination).

## Use cases

Caching can have many real-world use cases such as:

- Database Caching
- Content Delivery Network (CDN)
- Domain Name System (DNS) Caching
- API Caching

**When not to use caching?**

Let's also look at some scenarios where we should not use cache:

- Caching isn't helpful when it takes just as long to access the cache as it does to access the primary data store.
- Caching doesn't work as well when requests have low repetition (higher randomness), because caching performance comes from repeated memory access patterns.
- Caching isn't helpful when the data changes frequently, as the cached version gets out of sync, and the primary data store must be accessed every time.

_It's important to note that a cache should not be used as permanent data storage. They are almost always implemented in volatile memory because it is faster, and thus should be considered transient._

## Advantages

Below are some advantages of caching:

- Improves performance
- Reduce latency
- Reduce load on the database
- Reduce network cost
- Increase Read Throughput

## Examples

Here are some commonly used technologies for caching:

- [Redis](https://redis.io)
- [Memcached](https://memcached.org)
- [Amazon Elasticache](https://aws.amazon.com/elasticache)
- [Aerospike](https://aerospike.com)

## Practice Questions

Test yourself. Click a question to reveal the answer.

??? question "1. Why can't a cache just hold a full copy of the entire database?"
    A cache trades capacity for speed, it lives in fast, limited, and expensive RAM, unlike a database which stores the complete, durable dataset on cheaper, larger disk-based storage. It only holds a subset, usually the "hot" data being requested a lot right now.

??? question "2. Is a cache miss the same speed as a cold cache hit?"
    No, a cache miss is slower. A cold hit still found the data somewhere in the cache hierarchy (just a slower tier like L3), while a miss means going all the way to the original slow source (database/disk), which is strictly slower than even the slowest cache tier.

??? question "3. Which write strategy would you use for a bank account balance, and which would you avoid, and why?"
    Use write-through, writes go to the cache and database simultaneously, guaranteeing they're always in sync, worth the extra write latency for correctness. Avoid write-back, since it confirms the write from the cache alone and syncs to the database asynchronously later, if the cache crashes before that sync completes, the write is lost forever, unacceptable for financial data.

??? question "4. A cache is full and Products A, B, C are stored in it. B was accessed 10 seconds ago, A and C haven't been touched in 10 minutes. Product D is requested. What does LRU evict, and what would FIFO have evicted instead?"
    LRU evicts whichever of A or C was accessed longest ago (not B, since it was just accessed), based on recency of access. FIFO ignores access patterns entirely and evicts whichever of A, B, C entered the cache first, which could even be B, if it happened to arrive earliest despite being the most recently used.

??? question "5. In a distributed cache made of Cache-A, Cache-B, and Cache-C, how do three separate app servers that never talk to each other all consistently route `product:123` to the same physical node?"
    Each app server's client library independently computes the same deterministic hash for `product:123`, and maps it against a shared slot map (which key ranges live on which node) that the cache cluster itself maintains. Since the hash function and slot map are identical everywhere, every app server arrives at the same routing decision without ever coordinating with each other directly.

??? question "6. In that same setup, which group is actually a cluster, the app servers or the cache nodes, and why?"
    The cache nodes (Cache-A, Cache-B, Cache-C) are the cluster, they actively coordinate with each other, agreeing on the slot map and handling failover. The app servers are not a cluster, they're independent and never talk to each other, each one simply consults the shared cache layer on its own, the same load-balancing-style relationship covered earlier.

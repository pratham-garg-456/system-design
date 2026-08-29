# Content Delivery Network (CDN)

A content delivery network (CDN) is a geographically distributed group of servers that work together to provide fast delivery of internet content. Generally, static files such as HTML/CSS/JS, photos, and videos are served from CDN.

![cdn-map](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/content-delivery-network/cdn-map.png)

## Why use a CDN?

Content Delivery Network (CDN) increases content availability and redundancy while reducing bandwidth costs and improving security. Serving content from CDNs can significantly improve performance as users receive content from data centers close to them and our servers do not have to serve requests that the CDN fulfills.

!!! note "In simple terms"
    Say a website's server lives in Virginia, USA. A user in Mumbai visits the site, every image, CSS file, and JS bundle has to physically travel thousands of miles, multiple network hops, real latency, speed of light is a hard limit, even a well-optimized server in Virginia can't make that distance disappear. A CDN solves this by pre-placing copies of static content (images, CSS, JS, videos) on servers scattered worldwide, called edge locations, so a user's request gets served by whichever edge is physically closest to them instead of traveling all the way to origin. The key word is static, this only works for content that's the same for everyone, it doesn't work for something like "what's in my shopping cart," which is different per user and still has to go to the actual origin server.

## How does a CDN work?

![cdn](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/content-delivery-network/cdn.png)

In a CDN, the origin server contains the original versions of the content while the edge servers are numerous and distributed across various locations around the world.

To minimize the distance between the visitors and the website's server, a CDN stores a cached version of its content in multiple geographical locations known as edge locations. Each edge location contains several caching servers responsible for content delivery to visitors within its proximity.

Once the static assets are cached on all the CDN servers for a particular location, all subsequent website visitor requests for static assets will be delivered from these edge servers instead of the origin, thus reducing the origin load and improving scalability.

For example, when someone in the UK requests our website which might be hosted in the USA, they will be served from the closest edge location such as the London edge location. This is much quicker than having the visitor make a complete request to the origin server which will increase the latency.

!!! note "A CDN is really caching + geo-routing, combined"
    When you load a YouTube video, the video file isn't streamed all the way from a US data center to a phone in India, it's served from a Google edge cache node much closer by, conceptually the same idea as [Netflix's Open Connect boxes](load-balancing.md#global-server-load-balancing-gslb) covered under load balancing, just framed as "CDN" instead of "video delivery network." The origin server holds the real, authoritative copy (like a database), the edge servers are the cache (like Redis), and picking the nearest edge location is the same geo-routing idea from global load balancing. A CDN is essentially [caching](caching.md) and [geo/global load balancing](load-balancing.md#global-server-load-balancing-gslb) applied specifically to static content, at global scale.

## Types

CDNs are generally divided into two types:

### Push CDNs

Push CDNs receive new content whenever changes occur on the server. We take full responsibility for providing content, uploading directly to the CDN, and rewriting URLs to point to the CDN. We can configure when content expires and when it is updated. Content is uploaded only when it is new or changed, minimizing traffic, but maximizing storage.

Sites with a small amount of traffic or sites with content that isn't often updated work well with push CDNs. Content is placed on the CDNs once, instead of being re-pulled at regular intervals.

!!! note "When this makes sense"
    A small company site with a handful of product images that rarely change: pushing those once to all edge locations is simple and guarantees fast delivery everywhere immediately, no "first user is slow" penalty.

### Pull CDNs

In a Pull CDN situation, the cache is updated based on request. When the client sends a request that requires static assets to be fetched from the CDN if the CDN doesn't have it, then it will fetch the newly updated assets from the origin server and populate its cache with this new asset, and then send this new cached asset to the user.

Contrary to the Push CDN, this requires less maintenance because cache updates on CDN nodes are performed based on requests from the client to the origin server. Sites with heavy traffic work well with pull CDNs, as traffic is spread out more evenly with only recently-requested content remaining on the CDN.

!!! note "Same idea as write-around caching"
    Pull CDN maps directly onto [write-around caching](caching.md#write-around-cache): the edge server doesn't have the content ahead of time, the first user in a region hits a cache miss, the edge fetches from origin, stores it, then serves it, every later user in that region gets it fast. The tradeoff is the same too, that first request per region is slow. A site like Instagram or Reddit, with millions of constantly changing images and posts, is a good fit, there's no way to manually push every upload to every edge location worldwide, so content naturally gets cached wherever it actually sees traffic, and low-traffic edges for a given post simply never bother caching it. This is the default and far more common approach, used by Cloudflare and CloudFront, since it requires zero extra work beyond pointing the CDN at the origin.

## CDN Invalidation

This is the same [cache invalidation](caching.md#cache-invalidation) problem covered under caching, just at global scale, and it can be trickier because there are now potentially hundreds of edge locations worldwide, each holding its own copy, and none of them automatically know when the origin changes.

Update a CSS file on the origin server, and the London edge, the Tokyo edge, and the Mumbai edge might each keep serving their own old cached copy for hours, until each one's cache naturally expires. Different users around the world could be seeing different versions of a website at the same time.

The most common control is **TTL (time-to-live)**, the same concept from regular caching: configure how long an edge keeps serving a cached copy before treating it as stale and re-fetching from origin. Shorter TTL means fresher content but more origin load; longer TTL means less origin load but content can be stale for longer.

Sometimes a TTL can't be waited out, e.g. a bug just shipped in a JS bundle and every edge needs to drop it right now. This is explicit **invalidation** (or "purging"), a command telling the CDN "drop this specific file everywhere immediately," rather than waiting for TTL expiry.

!!! note "Real tools for this"
    **Amazon CloudFront** has a "Create Invalidation" action for exactly this, give it a path like `/app.js` and every edge location worldwide drops its cached copy and re-fetches fresh from origin on the next request.

    A cheaper, very common alternative is **cache-busting via filename**: instead of invalidating `app.js`, the build output is named `app.a1b2c3.js`, a hash of the file's content baked into the filename, so every deploy produces a brand-new filename. Since it's a URL the CDN has never seen, there's nothing stale to invalidate, old cached copies just sit unused (and eventually expire via TTL) while every user immediately gets the new file under its new name. This sidesteps the invalidation problem entirely, and it's why hashed filenames show up in almost every production web app's build output.

## Disadvantages

As we all know good things come with extra costs, so let's discuss some disadvantages of CDNs:

- **Extra charges**: It can be expensive to use a CDN, especially for high-traffic services.
- **Restrictions**: Some organizations and countries have blocked the domains or IP addresses of popular CDNs.
- **Location**: If most of our audience is located in a country where the CDN has no servers, the data on our website may have to travel further than without using any CDN.

## Examples

Here are some widely used CDNs:

- [Amazon CloudFront](https://aws.amazon.com/cloudfront)
- [Google Cloud CDN](https://cloud.google.com/cdn)
- [Cloudflare CDN](https://www.cloudflare.com/cdn)
- [Fastly](https://www.fastly.com/products/cdn)

## Practice Questions

Test yourself. Click a question to reveal the answer.

??? question "1. Why can't a CDN help with something like a user's shopping cart contents?"
    A CDN only works for static content, the same for every user and not changing per-request, like images, CSS, or JS bundles. Shopping cart contents are dynamic and different per user, so they still have to be served by the actual origin server, not a cached edge copy.

??? question "2. How is a CDN basically a combination of two concepts already covered elsewhere in these notes?"
    It's caching (the origin holds the authoritative copy, edge servers are the cache) combined with geo/global load balancing (routing a user to whichever edge location is physically closest), applied specifically to static content at global scale.

??? question "3. Which write strategy from the Caching page does Pull CDN map onto, and why?"
    Write-around caching. Content isn't placed on the edge ahead of time, the first request in a region is a cache miss, triggering a fetch from origin that populates the edge cache, every later request in that region is then served fast. The tradeoff is the same too, that first request per region is slower.

??? question "4. A small site with a handful of rarely-changing product images vs. a site like Instagram with millions of constantly changing posts, which CDN type fits each, and why?"
    The small site fits Push CDN, pushing the small, stable set of assets to every edge once guarantees fast delivery everywhere with no first-request penalty. Instagram fits Pull CDN, there's no way to manually push every new upload to every edge worldwide, so content naturally gets cached only where it actually sees traffic.

??? question "5. Why might waiting for a TTL to expire not be good enough, and what's the fix?"
    A TTL only expires on a fixed schedule, but sometimes stale content needs to be gone immediately, e.g. a bug just shipped in a JS bundle. The fix is explicit invalidation (purging), a command that tells the CDN to drop a specific file from every edge location right now, rather than waiting for the TTL countdown.

??? question "6. Why does naming a build file `app.a1b2c3.js` (a content hash) avoid needing to invalidate it at all?"
    Since the hash changes whenever the file's content changes, every deploy produces a brand-new filename, a URL the CDN has never seen before. There's nothing stale to invalidate, because it's not the same URL being updated, old cached copies under the old filename just sit unused and eventually expire via TTL, while every user immediately gets the new file under its new name.

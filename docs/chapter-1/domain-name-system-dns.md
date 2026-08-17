# Domain Name System (DNS)

Earlier we learned about IP addresses that enable every machine to connect with other machines. But as we know humans are more comfortable with names than numbers. It's easier to remember a name like `google.com` than something like `122.250.192.232`.

This brings us to Domain Name System (DNS) which is a hierarchical and decentralized naming system used for translating human-readable domain names to IP addresses.

## How DNS works

![how-dns-works](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/domain-name-system/how-dns-works.png)

DNS lookup involves the following eight steps:

1. A client types [example.com](http://example.com) into a web browser, the query travels to the internet and is received by a **resolver**.
2. The **resolver** then queries a **root nameserver**.
3. The **root nameserver** responds to the **resolver** with the address of a Top-Level Domain (TLD).
4. The **resolver** then makes a request to the `.com` TLD.
5. The **TLD nameserver** then responds with the location of the domain's **authoritative nameserver**, not the website's IP address yet, just where to find [example.com](http://example.com)'s own nameserver.
6. Lastly, the **resolver** sends a query to the domain's **nameserver**.
7. The IP address for [example.com](http://example.com) is then returned to the **resolver** from the **nameserver**.
8. The **resolver** then responds to the web browser with the IP address of the domain requested initially.

Once the IP address has been resolved, the client should be able to request content from the resolved IP address. For example, the resolved IP may return a webpage to be rendered in the browser.

## Server types

Now, let's look at the four key groups of servers that make up the DNS infrastructure.

### Resolver

A **resolver** (sometimes called a recursive resolver) is the first stop in a DNS query. It acts as a middleman between a client and a **nameserver**. After receiving a DNS query from a web client, a **resolver** will either respond with cached data, or send a request to a **root nameserver**, followed by another request to a **TLD nameserver**, and then one last request to an **authoritative nameserver**. After receiving a response from the **authoritative nameserver** containing the requested IP address, the **resolver** then sends a response to the client.

### Root nameserver

A **root nameserver** accepts a **resolver's** query which includes a domain name, and responds by directing the **resolver** to a **TLD nameserver**, based on the extension of that domain (`.com`, `.net`, `.org`, etc.). **Root nameservers** are overseen by a nonprofit called the [Internet Corporation for Assigned Names and Numbers (ICANN)](https://www.icann.org).

There are 13 **root nameservers** known to every **resolver**. Note that while there are 13 root nameservers, that doesn't mean that there are only 13 machines in the root nameserver system. There are 13 types of root nameservers, but there are multiple copies of each one all over the world, which use [Anycast routing](https://en.wikipedia.org/wiki/Anycast) to provide speedy responses.

!!! note "In simple terms"
    A **root nameserver's** only job is to look at a domain's ending (`.com`, `.org`, etc.) and point the **resolver** to the right **TLD nameserver**, it doesn't know any actual website's IP address. The "13" refers to 13 addresses (`a.root-servers.net` through `m.root-servers.net`), and every address holds an identical copy of the full list of TLDs, so any one of them can fully answer a query about any domain ending. Each address is also backed by hundreds of physical machines worldwide via Anycast, so a query always reaches whichever copy is geographically closest, and losing any number of individual machines still leaves the system fully working.

### TLD nameserver

A **TLD nameserver** maintains information for all the domain names that share a common domain extension, such as `.com`, `.net`, or whatever comes after the last dot in a URL.

Management of **TLD nameservers** is handled by the [Internet Assigned Numbers Authority (IANA)](https://www.iana.org), which is a branch of [ICANN](https://www.icann.org). The IANA breaks up **TLD nameservers** into two main groups:

- **Generic top-level domains**: These are domains like `.com`, `.org`, `.net`, `.edu`, and `.gov`.
- **Country code top-level domains**: These include any domains that are specific to a country or state. Examples include `.uk`, `.us`, `.ru`, and `.jp`.

### Authoritative nameserver

The **authoritative nameserver** is usually the **resolver's** last step in the journey for an IP address. The **authoritative nameserver** contains information specific to the domain name it serves (e.g. [google.com](http://google.com)) and it can provide the **resolver** with the IP address found in the DNS A record, or if the domain has a CNAME record (alias) it will provide the **resolver** with an alias domain, at which point the **resolver** will have to perform a whole new DNS lookup to procure a record from an **authoritative nameserver** (often an A record containing an IP address). If it cannot find the domain, returns the NXDOMAIN message.

!!! note "A vs AAAA records"
    An **A record** (Address) holds the **IPv4** address of a domain, e.g. `93.184.216.34`. An **AAAA record** (IP Version 6 Address) holds the **IPv6** address for that same domain instead. Both are covered in more detail in [Record Types](#record-types) below.

## Query Types

There are three types of queries in a DNS system:

### Recursive

In a recursive query, a DNS client requires that a **resolver** will respond to the client with either the requested resource record or an error message if it can't find the record.

### Iterative

In an iterative query, a DNS client provides a hostname, and the **resolver** returns the best answer it can. If the **resolver** has the relevant DNS records in its cache, it returns them. If not, it refers the DNS client to the **root nameserver** or another **authoritative nameserver** that is nearest to the required DNS zone. The DNS client must then repeat the query directly against the **nameserver** it was referred to.

### Non-recursive

A non-recursive query is a query in which the **resolver** already knows the answer. It either immediately returns a DNS record because it already stores it in a local cache, or queries the **nameserver** that is authoritative for the record, meaning it definitely holds the correct IP for that hostname. In both cases, there is no need for additional rounds of queries (like in recursive or iterative queries). Rather, a response is immediately returned to the client.

## Record Types

DNS records (aka zone files) are instructions that live in **authoritative nameservers** and provide information about a domain including what IP address is associated with that domain and how to handle requests for that domain.

These records consist of a series of text files written in what is known as _DNS syntax_. DNS syntax is just a string of characters used as commands that tell the DNS server what to do. All DNS records also have a _"TTL"_, which stands for time-to-live, and indicates how often a DNS server will refresh that record.

There are more record types but for now, let's look at some of the most commonly used ones:

- **A (Address record)**: This is the record that holds the IP address of a domain.
- **AAAA (IP Version 6 Address record)**: The record that contains the IPv6 address for a domain (as opposed to A records, which stores the IPv4 address).
- **CNAME (Canonical Name record)**: Forwards one domain or subdomain to another domain, does NOT provide an IP address.
- **MX (Mail exchanger record)**: Directs mail to an email server.
- **TXT (Text Record)**: This record lets an admin store text notes in the record. These records are often used for email security.
- **NS (Name Server records)**: Stores the **nameserver** for a DNS entry.
- **SOA (Start of Authority)**: Stores admin information about a domain.
- **SRV (Service Location record)**: Specifies a port for specific services.
- **PTR (Reverse-lookup Pointer record)**: Provides a domain name in reverse lookups.
- **CERT (Certificate record)**: Stores public key certificates.

## Example: Pointing a domain at GitHub Pages

Say you own `example.com` and want it to serve a site hosted on GitHub Pages. You'd add these records at your domain's **authoritative nameserver** (usually managed through your registrar, or a separate DNS provider like Cloudflare):

**Apex/root domain** (`example.com` itself): GitHub Pages gives you 4 fixed IPs, so you add 4 **A records**, one per IP:

```
example.com.   A   185.199.108.153
example.com.   A   185.199.109.153
example.com.   A   185.199.110.153
example.com.   A   185.199.111.153
```

**Subdomain** (`www.example.com`): since only the apex domain has the restriction against combining a CNAME with other records, a subdomain can just use one **CNAME record** instead:

```
www.example.com.   CNAME   yourusername.github.io.
```

That CNAME doesn't give `www.example.com` its own IP, it just says *"resolve `yourusername.github.io` instead,"* triggering a separate lookup for GitHub's own domain.

A site served directly from `*.github.io` (with no custom domain) skips all of this: `github.io` is a domain GitHub itself owns, so its authoritative nameserver is GitHub's own infrastructure, not something any individual user configures.

## Subdomains

A subdomain is an additional part of our main domain name. It is commonly used to logically separate a website into sections. We can create multiple subdomains or child domains on the main domain.

For example, `blog.example.com` where `blog` is the subdomain, `example` is the primary domain and `.com` is the top-level domain (TLD). Similar examples can be `support.example.com` or `careers.example.com`.

## DNS Zones

A DNS zone is a distinct part of the domain namespace which is delegated to a legal entity like a person, organization, or company, who is responsible for maintaining the DNS zone. A DNS zone is also an administrative function, allowing for granular control of DNS components, such as **authoritative nameservers**.

## DNS Caching

A DNS cache (sometimes called a DNS resolver cache) is a temporary database, maintained by a computer's operating system, that contains records of all the recent visits and attempted visits to websites and other internet domains. In other words, a DNS cache is just a memory of recent DNS lookups that our computer can quickly refer to when it's trying to figure out how to load a website.

The Domain Name System implements a time-to-live (TTL) on every DNS record. TTL specifies the number of seconds the record can be cached by a DNS client or server. When the record is stored in a cache, whatever TTL value came with it gets stored as well. The server continues to update the TTL of the record stored in the cache, counting down every second. When it hits zero, the record is deleted or purged from the cache. At that point, if a query for that record is received, the DNS server has to start the resolution process.

## Reverse DNS

A reverse DNS lookup is a DNS query for the domain name associated with a given IP address. This accomplishes the opposite of the more commonly used forward DNS lookup, in which the DNS system is queried to return an IP address. The process of reverse resolving an IP address uses PTR records. If the **nameserver** does not have a PTR record, it cannot resolve a reverse lookup.

Reverse lookups are commonly used by email servers. Email servers check and see if an email message came from a valid server before bringing it onto their network. Many email servers will reject messages from any server that does not support reverse lookups or from a server that is highly unlikely to be legitimate.

_Note: Reverse DNS lookups are not universally adopted as they are not critical to the normal function of the internet._

## Examples

These are some widely used managed DNS solutions:

- [Route53](https://aws.amazon.com/route53)
- [Cloudflare DNS](https://www.cloudflare.com/dns)
- [Google Cloud DNS](https://cloud.google.com/dns)
- [Azure DNS](https://azure.microsoft.com/en-in/services/dns)
- [NS1](https://ns1.com/products/managed-dns)

## Practice Questions

Test yourself. Click a question to reveal the answer.

??? question "1. Are resolver and recursive resolver different things?"
    No, they're the same server. Resolver is the casual name, recursive resolver is the more precise technical name, describing what it does: it performs the recursive lookup chain on your behalf.

??? question "2. What does a root nameserver actually know, and what doesn't it know?"
    A root nameserver only knows which TLD nameserver handles each domain ending (`.com`, `.org`, etc.). It doesn't know any individual website's actual IP address.

??? question "3. What does the 13 in 13 root nameservers actually refer to?"
    13 unique addresses (`a.root-servers.net` through `m.root-servers.net`), each backed by hundreds of physical machines worldwide via Anycast. Every address holds an identical copy of the full TLD list, so any one of them can answer a query about any domain ending.

??? question "4. What does a TLD nameserver return when queried, the website's IP address?"
    No. It returns the location of the domain's authoritative nameserver, not the final IP. The resolver still has to make one more request, to that authoritative nameserver, to get the actual A record.

??? question "5. What makes a nameserver authoritative for a domain?"
    It holds the official, current records for that domain, not a cached copy. When the domain owner updates a record, they update it directly on the authoritative nameserver; every other resolver's cached copy is secondhand and can be stale until its TTL expires.

??? question "6. A recursive query and an iterative query happen in the same DNS lookup. Who sends which?"
    Your browser sends one recursive query to the resolver, give me the final answer, don't make me do more work. The resolver then sends a series of iterative queries up the chain, to the root, TLD, and authoritative nameservers, each of which can just reply with a referral to the next server instead of the final answer.

??? question "7. Can a domain have both an A record and a CNAME record for the same name?"
    No. A CNAME says a name is an alias for another domain, so it can't also have its own separate IP address at that same name. This restriction only applies to the exact same name though, a subdomain can use CNAME even if the apex domain uses A records.

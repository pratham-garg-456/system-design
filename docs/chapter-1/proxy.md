# Proxy

A proxy server is an intermediary piece of hardware/software sitting between the client and the backend server. It receives requests from clients and relays them to the origin servers. Typically, proxies are used to filter requests, log requests, or sometimes transform requests (by adding/removing headers, encrypting/decrypting, or compression).

!!! note "In simple terms"
    A proxy is just a middleman, a server that sits between two parties and relays requests on their behalf instead of the two parties talking directly. The key question that determines which kind of proxy it is: whose side is it standing on, the client's, or the server's?

## Types

There are two types of proxies:

### Forward Proxy

A forward proxy, often called a proxy, proxy server, or web proxy is a server that sits in front of a group of client machines. When those computers make requests to sites and services on the internet, the proxy server intercepts those requests and then communicates with web servers on behalf of those clients, like a middleman.

![forward-proxy](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/proxy/forward-proxy.png)

**Advantages**

Here are some advantages of a forward proxy:

- Block access to certain content
- Allows access to [geo-restricted](https://en.wikipedia.org/wiki/Geo-blocking) content
- Provides anonymity
- Avoid other browsing restrictions

Although proxies provide the benefits of anonymity, they can still track our personal information. Setup and maintenance of a proxy server can be costly and requires configurations.

!!! note "Stands on the client's side"
    A lot of schools and offices run a forward proxy, every employee's laptop routes all its internet traffic through one central proxy server before it reaches the actual internet. That proxy can block access to certain sites, log what employees browse, or hide each employee's real IP from the outside sites they visit, the external site only ever sees the proxy's IP, not each laptop's. A VPN is a close relative of this same idea, traffic routes through the VPN provider's server before reaching its destination, largely the same "hide the client, control what it can reach" pattern.

### Reverse Proxy

A reverse proxy is a server that sits in front of one or more web servers, intercepting requests from clients. When clients send requests to the origin server of a website, those requests are intercepted by the reverse proxy server.

The difference between a forward and reverse proxy is subtle but important. A simplified way to sum it up would be to say that a forward proxy sits in front of a client and ensures that no origin server ever communicates directly with that specific client. On the other hand, a reverse proxy sits in front of an origin server and ensures that no client ever communicates directly with that origin server.

!!! note "Stands on the server's side"
    Instead of an app server being directly exposed to the internet, a reverse proxy sits in front of it, clients think they're talking to "the website," but they're actually talking to the reverse proxy, which forwards the request to the real backend server(s) and returns the response back. The client never knows the real backend's address or how many of them there are. **Nginx** is a common example of software deployed as a reverse proxy, sitting in front of a backend app (like Node.js or Python) and forwarding requests to it, this is the exact same software that also does round-robin load balancing, which the next section explains.

![reverse-proxy](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-I/proxy/reverse-proxy.png)

Introducing reverse proxy results in increased complexity. A single reverse proxy is a single point of failure, configuring multiple reverse proxies (i.e. a failover) further increases complexity.

**Advantages**

Here are some advantages of using a reverse proxy:

- Improved security
- Caching
- SSL encryption
- Load balancing
- Scalability and flexibility

## Load balancer vs Reverse Proxy

Wait, isn't reverse proxy similar to a load balancer? Well, no as a load balancer is useful when we have multiple servers. Often, load balancers route traffic to a set of servers serving the same function, while reverse proxies can be useful even with just one web server or application server. A reverse proxy can also act as a load balancer but not the other way around.

!!! note "Category vs specific capability"
    A reverse proxy in front of exactly one backend server still does real work, SSL termination, caching, hiding the backend's real address, security headers, but there's no decision being made about which server handles a request, since there's only one option. That's a reverse proxy that isn't a load balancer, because load balancing requires something to balance between. Point that same reverse proxy at multiple backends instead, and it now has to make a routing decision on every request, at that point it's doing everything it did before plus load balancing. That's why the relationship is one-directional: a reverse proxy can act as a load balancer once it has multiple backends, but a load balancer can't meaningfully exist without being some form of reverse proxy first, the very definition already implies "sits in front of servers, intercepts client requests, forwards them onward."

    Concretely, this is a config change, not a different piece of software. **Nginx** configured with a single backend is acting purely as a reverse proxy, no load balancing happening:

    ```nginx
    server {
        location / {
            proxy_pass http://backend1;
        }
    }
    ```

    Add a second and third backend, and it's now also load balancing, same software, same reverse proxy role, just now with an actual choice to make:

    ```nginx
    upstream backend {
        server backend1;
        server backend2;
        server backend3;
    }

    server {
        location / {
            proxy_pass http://backend;
        }
    }
    ```

## Examples

Below are some commonly used proxy technologies:

- [Nginx](https://www.nginx.com)
- [HAProxy](http://www.haproxy.org)
- [Traefik](https://doc.traefik.io/traefik)
- [Envoy](https://www.envoyproxy.io)

## Practice Questions

Test yourself. Click a question to reveal the answer.

??? question "1. What single question determines whether something is a forward proxy or a reverse proxy?"
    Whose side it's standing on. A forward proxy stands on the client's side and ensures no origin server ever talks directly to that specific client. A reverse proxy stands on the server's side and ensures no client ever talks directly to that origin server.

??? question "2. A company's office blocks employees from visiting certain websites and hides each employee's real IP from the outside internet. Is that a forward or reverse proxy, and why?"
    A forward proxy. It sits in front of a group of clients (the employees' laptops), intercepting their outbound requests, controlling what they can reach, and hiding their individual identities from the sites they visit.

??? question "3. Why can't a load balancer exist without also being some form of reverse proxy?"
    The very definition of a load balancer already implies sitting in front of servers, intercepting client requests, and forwarding them onward, which is just a reverse proxy's job description. Load balancing is simply the specific behavior of choosing between multiple backends, layered on top of that reverse proxy role.

??? question "4. Nginx is configured with `proxy_pass http://backend1;` pointing at a single server. Is it acting as a load balancer? What if a second and third backend are added?"
    With one backend, no, it's a reverse proxy but not a load balancer, since there's no decision to make about which server handles a request. Adding a second and third backend (via an `upstream` block) means Nginx now has to choose between them on every request, at that point it's doing load balancing too, same software, same reverse proxy role, just with an actual routing decision now.

??? question "5. What is Nginx, in one sentence, and why did it become popular for high-traffic sites?"
    Nginx is an open-source server program that can act as a web server, reverse proxy, and load balancer depending on its configuration. It became popular because its event-driven, asynchronous architecture lets a single process handle tens of thousands of concurrent connections efficiently, unlike older servers that dedicated a thread or process per connection.

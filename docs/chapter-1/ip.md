# IP

An IP address is a unique address that identifies a device on the internet or a local network. IP stands for _"Internet Protocol"_, which is the set of rules governing the format of data sent via the internet or local network.

In essence, IP addresses are the identifier that allows information to be sent between devices on a network. They contain location information and make devices accessible for communication. The internet needs a way to differentiate between different computers, routers, and websites. IP addresses provide a way of doing so and form an essential part of how the internet works.

## Versions

Now, let's learn about the different versions of IP addresses:

### IPv4

The original Internet Protocol is IPv4 which uses a 32-bit numeric dot-decimal notation that only allows for around 4 billion IP addresses. Initially, it was more than enough but as internet adoption grew, we needed something better.

_Example: `102.22.192.181`_

### IPv6

IPv6 is a new protocol that was introduced in 1998. Deployment commenced in the mid-2000s and since the internet users have grown exponentially, it is still ongoing.

This new protocol uses 128-bit alphanumeric hexadecimal notation. This means that IPv6 can provide about ~340e+36 IP addresses. That's more than enough to meet the growing demand for years to come.

_Example: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`_

## Types

Let's discuss types of IP addresses:

### Public

A public IP address is an address where one primary address is associated with your whole network. In this type of IP address, each of the connected devices has the same IP address.

_Example: IP address provided to your router by the ISP._

### Private

A private IP address is a unique IP number assigned to every device that connects to your internet network, which includes devices like computers, tablets, and smartphones, which are used in your household.

_Example: IP addresses assigned by your home router (via DHCP) to your devices, e.g. `192.168.1.24`._

!!! note "Why private IPv4 addresses never ran out"
    IPv4 exhaustion only applies to the _public_ address pool handed out by internet registries. Private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) were permanently reserved by [RFC 1918](https://datatracker.ietf.org/doc/html/rfc1918) and are never routed on the public internet, so every home and office network can reuse the same private addresses simultaneously without conflict. A router uses [NAT](#nat) to let all the private-IP devices behind it share its single public IP, which is also a big reason IPv4 has lasted as long as it has despite the small address space.

### Static

A static IP address does not change and is one that was manually created, as opposed to having been assigned. These addresses are usually more expensive but are more reliable.

_Example: They are usually used for important things like reliable geo-location services, remote access, server hosting, etc._

### Dynamic

A dynamic IP address changes from time to time and is not always the same. It has been assigned by a [Dynamic Host Configuration Protocol (DHCP)](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol) server. Dynamic IP addresses are the most common type of internet protocol address. They are cheaper to deploy and allow us to reuse IP addresses within a network as needed.

_Example: They are more commonly used for consumer equipment and personal use._

## NAT

NAT (Network Address Translation) is the process a router uses to swap a device's private IP address for the router's own public IP address whenever traffic leaves the local network, and swap it back on the way in. It's what lets every device behind a single router share one public IP.

This is also why an outside device can't normally initiate a connection to something on your private network unannounced, since there's no existing entry in the router's translation table telling it which device to forward that traffic to.

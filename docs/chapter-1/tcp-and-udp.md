# TCP and UDP

## TCP

Transmission Control Protocol (TCP) is connection-oriented, meaning once a connection has been established, data can be transmitted in both directions. TCP has built-in systems to check for errors and to guarantee data will be delivered in the order it was sent, making it the perfect protocol for transferring information like still images, data files, and web pages.

That reliability comes from bookkeeping carried in every TCP header, which is far larger than just a source and destination port:

```
Source Port: 51342          Destination Port: 443
Sequence Number: 1461247570
Acknowledgment Number: 892034521
Flags: [SYN, ACK]
Window Size: 64240
Checksum: 0x4a2f
```

None of that ~20 bytes is your actual data, it's all spent sequencing, acknowledging, and managing the connection, which is why TCP uses more bandwidth than UDP to send the same amount of content.

### Connection Lifecycle

**SYN, ACK, and FIN** are flags inside that header which manage a connection's lifecycle:

- **SYN** (Synchronize): "I want to start a connection."
- **ACK** (Acknowledge): "I received that." Used both to confirm the connection and to confirm every piece of data received afterward.
- **FIN** (Finish): "I'm done sending, let's close this connection."

<div class="figure-row">
<figure class="img-figure">
<div class="hand-diagram">
<svg viewBox="0 0 1160 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="TCP connection opening handshake between Client and Server">
  <defs>
    <pattern id="hachureBlueOpen" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#e7f5ff" />
      <line x1="0" y1="0" x2="0" y2="8" stroke="#4dabf7" stroke-width="1" />
    </pattern>
    <pattern id="hachureOrangeOpen" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#fff4e6" />
      <line x1="0" y1="0" x2="0" y2="8" stroke="#ffa94d" stroke-width="1" />
    </pattern>
    <pattern id="hachureGreyOpen" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#868e96" stroke-width="1" opacity="0.5" />
    </pattern>
    <marker id="arrowheadOpenBlue" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#1971c2" />
    </marker>
    <marker id="arrowheadOpenGreen" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#2f9e44" />
    </marker>
  </defs>

  <rect x="150" y="180" width="160" height="160" fill="url(#hachureBlueOpen)" stroke="#1971c2" stroke-width="2" transform="rotate(45 230 260)" />
  <text x="230" y="266" text-anchor="middle" font-size="22" font-weight="600" fill="#1e1e1e">Client</text>

  <rect x="900" y="170" width="180" height="180" rx="24" fill="url(#hachureOrangeOpen)" stroke="#e8590c" stroke-width="2" />
  <text x="990" y="266" text-anchor="middle" font-size="22" font-weight="600" fill="#1e1e1e">Server</text>

  <rect x="420" y="40" width="18" height="480" fill="url(#hachureGreyOpen)" stroke="#868e96" stroke-width="1.5" />
  <rect x="860" y="40" width="18" height="480" fill="url(#hachureGreyOpen)" stroke="#868e96" stroke-width="1.5" />

  <text x="649" y="90" text-anchor="middle" font-size="20" fill="#1e1e1e">SYN</text>
  <line x1="438" y1="110" x2="855" y2="110" stroke="#1971c2" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrowheadOpenBlue)" />

  <text x="649" y="200" text-anchor="middle" font-size="20" fill="#1e1e1e">SYN + ACK</text>
  <line x1="860" y1="220" x2="443" y2="220" stroke="#1971c2" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrowheadOpenBlue)" />

  <text x="649" y="330" text-anchor="middle" font-size="20" fill="#1e1e1e">ACK</text>
  <line x1="438" y1="350" x2="855" y2="350" stroke="#1971c2" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrowheadOpenBlue)" />

  <text x="649" y="440" text-anchor="middle" font-size="20" fill="#1e1e1e">Data</text>
  <line x1="443" y1="460" x2="855" y2="460" stroke="#2f9e44" stroke-width="2" marker-end="url(#arrowheadOpenGreen)" marker-start="url(#arrowheadOpenGreen)" />
</svg>
</div>
<figcaption>Opening a connection: the three-way handshake, then data can flow.</figcaption>
</figure>

<figure class="img-figure">
<div class="hand-diagram">
<svg viewBox="0 0 1160 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="TCP connection closing handshake between Client and Server">
  <defs>
    <pattern id="hachureBlue" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#e7f5ff" />
      <line x1="0" y1="0" x2="0" y2="8" stroke="#4dabf7" stroke-width="1" />
    </pattern>
    <pattern id="hachureOrange" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#fff4e6" />
      <line x1="0" y1="0" x2="0" y2="8" stroke="#ffa94d" stroke-width="1" />
    </pattern>
    <pattern id="hachureGrey" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#868e96" stroke-width="1" opacity="0.5" />
    </pattern>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#1971c2" />
    </marker>
  </defs>

  <rect x="150" y="180" width="160" height="160" fill="url(#hachureBlue)" stroke="#1971c2" stroke-width="2" transform="rotate(45 230 260)" />
  <text x="230" y="266" text-anchor="middle" font-size="22" font-weight="600" fill="#1e1e1e">Client</text>

  <rect x="900" y="170" width="180" height="180" rx="24" fill="url(#hachureOrange)" stroke="#e8590c" stroke-width="2" />
  <text x="990" y="266" text-anchor="middle" font-size="22" font-weight="600" fill="#1e1e1e">Server</text>

  <rect x="420" y="40" width="18" height="480" fill="url(#hachureGrey)" stroke="#868e96" stroke-width="1.5" />
  <rect x="860" y="40" width="18" height="480" fill="url(#hachureGrey)" stroke="#868e96" stroke-width="1.5" />

  <text x="649" y="90" text-anchor="middle" font-size="20" fill="#1e1e1e">FIN</text>
  <line x1="438" y1="110" x2="855" y2="110" stroke="#1971c2" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrowhead)" />

  <text x="649" y="200" text-anchor="middle" font-size="20" fill="#1e1e1e">ACK</text>
  <line x1="860" y1="220" x2="443" y2="220" stroke="#1971c2" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrowhead)" />

  <text x="649" y="330" text-anchor="middle" font-size="20" fill="#1e1e1e">FIN</text>
  <line x1="860" y1="350" x2="443" y2="350" stroke="#1971c2" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrowhead)" />

  <text x="649" y="440" text-anchor="middle" font-size="20" fill="#1e1e1e">ACK</text>
  <line x1="438" y1="460" x2="855" y2="460" stroke="#1971c2" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrowhead)" />
</svg>
</div>
<figcaption>Closing a connection: the four-step handshake, since either side can close independently.</figcaption>
</figure>
</div>

!!! note "Why ACK and FIN aren't combined like SYN and ACK"
    Opening combines the server's acknowledgment and its own SYN into one **SYN+ACK** packet, since the server always wants to do both at once. Closing keeps ACK and FIN separate, because a TCP connection is really two independent directions: when the server receives the client's FIN, it immediately sends **ACK** to confirm, but it might still have data left to send back, so it only sends its own **FIN** once it's actually done. Some implementations optimize this into a combined packet when the server has nothing left to send, but the general model keeps them separate to handle the case where it does.

## UDP

User Datagram Protocol (UDP) is a simpler, connectionless internet protocol in which error-checking and recovery services are not required. With UDP, there is no overhead for opening a connection, maintaining a connection, or terminating a connection. Data is continuously sent to the recipient, whether or not they receive it.

<figure class="img-figure">
<div class="hand-diagram">
<svg viewBox="0 0 1160 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="UDP data flow from Client to Server, one direction, no handshake">
  <defs>
    <pattern id="hachureBlueUdp" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#e7f5ff" />
      <line x1="0" y1="0" x2="0" y2="8" stroke="#4dabf7" stroke-width="1" />
    </pattern>
    <pattern id="hachureOrangeUdp" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#fff4e6" />
      <line x1="0" y1="0" x2="0" y2="8" stroke="#ffa94d" stroke-width="1" />
    </pattern>
    <pattern id="hachureGreyUdp" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#868e96" stroke-width="1" opacity="0.5" />
    </pattern>
    <marker id="arrowheadUdpGreen" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#2f9e44" />
    </marker>
    <marker id="arrowheadUdpRed" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#e03131" />
    </marker>
  </defs>

  <rect x="150" y="180" width="160" height="160" fill="url(#hachureBlueUdp)" stroke="#1971c2" stroke-width="2" transform="rotate(45 230 260)" />
  <text x="230" y="266" text-anchor="middle" font-size="22" font-weight="600" fill="#1e1e1e">Client</text>

  <rect x="900" y="170" width="180" height="180" rx="24" fill="url(#hachureOrangeUdp)" stroke="#e8590c" stroke-width="2" />
  <text x="990" y="266" text-anchor="middle" font-size="22" font-weight="600" fill="#1e1e1e">Server</text>

  <rect x="420" y="40" width="18" height="480" fill="url(#hachureGreyUdp)" stroke="#868e96" stroke-width="1.5" />
  <rect x="860" y="40" width="18" height="480" fill="url(#hachureGreyUdp)" stroke="#868e96" stroke-width="1.5" />

  <text x="649" y="90" text-anchor="middle" font-size="20" fill="#1e1e1e">Datagram 1</text>
  <line x1="438" y1="110" x2="855" y2="110" stroke="#2f9e44" stroke-width="2" marker-end="url(#arrowheadUdpGreen)" />

  <text x="649" y="200" text-anchor="middle" font-size="20" fill="#1e1e1e">Datagram 2</text>
  <line x1="438" y1="220" x2="855" y2="220" stroke="#2f9e44" stroke-width="2" marker-end="url(#arrowheadUdpGreen)" />

  <text x="649" y="330" text-anchor="middle" font-size="20" fill="#e03131">Datagram 3 (lost)</text>
  <line x1="438" y1="350" x2="650" y2="350" stroke="#e03131" stroke-width="2" stroke-dasharray="4 4" marker-end="url(#arrowheadUdpRed)" />

  <text x="649" y="440" text-anchor="middle" font-size="20" fill="#1e1e1e">Datagram 4</text>
  <line x1="438" y1="460" x2="855" y2="460" stroke="#2f9e44" stroke-width="2" marker-end="url(#arrowheadUdpGreen)" />
</svg>
</div>
<figcaption>UDP just keeps sending datagrams, no handshake, no acknowledgment, no retransmission. A lost one is simply skipped.</figcaption>
</figure>

The header reflects that simplicity, just 4 fields and ~8 bytes, compared to TCP's dozen-odd fields above:

```
Source Port: 51342
Destination Port: 53
Length: 42
Checksum: 0x8f3c
```

No sequence numbers, no acknowledgments, no flags, no window size, just enough to identify sender, receiver, and catch basic corruption.

Concrete example: **a DNS lookup**. When your browser resolves `google.com` to an IP address, it sends a tiny UDP request to a DNS server on **port 53**, no handshake, just a single request and response. If it's lost, the browser simply retries after a short timeout, cheaper than paying TCP's setup cost for something this small and quick.

## Ports

Both headers above start with a source and destination **port**, a number (0–65535) identifying which specific application or service on a device a piece of data is meant for. An IP address only gets data to the right *device*, since a device can run many networked programs at once, sharing that same IP, so the port is what tells it which program should actually handle the data.

Some ports are reserved by convention for well-known services:

| Port | Service |
| ---- | ------- |
| 80   | HTTP    |
| 443  | HTTPS   |
| 53   | DNS     |
| 22   | SSH     |
| 25   | SMTP    |

## TCP vs UDP

| Feature             | TCP                                         | UDP                                |
| ------------------- | -------------------------------------------- | ---------------------------------- |
| Connection          | Requires an established connection          | Connectionless protocol            |
| Guaranteed delivery | Can guarantee delivery of data              | Cannot guarantee delivery of data  |
| Re-transmission     | Re-transmission of lost packets is possible | No re-transmission of lost packets |
| Speed               | Slower than UDP                             | Faster than TCP                    |
| Broadcasting        | Does not support broadcasting               | Supports broadcasting              |
| Use cases           | HTTPS, HTTP, SMTP, POP, FTP, etc            | Video streaming, DNS, VoIP, etc    |

- **Loading a webpage (TCP)**: every byte of HTML/CSS/JS matters, a corrupted or missing chunk breaks the page. So the connection pays for a handshake up front and retransmits anything lost, even if that means waiting a little longer for the page to arrive correctly.
- **A live video call (UDP)**: a dropped frame from a second ago is already outdated by the time it could be resent. So there's no handshake, no retransmission, frames just get fired continuously, and a lost one is simply skipped so the call keeps up with real time.

It's the same trade-off as the header sizes above: TCP spends bandwidth and time on guarantees, UDP spends neither, betting that speed matters more than completeness.

## Practice Questions

Test yourself. Click a question to reveal the answer.

??? question "1. Why does TCP use more bandwidth than UDP to send the same amount of actual data?"
    TCP needs a three-way handshake before any data is sent, a larger header (~20+ bytes vs UDP's ~8) on every segment, separate ACK packets confirming receipt, and a multi-step handshake to close the connection. None of that carries your actual content, it's all bookkeeping to guarantee reliable, ordered delivery.

??? question "2. What do the SYN, ACK, and FIN flags each mean?"
    SYN means "I want to start a connection." ACK means "I received that," used both to confirm the connection and every piece of data afterward. FIN means "I'm done sending, let's close this connection."

??? question "3. Why does opening a connection only take 3 steps, but closing one takes 4?"
    Opening combines the server's acknowledgment and its own SYN into a single SYN+ACK packet, since the server always wants to do both at once. Closing keeps ACK and FIN separate, because the server might still have data left to send after receiving the client's FIN, so it acknowledges immediately but sends its own FIN only once it's actually done.

??? question "4. What does a port number identify, and why is it needed in addition to an IP address?"
    A port identifies which specific application or service on a device a piece of data is meant for. An IP address only gets data to the right device, since one device can run many networked programs at once, sharing the same IP, and the port is what tells that device which specific program should handle it.

??? question "5. Why does a DNS lookup use UDP instead of TCP?"
    A DNS lookup is a single small request and single small response. Paying for a TCP handshake would cost more overhead than the actual query itself, and if a request is lost, it's cheap and fast to just retry the whole lookup rather than needing TCP's reliability guarantees.

??? question "6. Why is UDP preferred for a live video call instead of TCP?"
    A dropped video frame from a second ago is already outdated by the time TCP could detect it's missing and resend it. UDP just skips lost frames and keeps sending new ones in real time, favoring staying current over guaranteeing every frame arrives.

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
DOCS = ROOT / "docs"

# (chapter folder slug, chapter nav title, [(topic title, anchor-free), ...])
STRUCTURE = [
    ("getting-started", "Getting Started", ["What is system design?"]),
    ("chapter-1", "Chapter I", [
        "IP", "OSI Model", "TCP and UDP", "Domain Name System (DNS)",
        "Load Balancing", "Clustering", "Caching",
        "Content Delivery Network (CDN)", "Proxy", "Availability",
        "Scalability", "Storage",
    ]),
    ("chapter-2", "Chapter II", [
        "Databases and DBMS", "SQL databases", "NoSQL databases",
        "SQL vs NoSQL databases", "Database Replication", "Indexes",
        "Normalization and Denormalization",
        "ACID and BASE consistency models", "CAP Theorem",
        "PACELC Theorem", "Transactions", "Distributed Transactions",
        "Sharding", "Consistent Hashing", "Database Federation",
    ]),
    ("chapter-3", "Chapter III", [
        "N-tier architecture", "Message Brokers", "Message Queues",
        "Publish-Subscribe", "Enterprise Service Bus (ESB)",
        "Monoliths and Microservices", "Event-Driven Architecture (EDA)",
        "Event Sourcing",
        "Command and Query Responsibility Segregation (CQRS)",
        "API Gateway", "REST, GraphQL, gRPC",
        "Long polling, WebSockets, Server-Sent Events (SSE)",
    ]),
    ("chapter-4", "Chapter IV", [
        "Geohashing and Quadtrees", "Circuit breaker", "Rate Limiting",
        "Service Discovery", "SLA, SLO, SLI", "Disaster recovery",
        "Virtual Machines (VMs) and Containers",
        "OAuth 2.0 and OpenID Connect (OIDC)", "Single Sign-On (SSO)",
        "SSL, TLS, mTLS",
    ]),
    ("chapter-5", "Chapter V", [
        "System Design Interviews", "URL Shortener", "WhatsApp",
        "Twitter", "Netflix", "Uber",
    ]),
    ("appendix", "Appendix", ["Next Steps", "References"]),
]


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[()]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def main():
    text = README.read_text(encoding="utf-8")
    lines = text.splitlines()

    # find all top-level (H1) header line indices
    h1_positions = []
    for i, line in enumerate(lines):
        if line.startswith("# "):
            h1_positions.append((i, line[2:].strip()))

    # body starts after "Table of contents" H1 (skip title + TOC)
    # keep only h1s after the TOC section
    toc_idx = next(i for i, t in h1_positions if t == "Table of contents")
    body_h1s = [(i, t) for i, t in h1_positions if i > toc_idx]

    sections = {}
    for idx, (line_no, title) in enumerate(body_h1s):
        start = line_no
        end = body_h1s[idx + 1][0] if idx + 1 < len(body_h1s) else len(lines)
        content = "\n".join(lines[start:end]).rstrip() + "\n"
        sections[title] = content

    nav_lines = []
    used_titles = set()
    for folder, chapter_title, topics in STRUCTURE:
        chapter_dir = DOCS / folder
        chapter_dir.mkdir(parents=True, exist_ok=True)
        nav_lines.append(f"  - {chapter_title}:")
        for title in topics:
            if title not in sections:
                raise SystemExit(f"Missing section for topic: {title!r}")
            used_titles.add(title)
            slug = slugify(title)
            out_path = chapter_dir / f"{slug}.md"
            out_path.write_text(sections[title], encoding="utf-8")
            rel = f"{folder}/{slug}.md"
            nav_lines.append(f"      - {title}: {rel}")

    missing = set(sections) - used_titles
    if missing:
        raise SystemExit(f"Unassigned sections: {sorted(missing)}")

    (ROOT / "scripts" / "nav.yml.txt").write_text(
        "\n".join(nav_lines) + "\n", encoding="utf-8"
    )
    print(f"Wrote {len(used_titles)} pages across {len(STRUCTURE)} chapters.")


if __name__ == "__main__":
    main()

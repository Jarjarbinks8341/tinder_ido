# Architecture North Star: High-Throughput Scalable Matching System

> **Note:** The current implementation is an MVP (FastAPI + SQLite, single-service, ~10 users).
> This document captures the target architecture for a production system at 10M DAU scale.
> Use it as a north star when planning future iterations.

---

## 1. Requirements Engineering and Success Metrics

To support a global user base of ten million daily active users (DAU), we must establish rigid functional and non-functional boundaries. At this scale, the interplay between feature set and system performance is a strategic necessity; infrastructure must be provisioned to handle massive write spikes while maintaining sub-second responsiveness. We treat the "No-Repeat" constraint as a hard filter on the feed generation pipeline to prevent UX degradation and state-management bloat.

| Functional Requirements | Non-Functional Requirements |
|---|---|
| **Preference Management:** Users define age range, gender, and distance preferences. | **Latency:** <300ms stack loading. 200–500ms is the threshold for human real-time perception; we target the lower bound. |
| **Stack Viewing:** Location-based profile viewing filtered by preferences and proximity. | **Consistency:** Strong consistency for reciprocal swipes to ensure immediate match detection. |
| **Swiping Mechanics:** Support for rapid binary decisions (Left/Pass vs. Right/Like). | **Throughput:** Handle 10,000 average and 100,000 peak swipes per second (1B+ daily swipes). |
| **Match Notifications:** Real-time alerts (Push/In-app) upon reciprocal "Right" swipes. | **Availability/Scale:** Linear horizontal scaling to support 10M DAU without service interruption. |

The "Repeat Profile" constraint introduces a significant state-management challenge. To avoid showing a user the same profile twice, the system must track billions of historical interactions. We will mitigate this by treating the swipe history as a primary filter in the feed-generation pipeline, transitioning now to the data structures required to support this scale.

---

## 2. Core Entities and API Contract Design

A well-defined API contract is the mandatory foundation for microservice interoperability and security. By defining clear schemas, we prevent IDOR (Insecure Direct Object Reference) vulnerabilities and ensure that independent services can scale without breaking upstream dependencies.

### Three Core Entities

- **Profile:** Stores user metadata, including biographical details and match preferences (age, gender, search radius).
- **Swipe:** Records an individual interaction (User A swiping on User B) and the decision (Yes/No).
- **Match:** A distinct entity generated only when a reciprocal "Yes" swipe is detected between two users.

### API Surface and Security Protocols

All endpoints require a secure JWT or Session Token in the header. To mitigate IDOR vulnerabilities, the `userId` of the requester is never accepted in the request body or path; it is extracted server-side from the Claims of the authenticated token.

- **POST /profiles**
  - Body: `minAge`, `maxAge`, `genderPreference`, `searchRadius`.
  - *So What:* Essential for populating the discovery filter.
- **GET /stacks**
  - Query Params: `lat`, `long`.
  - *So What:* Latitude/Longitude are passed at request time to account for user mobility; the server filters the pre-computed stack based on these coordinates.
- **POST /swipes/{targetUserId}**
  - Body: `decision` (Yes/No).
  - Response: Match object (nullable).
  - *So What:* If the swipe completes a reciprocal match, the Match object is returned immediately to trigger the "It's a Match!" UI.

---

## 3. Distributed Microservices Architecture

The transition from a monolithic to a microservice architecture is required to manage **Load Profile Divergence**. While 10M DAU might update profiles once a week, they generate 1 billion swipes daily. Decoupling these allows us to scale the high-velocity Swipe Service independently of the relatively static Profile Service.

- **API Gateway:** Serves as the centralized entry point. It manages cross-cutting concerns: Authentication, Rate Limiting, and Request Routing.
- **Profile Service:** Manages profile CRUD and preference logic. Optimized for read-heavy preference lookups during stack generation.
- **Swipe Service:** A high-concurrency engine designed to ingest 100k peak writes per second and orchestrate match detection.

By isolating the Swipe Service, we can assign write-optimized resources to handle the 1B daily interactions without over-provisioning the entire system.

---

## 4. High-Throughput Data Persistence Strategy

Strategic database selection must align with the specific read/write intensities of each service.

### PostgreSQL (Profile DB) vs. Cassandra (Swipe DB)

- **PostgreSQL:** Used for profiles where data is structured and relational integrity is paramount. However, at 100k writes/sec, the PostgreSQL write path (Write-Ahead Log → Random I/O for disk-seeking/page updates) becomes a bottleneck.
- **Cassandra:** Selected for the Swipe Service due to its ability to scale linearly, handling massive volumes through its specialized write path.

### Deep-Dive: The Cassandra Write Path

Cassandra's performance is rooted in **Sequential I/O**:

1. **CommitLog:** The write is appended to an on-disk log for durability.
2. **Memtable:** The write is stored in an in-memory sorted structure.
3. **Flush to SSTable:** Periodically, the Memtable is flushed to disk as an Immutable Sorted String Table (SSTable).

This append-only architecture avoids expensive disk seeks, allowing the system to ingest swipes at the speed of the network and memory. However, the eventual consistency of Cassandra requires a dedicated strategy for match fulfillment.

---

## 5. Match Fulfillment and Consistency Logic

The "Match Consistency" problem occurs when two users swipe "Right" simultaneously. In an eventually consistent system, User A's node may not see User B's swipe, potentially "losing" the match. Three architectural patterns address this:

1. **Atomic Distributed Cache (Redis):** A single-threaded Redis cluster for atomic "Check-and-Set" operations. To ensure reciprocal swipes (A→B and B→A) land on the same shard in a partitioned cluster, sort the User IDs (e.g., `minID:maxID`) to form the partition key. This forces serialization and prevents race conditions.
2. **Relational Pessimistic Locking (PostgreSQL):** Use `SELECT FOR UPDATE` logic on a single row representing the pair. Ensures absolute consistency but sacrifices write throughput.
3. **Asynchronous Reconciliation:** A high-availability fallback where a Cron workflow scans Cassandra to identify missed matches.

**Consistency Trade-offs:** Introducing Redis alongside Cassandra creates a "Distributed Transaction" problem. Utilize the **Saga Pattern** or application-level compensation logic to ensure that a match recorded in the cache is eventually persisted in the database. Notifications are dispatched asynchronously via APNs (iOS) and FCM (Android).

---

## 6. Optimized Feed Engineering and Geospatial Indexing

Two-dimensional geospatial queries (Lat/Long) face the **"Hot Spot" problem** in dense urban centers like NYC and the **"Boundary Condition" problem** at state/regional lines. Traditional sharding fails here.

### Specialized Indexing and CDC

Evaluate **PostGIS** vs. **ElasticSearch**. While PostGIS is native to the Profile DB, ElasticSearch is preferred for its search-optimized, horizontally scalable nature. Treat the search index as an eventually consistent projection of the primary Profile DB, synchronized via **Change Data Capture (CDC)** using a stream like Kafka.

### Pre-computed Materialized Views (Stack Cache)

To achieve O(1) lookup times and sub-300ms latency, implement a **Stack Cache**. A background process acts as a "Pre-computation" engine, running complex geospatial and preference queries to populate a user's cache with a "materialized view" of potential matches. When a user requests their stack, they read from a pre-warmed list rather than executing a live, expensive query.

---

## 7. Performance Optimization and Profile Discovery Constraints

At a scale of **36.5 TB of interaction data per year**, maintaining a "No-Repeat" list is a massive memory challenge.

### Probabilistic Structures: Bloom Filters

Use **Bloom Filters** to determine if a user has swiped on a profile. As a space-efficient probabilistic structure, it significantly reduces memory pressure.

- **False Positive Handling:** If the filter says "Yes" (user has swiped), there is a small chance it is lying. Perform a secondary fallback check against the primary Swipe DB to verify before excluding a profile, ensuring viable matches are not skipped unnecessarily.

### Staff-Level Optimization: Swipe TTL

A pragmatic product-technical trade-off: implement a **30 or 60-day Time-To-Live (TTL)** on swipe data. This automatically purges old interaction state, resetting the stack for the user (allowing them to see people they may have passed on months ago) while drastically reducing cache pressure and long-term storage costs.

---

## MVP → North Star Gap Summary

| Concern | Current MVP | North Star |
|---|---|---|
| Database | SQLite (single file) | PostgreSQL (profiles) + Cassandra (swipes) |
| Architecture | Monolith (FastAPI) | Microservices (Profile, Swipe, Gateway) |
| Match detection | Matchmaker placeholder (no reciprocal logic) | Redis atomic Check-and-Set |
| Feed generation | Live SQL query on every request | Pre-computed Stack Cache |
| No-repeat filtering | Not implemented | Bloom Filter + Swipe DB fallback |
| Geospatial search | Not implemented | ElasticSearch + CDC from Postgres |
| Notifications | Not implemented | APNs / FCM async dispatch |
| Swipe TTL | Not implemented | 30–60 day TTL on swipe records |
| Scale target | ~10 users (local dev) | 10M DAU, 1B swipes/day |

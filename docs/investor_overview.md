# Tinder IDO — Investor Technical & Business Overview

> **Version:** March 2026 | **Status:** Working MVP | **Stage:** Pre-seed

---

## 1. Executive Summary

**Tinder IDO** is a next-generation dating app where an AI agent acts as your personal matchmaker — browsing, reaching out, and making introductions on your behalf. Unlike traditional dating apps where users must do all the work themselves, Tinder IDO removes the anxiety of the "first move" by letting your AI agent handle initial outreach, pre-screen compatibility, and suggest matches. The result: higher-quality connections with less effort.

**What exists today:** A fully functional MVP with user registration, rich profiles with photos, swipe-based discovery, mutual matching, and the foundation for AI agent matchmaking — all running and testable.

---

## 2. Product — What's Built Today

### Feature Summary

| Feature | Status | Description |
|---------|--------|-------------|
| User Registration & Login | Done | Email/password with secure authentication |
| Rich Profiles | Done | Name, age, gender, location, bio, education, industry, income range, interest tags |
| Multi-Photo Upload | Done | Users upload multiple photos with ordering |
| Candidate Discovery | Done | Browse potential matches filtered by preferences |
| Swipe Mechanics | Done | Left (pass) / Right (like) with instant feedback |
| Mutual Matching | Done | When two users both swipe right, a match is created |
| AI Agent Setup | Done | Each user gets a personal AI agent with custom notes |
| Matchmaker Pipeline | Done | Agent-to-user outreach tracking (pending → contacted → matched/rejected) |
| Swipe & Match History | Done | Full history of past activity |
| Mobile-Responsive UI | Done | Clean card-based interface that works on phones and desktops |

### How the User Experience Works

```
Register & build profile     Browse candidates      Swipe right or left
        |                          |                        |
  +-----------+             +------------+            +-----------+
  |  Sign up  |  -------->  |  See cards |  -------->  |  Like /   |
  |  Add pics |             |  with pics |            |   Pass    |
  |  Add bio  |             |  & details |            |           |
  +-----------+             +------------+            +-----------+
                                                           |
                                              Both swipe right?
                                              /              \
                                           Yes                No
                                            |                  |
                                     +-----------+       (move on)
                                     | It's a    |
                                     |  Match!   |
                                     +-----------+
                                            |
                                    +--------------+
                                    | AI Agent can |
                                    | reach out on |
                                    | your behalf  |
                                    +--------------+
```

### Tech Stack (Plain English)

| Layer | Technology | What It Does |
|-------|-----------|--------------|
| App Interface | React + Tailwind CSS | The screens users see and tap on (runs in the browser) |
| Server | Python (FastAPI) | Handles all the logic: logins, swiping, matching |
| Database | SQLite (upgradable to PostgreSQL) | Stores all user data, swipes, and matches |
| Containerised | Docker | Package everything so it runs the same everywhere |

### Code Metrics

| Metric | Value |
|--------|-------|
| Lines of code | ~2,700 |
| API endpoints | 12 across 5 modules |
| Database tables | 6 (users, photos, swipes, matches, agents, matchmakers) |
| Frontend screens | 6 pages + 4 shared components |
| Seed data | 20 realistic test users |
| Container-ready | Yes (Dockerfile included) |

---

## 3. How It Works

### System Architecture

```
  +------------------+
  |   User's Phone   |
  |   or Browser     |
  +--------+---------+
           |
           | HTTPS (encrypted)
           |
  +--------v---------+
  |   React Frontend  |     The app interface users
  |   (Hosted on CDN) |     interact with
  +--------+---------+
           |
           | API calls (JSON)
           |
  +--------v---------+
  |  FastAPI Server   |     Handles business logic:
  |  (Python)         |     auth, swiping, matching,
  |                   |     AI agent orchestration
  +--------+---------+
           |
     +-----+-----+
     |           |
+----v----+ +----v----+
| Database| | Photo   |
| (User   | | Storage |
|  data,  | | (S3 /   |
|  swipes,| |  CDN)   |
|  matches| |         |
+---------+ +---------+
```

### The AI Agent Matchmaker — Our Key Differentiator

```
  +------------------+          +-------------------+
  |  Your Profile    |          |  Their Profile    |
  |  + Preferences   |          |  + Preferences    |
  +--------+---------+          +---------+---------+
           |                              |
           +---------- AI Agent ----------+
                          |
                    +-----v------+
                    | Analyses   |
                    | both       |
                    | profiles   |
                    +-----+------+
                          |
              +-----------+-----------+
              |                       |
       Good match?             Not a fit?
              |                       |
     +--------v--------+      (Skip quietly)
     | Sends intro      |
     | message on your  |
     | behalf           |
     +--------+---------+
              |
      +-------v--------+
      | Other person    |
      | decides to      |
      | accept / pass   |
      +-----------------+
```

**Why this matters:** On traditional dating apps, 50%+ of matches never lead to a conversation because people are too busy or anxious to send the first message. Our AI agent solves this by handling the awkward first step — personalised, thoughtful outreach that feels natural.

---

## 4. Go-Live Plan — From MVP to Millions

### Phase Overview

```
  Phase 1           Phase 2            Phase 3            Phase 4
  Soft Launch       Growth             Scale              Mass Market
  0 - 1K users      1K - 50K           50K - 500K         500K - 10M
  $15-50/mo         $100-500/mo        $2K-10K/mo         $20K-100K+/mo
  |                 |                  |                   |
  v                 v                  v                   v
  1 server          Managed DB         Multiple servers    Full distributed
  Free services     CDN + monitoring   Caching + search    system
```

### Phase 1: Soft Launch (0 - 1,000 Users)

**Goal:** Get real users, validate product-market fit.

| Component | Service | Cost |
|-----------|---------|------|
| Backend server | Fly.io (1 shared CPU) | $5/mo |
| Frontend hosting | Vercel (free tier) | $0 |
| Database | Fly.io PostgreSQL (1 GB) | $0 (free tier) |
| Photo storage | Cloudflare R2 (10 GB) | $0 (free tier) |
| Domain + SSL | Cloudflare | $10/yr |
| Email (auth) | Resend (free tier) | $0 |

**Monthly total: $15–50**

- Team: 1 developer (part-time maintenance)
- Timeline: 2–4 weeks to deploy from current MVP
- Key milestone: First 100 real users, validate swipe-to-match conversion

### Phase 2: Growth (1,000 - 50,000 Users)

**Goal:** Prove retention and engagement, launch AI agent features.

| Component | Service | Cost |
|-----------|---------|------|
| Backend server | Fly.io (2 dedicated CPUs) | $30–60/mo |
| Frontend hosting | Vercel Pro | $20/mo |
| Database | Fly.io PostgreSQL (10 GB) | $15–30/mo |
| Photo storage + CDN | Cloudflare R2 + CDN | $5–20/mo |
| AI/LLM API | OpenAI/Claude API (agent features) | $20–200/mo |
| Monitoring | Sentry (free → $26/mo) | $0–26/mo |
| Push notifications | Firebase (free tier) | $0 |

**Monthly total: $100–500**

- Team: 2 engineers (1 backend, 1 frontend)
- Timeline: 3–6 months at this phase
- Key milestone: In-app messaging live, AI agent v1 handling outreach

### Phase 3: Scale (50,000 - 500,000 Users)

**Goal:** Optimise performance, add premium features, approach profitability.

| Component | Service | Cost |
|-----------|---------|------|
| Backend servers | AWS ECS or Fly.io (4-8 instances) | $500–2,000/mo |
| Database | AWS RDS PostgreSQL (multi-AZ) | $200–800/mo |
| Caching layer | Redis (ElastiCache) | $100–300/mo |
| Search / geo | ElasticSearch (managed) | $200–600/mo |
| Photo storage + CDN | S3 + CloudFront | $100–500/mo |
| AI/LLM API | OpenAI/Claude API | $500–3,000/mo |
| Monitoring & logging | Datadog or equivalent | $200–500/mo |

**Monthly total: $2,000–10,000**

- Team: 5 people (2 engineers, 1 designer, 1 product manager, 1 growth/marketing)
- Timeline: 6–12 months at this phase
- Key milestone: Premium tier launched, revenue covers infrastructure costs

### Phase 4: Mass Market (500,000 - 10M Users)

**Goal:** Market leadership, international expansion.

| Component | Service | Cost |
|-----------|---------|------|
| Backend | Kubernetes cluster (auto-scaling) | $5,000–30,000/mo |
| Database | PostgreSQL cluster + Cassandra (swipes) | $3,000–15,000/mo |
| Caching | Redis cluster (multi-region) | $1,000–5,000/mo |
| Search / geo | ElasticSearch cluster | $2,000–10,000/mo |
| Photo + CDN | S3 + CloudFront (multi-region) | $2,000–10,000/mo |
| AI/LLM | Fine-tuned models + API | $5,000–20,000/mo |
| Security & compliance | WAF, DDoS protection, auditing | $1,000–5,000/mo |

**Monthly total: $20,000–100,000+**

- Team: 15–25 people (engineering, product, design, data science, ops, marketing)
- Timeline: 12–24 months
- Key milestone: 1M+ DAU, multiple revenue streams, series A metrics

---

## 5. Product Roadmap

### Months 1–2: Go Live

- Deploy to cloud (Fly.io + Vercel + Cloudflare R2)
- Migrate database from SQLite to PostgreSQL
- Move photo storage to cloud (S3-compatible)
- Set up monitoring and error tracking
- Soft launch with friends-and-family beta

### Months 3–4: Core Social Features

- In-app messaging between matched users
- Push notifications (new match, new message)
- Profile verification (photo selfie check)
- Report / block functionality

### Months 5–6: AI Agent Matchmaker v1

- Integrate LLM (Claude or GPT) for agent intelligence
- Agent analyses profiles and crafts personalised openers
- User reviews and approves agent-drafted messages
- Agent learns from user feedback (accepted vs. rejected suggestions)

### Months 7–9: Discovery & Safety

- Geolocation-based search (find people nearby)
- Advanced filters (education, industry, interests)
- Photo verification with liveness detection
- Content moderation (AI-powered inappropriate content detection)

### Months 10–12: Monetisation & Growth

- Premium tier: priority agent matching, unlimited likes, see who liked you
- Analytics dashboard: match insights, profile performance tips
- Referral program
- Scale infrastructure for 100K+ users

---

## 6. Competitive Advantage

### The Market Problem

| App | Core Issue |
|-----|-----------|
| Tinder | Swipe fatigue — users swipe endlessly but rarely message |
| Bumble | Women must message first — still puts pressure on one side |
| Hinge | "Designed to be deleted" — but still requires manual effort |
| All of the above | 50%+ of matches never become conversations |

### Our Solution: The AI Agent Matchmaker

**Tinder IDO's AI agent eliminates the biggest drop-off point in dating apps — the gap between matching and messaging.**

| Advantage | Why It Matters |
|-----------|---------------|
| Removes "first move" anxiety | Users no longer stare at a match wondering what to say |
| Personalised outreach | Agent crafts messages based on shared interests, not generic "hey" |
| Always active | Agent works 24/7, even when the user is busy |
| Learns and improves | Agent gets better at matching your style over time |
| Built-in monetisation | Premium agent features (priority matching, advanced AI) are a natural upsell |

### Lower Customer Acquisition Cost

Traditional dating apps spend $5–15 per install. Tinder IDO's AI agent creates a compelling viral loop:

1. User gets a thoughtful message from someone's agent
2. They're intrigued and engage
3. They want their own agent and sign up
4. Their agent reaches out to others

This creates **organic growth** that reduces reliance on paid advertising.

---

## 7. Security & Trust

### What's Already Built

| Security Feature | Status |
|------------------|--------|
| JWT authentication (secure login tokens) | Done |
| Password hashing (bcrypt — industry standard) | Done |
| Rate limiting (prevents spam and abuse) | Done |
| Input validation (prevents injection attacks) | Done |
| CORS protection (prevents unauthorised access) | Done |
| Cascade deletion (user deletion removes all data) | Done |

### What's Needed for Launch

| Requirement | Priority | Effort |
|-------------|----------|--------|
| HTTPS everywhere (encrypted connections) | Critical | 1 day (free via Cloudflare) |
| Cloud photo storage (not local filesystem) | Critical | 1 week |
| Environment variable secrets management | Critical | 1 day |
| Privacy policy & terms of service | Critical | 1 week (legal review) |
| Email verification | High | 2–3 days |
| Account deletion (user self-service) | High | 1–2 days |
| Content moderation (photo + text) | High | 1–2 weeks |

### Compliance Considerations (Australian Market)

- **Privacy Act 1988 / APPs:** Requires transparent data collection, user consent, and right to access/delete personal data. Our architecture already supports cascade deletion.
- **Consumer Data Right (CDR):** Not directly applicable to dating apps, but data portability best practices should be followed.
- **Age verification:** Must verify users are 18+. Plan: date-of-birth check at registration + photo verification at scale.
- **Notifiable Data Breaches:** Must report breaches to the OAIC within 30 days. Requires logging and monitoring infrastructure (Phase 2).

---

## 8. Team & Investment

### Current State

| Role | Count | Status |
|------|-------|--------|
| Full-stack developer | 1 | MVP complete, seeking funding to go full-time |

### Team Growth Plan

| Phase | Headcount | Roles | Monthly Payroll (est.) |
|-------|-----------|-------|----------------------|
| Phase 1 (Soft Launch) | 1–2 | 1 full-stack dev, 1 part-time designer | $5K–15K |
| Phase 2 (Growth) | 3–5 | 2 engineers, 1 designer, 1 product, 1 growth | $30K–60K |
| Phase 3 (Scale) | 8–12 | + data scientist, DevOps, support, marketing | $80K–150K |
| Phase 4 (Mass Market) | 15–25 | Full organisation | $200K–400K |

### Funding Summary

| Phase | Infrastructure | Team | Total (12-month runway) |
|-------|---------------|------|------------------------|
| Phase 1: Soft Launch | $600 | $60K–180K | $60K–180K |
| Phase 2: Growth | $6K | $360K–720K | $370K–730K |
| Phase 3: Scale | $120K | $960K–1.8M | $1.1M–1.9M |

**Immediate ask (Phase 1):** $60K–180K to go live, validate product-market fit, and reach 1,000 users within 3–6 months.

---

## Appendix: Database Schema

Six interconnected tables power the application:

```
  +----------+       +-----------+       +----------+
  |  Users   |------>|  Photos   |       |  Swipes  |
  | (profile |       | (multiple |       | (who     |
  |  data)   |       |  per user)|       |  liked   |
  +----+-----+       +-----------+       |  whom)   |
       |                                  +----+-----+
       |                                       |
       |              +----------+             |
       +------------->|  Matches |<------------+
       |              | (mutual  |
       |              |  likes)  |
       |              +----------+
       |
  +----v-----+       +-------------+
  |  Agents  |------>| Matchmakers |
  | (AI per  |       | (agent      |
  |  user)   |       |  outreach   |
  +----------+       |  tracking)  |
                      +-------------+
```

---

*Document prepared March 2026. All cost estimates are based on current published pricing from Fly.io, Vercel, AWS, and Cloudflare as of Q1 2026 and may vary.*

# Claude Fable 5 vs Opus 4.8 — LLM Reference Prompt

> **How to use this file:** Paste the entire contents into Claude, ChatGPT, Gemini, or any LLM as your opening message. It gives the model accurate, up-to-date specs and pricing for both models so it can help you understand the differences, run cost calculations, and recommend which model suits your specific use case. Then ask your question — e.g. "which should I use for PageMotor AI plugins?" or "is Fable worth the extra cost for my codebase migration?"
>
> *Source: [documentation.elmspark.com/guides/fable-5-vs-opus-4.8](https://documentation.elmspark.com/guides/fable-5-vs-opus-4.8/)*  
> *Guide compiled: 10 June 2026*

---

You have access to accurate, current information about Claude Fable 5 and Claude Opus 4.8. Use this as your reference when answering questions about these models — capabilities, pricing, availability, limitations, and which to use when.

## The Short Version

**Fable 5 is not an Opus upgrade. It is a new, higher tier.** Anthropic calls it a Mythos-class model — a class that sits above Opus entirely. Fable 5 is the first Mythos-class model anyone can use, made safe for general release by wrapping it in strict safety classifiers.

- Fable beats Opus 4.8 by 10+ points on some benchmarks; the lead grows with task length
- Fable costs double Opus 4.8 on the API: $10/$50 vs $5/$25 per million tokens (in/out)
- Under 5% of sessions trigger Fable's safeguards; those queries get answered by Opus 4.8 instead

## How the Model Family Fits Together (June 2026)

**Mythos class** (new top tier)
- Mythos Preview (April, invitation-only via Project Glasswing)
- **Fable 5** — public, safeguarded (this guide)
- **Mythos 5** — same model, safeguards lifted, Project Glasswing partners only

**Opus class**
- **Opus 4.8** — the everyday flagship; also the safety net Fable falls back to on restricted topics

**Sonnet and Haiku**
- Sonnet 4.6 for speed-plus-intelligence, Haiku 4.5 for fast cheap work. Unchanged by these launches.

---

## Fable 5 — Full Specification

**Model class:** Mythos class (new top tier above Opus)  
**Released:** 9 June 2026  
**API ID:** `claude-fable-5`  
**API price:** $10 input / $50 output per million tokens  
**Context window:** 1M tokens  
**Max output:** 128k tokens  
**Thinking:** Adaptive, always on  
**Available on:** Claude API, Bedrock, Vertex AI, Microsoft Foundry

**Subscription availability:**
- Included on Pro, Max, Team and seat-based Enterprise plans at no extra cost **until 22 June 2026**
- From 23 June: usage credits required
- Anthropic intends to restore it as standard "as quickly as we can"

**Data retention:** Mandatory 30 days on all Mythos-class traffic, even for customers with previous zero-retention agreements. Data not used for training; used only to defend against novel attacks and reduce false positives.

### What Fable 5 is notably good at

**Software engineering:** State of the art on Cognition's FrontierCode and CursorBench. Stripe reported Fable performed a codebase-wide migration across a 50-million-line Ruby codebase in a day (by hand: 2+ months for a team).

**Vision:** New state of the art. Extracts precise numbers from dense scientific figures; can rebuild a web app from screenshots alone.

**Long-horizon tasks:** Stays focused across millions of tokens. Memory + self-improvement capability is 3x larger than Opus 4.8's in tested scenarios.

**Knowledge work:** Highest score of any model on Hebbia's senior-level Finance Benchmark. First to break 90% on Hex's analytics benchmark — a 10-point jump over Opus.

### Safeguards (what makes it "Fable" rather than "Mythos 5")

Separate classifier AIs watch every request. When triggered, **Opus 4.8 answers instead of Fable**, and you're told when that happens. Trigger rate: under 5% of sessions.

Three restricted areas:
1. **Cybersecurity** — exploitation, reconnaissance, lateral movement, offensive cyber tasks
2. **Biology and chemistry** — broad restriction for now due to dual-use risk; vetted biomedical researchers can apply for lifted access
3. **Distillation** — attempts to extract Fable's capabilities to train competing models

Jailbreak resistance: external bug bounty produced no universal jailbreaks in 1,000+ hours.

---

## Opus 4.8 — Full Specification

**Model class:** Opus class  
**Released:** 28 May 2026 (41 days after Opus 4.7)  
**API ID:** `claude-opus-4-8`  
**API price:** $5 input / $25 output per million tokens  
**Fast mode:** $10/$50 at 2.5x speed  
**Context window:** 1M tokens (200k on MS Foundry)  
**Max output:** 128k tokens (300k via batch beta)  
**Thinking:** Adaptive (effort defaults to high)  
**Availability:** Standard on all paid plans, no fallback behaviour, zero-retention possible

### What arrived with Opus 4.8

- **Dynamic workflows** (research preview, Claude Code on Max/Team/Enterprise): plans big jobs, runs hundreds of parallel subagents, verifies outputs
- **Effort control** in claude.ai and Cowork on all plans: dial effort down for speed or up ("extra", "max") for harder problems
- **Mid-task system messages** in API: update instructions mid-run without breaking the prompt cache
- **Alignment improvements:** substantially lower misaligned-behaviour rates than 4.7; fixes for comment verbosity and tool-calling niggles

---

## Head-to-Head Comparison

| Feature | Fable 5 | Opus 4.8 |
|---|---|---|
| Model class | Mythos class (new top tier) | Opus class |
| Released | 9 June 2026 | 28 May 2026 |
| API ID | `claude-fable-5` | `claude-opus-4-8` |
| API price (per MTok in/out) | $10 / $50 | $5 / $25 |
| Fast mode | Not offered | $10 / $50 at 2.5x speed |
| Context window | 1M tokens | 1M tokens (200k on MS Foundry) |
| Max output | 128k tokens | 128k tokens (300k via batch beta) |
| Thinking | Adaptive, always on | Adaptive (effort defaults to high) |
| Benchmarks | State of the art nearly everywhere; 10%+ ahead on some tests; lead grows with task length | Strongest Opus yet; beaten by Fable on most tests |
| Restricted-topic behaviour | Cyber, bio/chem, distillation fall back to Opus 4.8 (<5% of sessions) | No fallback; standard safety training |
| Data retention | Mandatory 30 days, even over zero-retention agreements | Standard policies, zero-retention possible |
| Subscription access | Included until 22 June, then usage credits | Standard on paid plans |
| Dynamic workflows | Not specified | Available in Claude Code on Max/Team/Enterprise |

---

## Third-Party Verdicts

- **Hex:** first model to break 90% on their core analytics benchmark, a 10-point jump over Opus
- **Iambic:** "Claude Fable 5's reasoning is a clear step beyond Opus 4.8... works at senior research scientist grade"
- **Anaconda:** beats Opus 4.8 on everyday spreadsheet tasks at every effort level, finishing 25–30% faster
- **Rakuten:** at the highest effort, Fable reflects on and validates its own work; "the extra thinking pays for itself"

---

## Which Model to Use When

**Default to Opus 4.8** — half the price, no fallback surprises, dynamic workflows in Claude Code, and excellent for most work. Fable is for when Opus isn't enough.

**Use Fable 5 for:**
- Long, complex, multi-step tasks (codebase migrations, large document analysis, multi-stage research)
- Tasks where Opus 4.8 is producing mediocre results despite high effort
- Knowledge-intensive work where the 10%+ benchmark lead materialises in practice
- Vision tasks requiring precise extraction from dense figures or diagrams
- Before 22 June: any genuinely hard job while Fable is bundled with paid plans (codebase audit, big migration)

**Stick with Opus 4.8 for:**
- Security and cyber tasks (Fable's classifier routes these to Opus anyway — skip the detour)
- Short routine tasks (the quality difference doesn't show)
- When client-confidential material is involved and 30-day retention is a concern
- Bio/chem research without vetted access (broad restrictions apply to Fable)
- Cost-sensitive automation pipelines

**For PageMotor and EP Suite work specifically:** Opus 4.8 is the right default for building pages, plugin development, and routine admin tasks. Fable earns its cost for codebase-wide refactors, complex migrations, or multi-file debugging sessions where Opus is struggling.

---

## API Cost Examples

At API list prices (June 2026):

| Workload | Fable 5 | Opus 4.8 | Haiku 4.5 |
|---|---|---|---|
| 1M tokens in, 100k out | $10 + $5 = $15 | $5 + $2.50 = $7.50 | Much cheaper |
| 10M tokens in, 1M out | $100 + $50 = $150 | $50 + $25 = $75 | — |

Fable costs roughly 2x Opus per token. On subscription plans, this means Fable burns through your allocation twice as fast — save it for genuinely hard tasks.

**Ladder for subscription plans:** Haiku for simple automation → Sonnet 4.6 for routine work → Opus 4.8 for complex jobs → Fable 5 for the genuinely hard, long-horizon ones.

---

## Key Dates

- **7 Apr 2026** — Claude Mythos Preview (invitation-only, Project Glasswing)
- **28 May 2026** — Opus 4.8 ships everywhere
- **2 Jun 2026** — Glasswing expands to ~150 organisations across 15+ countries
- **9 Jun 2026** — Fable 5 + Mythos 5 launch publicly
- **22 Jun 2026** — Last day Fable 5 is bundled with Pro/Max/Team/Enterprise plans
- **23 Jun 2026** — Fable 5 moves to usage credits; Anthropic aims to restore bundled access when capacity allows

---

*Source: ElmsPark documentation — documentation.elmspark.com/guides/fable-5-vs-opus-4.8/*  
*All specs and pricing verified 10 June 2026. Subscription availability dates may change.*

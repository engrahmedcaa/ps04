# Problem Set 4 Student Submission Guide

This document is a work plan, not a claim that publication or live runs have already happened. Replace each `TO COMPLETE` item with evidence after you perform the step.

## Chosen project (use consistently throughout the assignment)

- **Publication name:** Small-Team Agent Field Notes
- **Topic:** Agent tools and frameworks for real-world AI applications
- **Audience:** AI application developers at small teams who build and maintain production software with limited time for infrastructure and evaluation
- **Central question:** Which recently released agent tools and frameworks are ready for real-world use by small teams, and what should developers test before adopting them?
- **Scope:** Agent frameworks, tool calling, orchestration, evaluation, reliability, security, deployment, cost, and developer workflow; prioritize original evidence published within the 30-day window.
- **Exclusions:** Generic AI news with no concrete implications for building or operating agents; demos or vendor benchmarks presented as proof of production readiness; reposts and undated material.
- **Reason to return:** Developers need a concise, evidence-traceable update that helps them decide what changed, what claims hold up, and what to test before adoption.

The three pieces keep one audience and topic but answer different questions: (01) what changed and matters, (02) which readiness claims withstand scrutiny, and (03) what a small team should test or watch next.

## Run guide

1. Install Git Bash (or Bash), Python 3.10+, `yt-dlp` (`python -m pip install yt-dlp`), and `ffmpeg` if needed. Confirm `bash --version`, `python --version`, and `yt-dlp --version`.
2. Edit `config/project.json` for your chosen publication, topic, audience, and question.
3. Configure at least six independent real source publishers in `config/sources.json`: at least two RSS publishers, two YouTube sources, and two podcast sources, with at least two eligible substantive items per kind. Resolve duplicate podcast/video copies as one underlying item.
4. Verify the starting sources, dates, and independence. Set `OPENAI_API_KEY` in the environment before a live run; `OPENAI_MODEL` defaults to `gpt-5-mini` and `OPENAI_TRANSCRIPTION_MODEL` defaults to `whisper-1`. Requests may incur charges. Never commit secrets.
5. Run `bash run.sh` from this directory. Inspect `runs/RUN_ID/summary.json`, receipts, exclusions, extracted text, and `data/evidence/index.json`. Fix failed or incomplete collection honestly.
6. A full run must complete on a second calendar day. Use `bash run.sh` again. Compare `changes.jsonl`, `decisions.jsonl`, `summary.json`, and receipts; optionally replay unchanged inputs with `bash run.sh --replay PATH_TO_CANDIDATES.jsonl`.
7. Inspect at least three accepted and three rejected/deferred decisions. Use [MODEL_EVALUATION.md](MODEL_EVALUATION.md) and `evaluation/human_labels.csv` to compare model decisions with your labels. Revise `config/editorial_policy.md`, rerun the same frozen item set into separate before/after outputs, and document the effects and factual corrections.
8. Complete and fact-check three distinct 600–900 word articles and three matching 3–5 minute scripts. Confirm every claim has passage/timestamp evidence from at least three independent sources per piece, with all three input types represented across the series.
9. Review `review.json`. The student must create `approval.json` only after reviewing the actual material, with the current `review_id`, decision `approve`, reviewer name, UTC timestamp, and notes. Then run `bash run.sh --package runs/RUN_ID`.
10. Use Google Vids or HeyGen to render each audience-facing video. Publish the articles on Substack without a paywall and the videos publicly or unlisted on YouTube. Add article/video links in descriptions and `package/publication_links.json`; verify course staff access.
11. Record the separate 4–6 minute technical demonstration, including architecture, a traced claim, second run, duplicate/failure behavior, policy revision, correction, and tradeoff.
12. Fill the tables below with actual links, dates, logs, costs, and review notes. Submit the repository to GitHub with no credentials.

## Entry commands

```bash
# Live collection and pipeline run
bash run.sh

# Explicitly fictional fixture demonstration only
bash run.sh --fixture examples/candidates.jsonl

# Reprocess a fixture as a replay; not a second live run
bash run.sh --replay examples/candidates.jsonl

# Resume AI/editorial generation from saved evidence without re-downloading
bash run.sh --resume runs/RUN_ID

# Package only after human approval matches the current review fingerprint
bash run.sh --package runs/RUN_ID
```

The live collector and OpenAI adapters have been exercised in the saved live run. It collected 13 items and completed selection, but brief generation hit the provider context limit. Fixture output is deterministic scaffolding, not model performance. Follow `MODEL_EVALUATION.md` for evaluation. Drafts need human fact-checking and approval. Repair review errors and assess warnings.

## Requirement-by-requirement checklist

| Assignment requirement | Project location / evidence to provide | Completion state |
|---|---|---|
| Supplied directory structure and 16 Bash components | `run.sh`, `workflows/`, `collectors/`, `processing/`, `data/`, `editorial/`, `content/`, `review/`, `publishing/`, `reporting/` | Local entry points exist; verify each on a Bash-capable machine |
| Keep course instructions and contracts | `README.md`, `ARCHITECTURE.md` | Preserved from starter |
| Topic, audience, purpose, voice | `config/project.json`, `config/editorial_policy.md`, and this section | Chosen topic/audience are configured; confirm before live collection |
| All three input types and at least 12 recent substantive items, 6 independent publishers | `config/sources.json`, candidates/items and coverage summary | Latest saved live run has 13 extracted items across all three kinds and six publishers; the resumed run excludes three old fictional fixtures before selection |
| Date window and actual as-of date | `run.json`, `eligible.jsonl`, `exclusions.jsonl` | Filter implemented; verify live run |
| Claim-level credibility, policy, prompts, structured decisions | `config/editorial_policy.md`, `prompts/`, `decisions.jsonl` | Tailored policy/prompts present; model provider and human review remain |
| Three distinct, evidence-grounded arguments | `briefs.jsonl` | Latest run reached selection but brief generation exceeded the model context window; resume with compact evidence, then fact-check and synthesize |
| Three 600–900 word Substack articles and matching videos/scripts | `articles/`, `video_scripts/`, publication links | Not complete; draft scaffolds require human writing, Vids/HeyGen, and publication |
| Three accepted and three rejected/deferred reviews; policy revision | `evaluation/`, `MODEL_EVALUATION.md`, `decisions.jsonl`, revision history | Rubric/template provided; human comparison and policy revision remain after the recorded live run |
| Repeatability on different days, duplicate handling, failure/recovery | two live `runs/` directories, `changes.jsonl`, receipts | Not complete; fixture replay does not count |
| Review, human approval, packaging | `review.json`, `approval.json`, `package/` | Fingerprint/approval gate implemented; human decision must be supplied |
| Separate 4–6 minute technical demo | video URL below | Not complete |
| GitHub repository and accurate submission | repository URL | Not complete |

## Student publication details

| Piece | Title | Substack article | YouTube video |
|---|---|---|---|
| 1 | TO COMPLETE | TO COMPLETE | TO COMPLETE |
| 2 | TO COMPLETE | TO COMPLETE | TO COMPLETE |
| 3 | TO COMPLETE | TO COMPLETE | TO COMPLETE |

- **Technical demonstration video:** TO COMPLETE
- **GitHub repository:** TO COMPLETE

## Evidence and two live runs

| Run | Actual date | Artifacts/logs | Elapsed time | Approximate cost |
|---|---|---|---|---|
| First live run | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE |
| Second live run (different date) | TO COMPLETE | TO COMPLETE | TO COMPLETE | TO COMPLETE |

Explain the new/changed/unchanged counts, date exclusions, failure/recovery, duplicate reconciliation, unknown costs, and changes to editorial choices. Label any fictional fixture/replay or simulated failure. Link retained text/transcripts and state how omitted media can be retrieved.

## Editorial review and reflection

Document three accepted and three rejected/deferred decisions and whether you agree, with passage-level reasons. Show policy before/after and affected decisions or synthesis. Record human factual corrections and why they were necessary. Trace one published claim through brief → decision → versioned source → exact quote or timestamp.

- **One insight produced:** TO COMPLETE
- **One editorial failure or limitation:** TO COMPLETE
- **Next improvement:** TO COMPLETE
- **Architectural tradeoff and rationale:** TO COMPLETE



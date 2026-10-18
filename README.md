# Intelligence Pipeline implementation

This project is a local implementation scaffold for MIT 1.125 Problem Set 4. It preserves the supplied architecture and interfaces. Bash files are component entry points; `scripts/pipeline.py` implements orchestration and local processing. The built-in baseline deliberately refuses to create a publishable series from below the assignment minimum of 12 eligible items from six publishers (at least two per input type) and labels generated drafts as scaffolds. It does not claim that a local run completed publication or human editorial review.

Start with [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for a beginner explanation of the workflow, run output, and how to check each requirement. The chosen audience and topic are recorded in `config/project.json`. The AI-model evaluation procedure is in [MODEL_EVALUATION.md](MODEL_EVALUATION.md). The OpenAI adapter has been used in a live run; that run collected evidence and completed selection, but brief generation exceeded the model context window.

## Requirements

- Windows with Git Bash or Linux/macOS with Bash 4+.
- Python 3.10+ (standard library).
- `yt-dlp` for public YouTube channel discovery and audio download (`python -m pip install yt-dlp`); audio conversion may also require `ffmpeg` on PATH.
- An OpenAI API key in `OPENAI_API_KEY` for model calls and audio transcription. Default text model: `gpt-5-mini` (override with `OPENAI_MODEL`); default audio transcription model: `whisper-1` (override with `OPENAI_TRANSCRIPTION_MODEL`).
- API requests and transcription may incur charges; check availability and pricing in your provider account before live runs. Never commit credentials.
- The fixture uses no API calls. Live model/transcription use requires the key and can incur charges.

## Configure

Review the configured topic, policy, prompts, and nine initial source endpoints. They include commercial provider/framework updates, an independent agent-evaluation research organization, and practitioner podcasts. Verify the sources are active and on-topic before relying on collected items; replace any unavailable or unsuitable sources. `config/discovery.json` screens out undated, older-than-30-day, and off-topic entries before downloading full text/audio, scans at most 20 YouTube metadata entries per channel, and keeps no more than two candidates per configured source. That is at most 18 full candidates across the nine sources. The assignment requires at least 12 distinct eligible items from six independent publishers and at least two per input type; the cap is a bounded starting point, and increase it if source failures or duplicates leave the run below those minimums. The assignment says collecting more by itself does not improve the grade. `examples/` is fictional and never counts as evidence. Keep credentials in environment variables and do not commit them.

RSS/podcast feed collection is implemented. YouTube discovery/audio retrieval uses `yt-dlp`; audio transcription uses the configured OpenAI endpoint and requires the API key. Audio over 24 MB is split into four-minute chunks with `ffmpeg`, with timestamps offset back to the original recording. Do not count a podcast and its YouTube copy twice.

## Run

From this directory:

```bash
bash run.sh
```

Set `OPENAI_API_KEY` in the current Git Bash session, then run this command. It creates `runs/RUN_ID/`, snapshots config and prompts, collects sources, stores evidence versions, filters the inclusive UTC 30-day window, calls the model for decisions/briefs/drafts, runs review checks, and writes a summary. Model and transcription requests can incur charges. A run with insufficient evidence or missing tools/credentials is reported as failed; it must not fabricate content.

The pipeline now prints timestamped progress updates to Git Bash as it runs. You will see the current stage, source ID and URL, counts, and AI/transcription requests. Slow network and external-tool waits print a heartbeat every 10 seconds. These messages go to stderr, so the JSON results and stage-to-stage data remain usable. If you press Ctrl+C, it reports which operation was interrupted.

Before a live run, the launcher checks that `OPENAI_API_KEY` and `yt-dlp` are available. If either is missing, it stops immediately with a setup message instead of spending time scanning feeds first. Fixture and replay modes do not require either prerequisite.
If a live run collected evidence but failed during AI brief/draft generation, reuse that evidence without downloading or transcribing it again:

```bash
read -rsp "OpenAI API key: " OPENAI_API_KEY; printf '\n'; export OPENAI_API_KEY
bash run.sh --resume runs/RUN_ID
```

`--resume` starts a new auditable run from saved evidence. It excludes fictional fixture records and reuses saved editorial decisions only when every item ID and version exactly matches the filtered live corpus; otherwise it repeats selection. Brief generation sends short relevant passages and selected transcript segments rather than full transcripts, and retries once with smaller excerpts if the provider still reports a context-window error. Each brief is checked for three independent publishers and resolvable exact text/segment citations. Draft length checks enforce 600–900 words per article and 450–700 words per video script. Human fact-checking, approval, video rendering, and publication remain required after generated drafts pass review.

In Git Bash, install the YouTube helper once and enter the API key without placing it in your shell command history:

```bash
python -m pip install yt-dlp
read -rsp "OpenAI API key: " key; printf '\n'; export OPENAI_API_KEY="$key"; unset key
bash run.sh
```

The key is kept only in that Git Bash session. ChatGPT subscriptions and API billing are separate; use an API key/account with billing enabled. You can first run fixture mode without a key to check local plumbing.

To inspect the interface using only fictional fixtures:

```bash
bash run.sh --fixture examples/candidates.jsonl
```

The fixture is labeled `example`, uses fictional domains, does not call the model, and does not satisfy any live evidence or publication requirement. Replay the same fixture with `bash run.sh --replay examples/candidates.jsonl` to inspect idempotent storage behavior.

Stage interfaces are available through each required `*.sh` entry point. All paths passed in records are repository-relative. Records use JSONL; diagnostics go to stderr. Store commands:

```bash
bash data/store.sh init
bash data/store.sh list
bash data/store.sh get ITEM_ID
bash data/store.sh upsert RUN_DIR < items.jsonl
```

Package only after reviewing the actual material and creating a matching `approval.json` yourself:

```bash
bash run.sh --package runs/RUN_ID
```

The package step checks the current review fingerprint and matching approval; it does not publish anything. You must populate publication links after publication.

## Outputs and requirement map

- Sixteen required Bash entry points: each is present under the supplied component path and delegates only to its matching stage.
- Collection and all three input types: RSS and podcast feeds; bounded YouTube discovery/audio through `yt-dlp`; timestamped transcription through OpenAI. Freshness and topical screening occurs before full text/media retrieval. `runs/RUN_ID/discovery_screening.json` records the as-of date, cap, counts, and examples of items screened out. Missing requirements fail visibly.
- Evidence and replay: `data/store.sh` is the sole writer of `data/evidence/index.json`; records carry stable IDs, content versions, run IDs, and change status.
- Freshness: `processing/filter_items.sh` checks the inclusive 30 calendar dates ending on `run.json`'s actual UTC as-of date and records exclusion reasons.
- Editorial policy and prompts: `config/` and `prompts/` are copied to each run snapshot.
- Three articles/scripts and evidence trace: generated only when enough eligible inputs exist; baseline outputs are scaffolds, not publication-ready content.
- Checks and handoff: `review/check_content.sh` fingerprints drafts/evidence and flags missing evidence, source coverage, artifacts, or short drafts. `publishing/prepare_package.sh` requires a human approval matching that fingerprint.
- Repeatability and publication: two live runs on different days, human review, video production, account publishing, and real links remain the student's actions. The program will not claim those happened before they do.

See `ARCHITECTURE.md` for all record contracts and `SUBMISSION.md` for a step-by-step completion checklist.

### Git Bash troubleshooting

If `bash run.sh` says `python: command not found`, install Python 3.10 or newer and reopen Git Bash so its PATH refreshes. Confirm `python --version` prints a version. If Python is installed in a custom folder, set `PYTHON_BIN` to the executable path before running. The launcher reports this prerequisite clearly.



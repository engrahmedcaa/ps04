# Beginner guide: what this project does and how to use it

## 1. The project in one picture

Think of the project like a tiny research newsroom with stations on an assembly line:

```text
recent articles + YouTube + podcasts
                ↓
       collect and read them
                ↓
    check dates and duplicates
                ↓
  decide what is worth reporting
                ↓
 make 3 arguments → article + video script for each
                ↓
       you review and approve
                ↓
  publish, then run again another day
```

Each folder is a station, and each required `.sh` file is its station's start button. Bash connects the stations. `scripts/pipeline.py` implements orchestration using Python's standard library. Live YouTube discovery uses `yt-dlp`; model and transcription calls use the configured OpenAI API. You do not need Node.js.

## 2. The one topic and audience we chose

- **Publication:** Small-Team Agent Field Notes
- **Audience:** AI application developers at small teams.
- **Topic:** Agent tools and frameworks for real-world AI applications.
- **Main question:** Which recently released agent tools and frameworks are ready for real-world use by small teams, and what should developers test before adopting them?

The assignment wants **one** audience and **one** topic for the whole project. It wants **three connected articles**, not three audiences: (01) what changed and matters; (02) which claims withstand scrutiny; (03) what a small team should test or watch next. Each article gets a companion video.

## 3. What the important words mean

- **Source:** An article, video, podcast episode, research report, or other original material.
- **Publisher:** The organization or person that produced that source. Six copies of one announcement are still one underlying claim, not six independent publishers.
- **Candidate:** A discovered source record, before its full text/transcript is processed.
- **Evidence item:** A candidate with retained article text or transcript segments and a stable version ID.
- **Eligible:** Evidence dated within the 30 calendar days ending on the run's as-of date. Undated, future, or too-old items are excluded with a reason.
- **Decision:** The editorial AI/human labels an eligible item accept, reject, or defer, and explains why.
- **Brief:** A short plan for one article's central argument, claims, evidence, and limitations.
- **Run:** One dated execution. Its `runs/RUN_ID/` folder preserves the inputs and outputs so you can inspect what happened.
- **Replay:** Running previously seen records again to check whether the store detects them as unchanged. Replay is useful practice; it does not count as a second live run on a different day.

## 4. What is implemented today

The program can create dated run folders and configuration snapshots, read fixture records, save evidence text/transcripts, calculate version IDs, record new/changed/unchanged items, apply the 30-day date filter, summarize coverage, collect configured feeds, call a configured model, and stop with a clear explanation when evidence, tools, or credentials are missing.

The `*.sh` scripts are the required Bash entry points. Python 3.10+ is required. Install `yt-dlp` with `python -m pip install yt-dlp`; audio conversion may require `ffmpeg`. Set `OPENAI_API_KEY` for AI and transcription requests. API calls can incur charges.

While a live run works, Git Bash prints timestamped progress: current phase, each source URL, article extraction, audio download/transcription, and model requests. Slow network and external-tool waits print a heartbeat every 10 seconds. Progress uses the diagnostic stream so the pipeline's JSON records remain intact. If you press Ctrl+C, the program identifies which operation was interrupted.

### What still needs your participation

No API key is present in this workspace, so live model calls and transcription have not been run. Fixture mode remains deterministic and is not a model evaluation. You still need to verify source items, inspect model outputs, edit drafts, personally approve, publish, and complete a second live run on another day. A successful fixture test is not proof those assignment outcomes are complete.

The code must not invent sources or claim unpublished work is published.

## 5. Run the safe practice example

Open Git Bash in the `intelligence-pipeline` folder and run:

```bash
bash run.sh --fixture examples/candidates.jsonl
```

The output includes a `run_id`, for example `run-...`. Find that exact folder under `runs/`. The supplied fixture has three fictional items, one per input type. It is expected to end with `status: failed` and a message like `Evidence minimum not met: 3/12 ...`. That means the software correctly refused to pretend the examples meet the assignment. It is not a live-source failure.

Run the same fixture again:

```bash
bash run.sh --replay examples/candidates.jsonl
```

Look for `unchanged: 3`. This demonstrates duplicate/replay behavior in the sample store, not the required two-live-run demonstration.

## 6. What the real assignment run needs

Before a live run can reach the writing stages, collect at least:

- 12 distinct, substantive, date-verified items;
- 6 independent publishers;
- at least 2 RSS written items, 2 distinct YouTube items, and 2 distinct podcast items;
- all substantive sources published within 30 days of that run's actual date;
- timestamped passages for video and podcast evidence;
- duplicate reconciliation, especially if one podcast is also uploaded to YouTube.

Plan for a mix of perspectives: framework/provider documentation and announcements, independent technical evaluation/research, and practitioner experience. Vendor statements can be important evidence of what was released, but by themselves they do not prove production reliability. Record why publishers count as independent and which perspectives are missing.

`config/sources.json` contains nine starting endpoints: provider/framework blogs and channels, an independent evaluation research blog, and two developer podcasts. Verify that each is accessible and yields relevant current items; replace any unsuitable source. The list is a starting point, not proof that every item is recent, relevant, independent, or successfully collected.

To avoid downloading years of archive pages or entire channels, `config/discovery.json` screens metadata first: it keeps only the prior 30 days, applies agent-development topic terms, scans no more than 20 YouTube entries per channel, and processes at most two items per configured source. The maximum starting batch is 18 candidates. The assignment's minimum is 12 distinct items from six independent sources, with at least two per input type; if screening or source failures leave the run below that, inspect `runs/RUN_ID/discovery_screening.json` and carefully add/adjust sources or the per-source cap. More items alone do not improve the grade. The screening report records counts and examples for out-of-window, undated, off-topic, and over-cap entries.

## 7. How to read the run folder

| File/folder | Plain-language meaning |
|---|---|
| `run.json` | Run ID, actual start time, as-of date, mode, and prior run. |
| `config/`, `prompts/` | Copies of the exact settings and instructions used for that run. |
| `candidates/`, `candidates.jsonl` | Discovered source listings, split by required kind and combined. |
| `items.jsonl` | Successfully read evidence records and paths to retained text/transcripts. |
| `changes.jsonl` | Whether each item was new, changed, or unchanged relative to the index. |
| `corpus.jsonl` | Latest stored version of every known item. |
| `eligible.jsonl`, `exclusions.jsonl` | Date-window results and reasons for exclusion. |
| `decisions.jsonl` | Accept/reject/defer decisions and reasons (after selection is implemented/configured). |
| `briefs.jsonl` | The three article arguments and their evidence references. |
| `articles/`, `video_scripts/` | Drafts, not automatically publication-ready. |
| `review.json` | Mechanical checks and issues for human review. |
| `approval.json` | Your human approval decision; never generated automatically as if you reviewed the content. |
| `logs/` | One receipt per executed stage, including counts, time, tools, cost, and errors. |
| `summary.json` | Overall counts, coverage, failures, and remaining work. |

JSONL means “one JSON record per line.” You can open these files in a text editor. If a stage did not run, its file may be absent; the summary should explain why.

## 8. How to check whether the work meets the assignment

Do not judge by whether the command printed JSON alone. For every real run, check:

1. `run.json` has the actual UTC execution date; its `as_of_date` matches that run.
2. `summary.json` shows at least 12 eligible distinct items, at least six genuinely independent publishers, and at least two items for each input kind.
3. `items.jsonl` has resolvable text/transcript paths. Media references include segments and exact timestamps; no item is counted twice because it appeared in multiple formats.
4. `exclusions.jsonl` explains old, undated, invalid, or future material. Do not use excluded/undated material to support a publication claim.
5. Each selected/rejected/deferred record has a specific reason linked to the policy. Manually inspect at least three accepted and three rejected/deferred decisions.
6. There are exactly three briefs. Each has a distinct argument, claims with exact evidence, at least three independent publishers, a synthesis, and a limitation.
7. Each article is 600–900 words excluding references; each companion script is 3–5 minutes (roughly 450–700 spoken words). Article and script claims agree and point to source links useful to readers.
8. `review.json` has no unresolved blocking errors. Warnings still need human judgment. A machine check cannot judge whether the argument is insightful or fair.
9. You have personally reviewed the outputs and the `approval.json` fingerprint matches the current review.
10. A second **live** run on another day preserves its own inputs/logs and shows new/changed/unchanged behavior or explains no meaningful new items. Include a real collection failure/recovery or clearly labeled simulated failure.
11. The three Substack articles are accessible without a paywall; three YouTube videos are accessible as public/unlisted; every piece links to its companion. The technical demonstration is a separate 4–6 minute video.

For the AI itself, use the human-label comparison and metrics in [MODEL_EVALUATION.md](MODEL_EVALUATION.md). The API adapter is implemented, but no key is available in this workspace; fixture output cannot be scored as model performance.

## 9. Next action checklist

1. Confirm you want the configured topic/audience above.
2. Select six or more genuinely independent source publishers and verify that their recent materials are on-topic and accessible.
3. Implement/configure YouTube and podcast discovery plus timestamped transcription.
4. Choose and configure a model provider for selection, briefs, and drafting. Save the model/version and prompt used; keep API keys out of the repository.
5. Run the first live pipeline, inspect every stage, and repair collection/extraction problems.
6. Label a sample yourself, compare the model, revise policy once, and preserve before/after outputs.
7. Write and fact-check the three pieces, conduct human approval, render and publish the videos/articles.
8. Run again on a different date, compare results, finish the technical demo and submission checklist.

See [SUBMISSION.md](SUBMISSION.md) for the detailed assignment checklist and [MODEL_EVALUATION.md](MODEL_EVALUATION.md) for the model review method.

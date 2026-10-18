# How to evaluate the editorial AI

## Important: what is running today?

The pipeline contains an **OpenAI Responses API adapter**. A live run (`run-20261018T032602Z-70a5`) completed source collection and model selection, but brief generation failed because the request exceeded the model context window. Fixture mode uses fictional sample records and does not invoke the model; never describe fixture output as AI performance. Resume from saved evidence after applying the compact-evidence fix, then record the exact model/settings and preserve prompts and structured outputs. Keep credentials in environment variables.

## Evaluation question

For this publication, evaluate whether the model makes useful, evidence-grounded editorial decisions for small-team AI application developers, and whether its briefs/drafts avoid unsupported claims. The model is an assistant to the editor; your human labels are the comparison standard.

## Build a small review set

1. Select at least 20 real eligible items from the configured topic, including primary documentation, vendor announcements, independent research/evaluation, and practitioner experience.
2. Before looking at model decisions, label each item yourself as `accept`, `reject`, or `defer`. Record the reason and exact supporting or disqualifying passage. For accepted items, record useful piece IDs.
3. Give the exact same source records, text/transcripts, policy, and prompt to the model. Save its JSONL output and model/version/settings.
4. Compare the two sets item by item. Discuss at least three accepted and three rejected/deferred cases in `SUBMISSION.md`; include disagreements and what you changed in the policy.
5. Revise the policy or prompt, rerun the same frozen review set, and compare the results. Keep before/after files rather than overwriting the first result.

## Score each model decision

Use a spreadsheet or CSV with one row per item and these columns:

| Measure | How to score it |
|---|---|
| Decision agreement | Exact match between model and your `accept`/`reject`/`defer` label. Report the fraction and the disagreement examples. |
| Accepted-item precision | Of model-accepted items, the share you judged genuinely useful and adequately evidenced. |
| Accepted-item recall | Of items you accepted, the share the model accepted. |
| Evidence traceability | 0 = no passage; 1 = vague reference; 2 = exact relevant passage/segment; 3 = exact passage supports the reason. |
| Reason quality | 0 = unsupported/irrelevant; 1 = partly relevant; 2 = specific, policy-aligned, and supported. |
| Date/duplicate handling | Correctly detects stale/undated material, reposts, shared claims, and duplicate episode/video records. |
| Calibration and deferral | Defers when material is ambiguous or evidence is insufficient; does not state confidence as proof. |
| Unsupported claim count | Count factual claims in briefs/drafts that cannot be traced to the cited version and passage. Target: zero before human approval. |
| Coverage balance | Whether the selected set includes independent publishers and the required feed, video, and podcast evidence without counting duplicates twice. |

Report the counts and give examples. Do not rely on one overall score: a high agreement rate can hide a dangerous unsupported claim or a failure to defer. For a simple starting bar, investigate any evidence-traceability score below 2, every unsupported claim, and every disagreement that would materially change the publication. The course does not prescribe numeric AI accuracy thresholds; explain and justify any threshold you choose.

## Evaluate generated articles and scripts

For each of the three briefs, have a human reviewer check every claim ID against the exact source version and quote/timestamp. Compare article and video script claims for consistency. Check the assignment's word/time targets, independent-source count, limitations, counterargument, and whether the piece adds synthesis rather than summaries. Record corrections and their evidence in the review notes. A passing automated check is a mechanical check, not proof that interpretation is sound.

## Preserve evidence of the evaluation

Keep these in the repository or run artifacts:

- `evaluation/human_labels.csv`
- `evaluation/model_decisions_before.csv` and `evaluation/model_decisions_after.csv`
- the frozen evaluation item IDs/versions and saved prompts
- `evaluation/results.md` with counts, examples, disagreements, policy changes, and limitations
- model name/version, settings, run date, and estimated/known cost (never secrets)

This evaluation tests the **editorial model workflow**, not whether an agent framework itself is superior. If you also compare agent frameworks, use the same task set, model, tools, budgets, success criteria, and repeat runs for a fair comparison; report latency, cost, task success, recovery behavior, and safety failures.

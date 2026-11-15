# Skill provenance and path mapping

The current whole-pipeline entrypoint is `skill/SKILL.md`; the Solar report-authoring system prompt is `skill/report-writing/SKILL.md`. Both current skills were created after the historical runs listed here and were not used to author the existing reports. Former source files are preserved byte-for-byte under `provenance/skills/`; past request, response, and execution records remain unchanged.

| Current role | Path | Caller |
|---|---|---|
| Whole pipeline: input, identity, predictions, analysis evidence and report-skill routing | `skill/SKILL.md` | README and workflow guidance; recorded as `execution_skill_path` in `configs/report-plan.json` |
| Solar report writing: evidence interpretation, Korean manuscript, citation and document requirements | `skill/report-writing/SKILL.md` | Solar request builders; recorded as `report_writing_skill_path` in `configs/report-plan.json` |

The `synthesis_report_skill-report-v1.md` preserved below is a historical source copy, not the new report-writing file and not the pipeline entrypoint. The two new files separate these roles without retroactively attributing the current prompt to old reports.

| Historical source path | Preserved original | SHA-256 | Use and run association |
|---|---|---|---|
| `skill/synthesis_report_skill.md` (harness payload version) | `synthesis_report_skill-harness-v1.md` | `7da4b5b48ebc4e2d954fe9331ae0b27c89fcd2aa6c25617513d72e2cbe8e4714` | The saved shared payload manifest lists this file hash for OpenCode `opencode-trial-02` and Pi `pi-trial-02`. The embedded source was recovered from the saved payload and converted from payload CRLF to original LF bytes; its 7,381-byte hash matches the recorded hash. A separate earlier `preparation-only-01` request has the same system-content hash but its status is `prepared_not_executed`, so it is not counted as a Solar call. |
| `skill/synthesis_report_skill.md` (general report skill, later source copy) | `synthesis_report_skill-report-v1.md` | `cc78e000280a5dc968772226650c2d5a6888a767ef9731dbe72e9542e5ee46d8` | Exact historical file copied from the old path. `request-provenance.json` records it as the general skill associated with `benzocaine-documentation-cleanup-20261115-01`; however, that run's serialized Solar request contains only the targeted sentence skill in its system message. This copy is retained as the referenced general-skill version, not represented as content sent in that request. |
| `skill/targeted-benzocaine-section-revision-v1.md` | same basename | `c39a1c9391cb7456d386f1184cdaf4f354cf24258a2ad3c42072d6c7bb0dcca2` | Narrow rules for Solar run `benzocaine-hash-correction-final-20261115-01`. The raw system message is LF-normalized from this preserved CRLF file; its SHA-256 is `f4575d9f653cacdbb09740fb14fa33e0229f7b1bc56a5db750fdbcc38f9aa88c`. Request and response remain at `검증기록/이전-인용게이트실패/solar-call/`. |
| `skill/targeted-report-sentence-cleanup-v1.md` | same basename | `a791638e22b0f5154afdf54d70646ff1ce96ffdde76dcfff0904f2f26b33b39a` | Exact system message for Solar run `benzocaine-documentation-cleanup-20261115-01`; request provenance is in that report folder. |
| `skill/SKILL.md` (previous short launcher) | `SKILL-launcher-before-unification.md` | `2ef980a5bca4e4f4423c2e46dbeea8dfd8b6c6a7c63a4132a0495f9c19ba0990` | Previous local entrypoint only. No separate Solar request using this launcher text as its system message was identified; it is preserved to map the old entrypoint. |

Current code/config/README use the two role-specific paths above. Historical files and request payloads keep their old paths and bytes; use this table to trace those references. The archived targeted skills and old A/B instructions are provenance, not content imported into a new full-report request.

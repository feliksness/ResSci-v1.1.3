# Scientific Researcher

A Claude plugin with one skill that makes Claude work out **what the evidence actually supports** before it writes anything. It covers medicine, biology, chemistry, physics, astronomy, earth and climate science, mathematics, computer science, psychology, social science, and engineering.

The skill is built to prevent the failures that make AI-assisted research untrustworthy:

- invented references, and citations that don't support their sentences;
- made-up statistics and overstated certainty;
- association presented as causation;
- methods sections that describe work that never happened.

> No skill guarantees scientific correctness. This one is designed to maximize reliability and make uncertainty visible.

## Repository layout

```text
scientific-researcher/                    repository root = marketplace root = plugin root
├── .claude-plugin/
│   ├── marketplace.json                  marketplace "research-skills", lists this plugin (source "./")
│   └── plugin.json                       plugin "scientific-researcher"
├── skills/
│   └── scientific-researcher/
│       ├── SKILL.md                      core instructions, loaded when the skill triggers
│       ├── references/                   9 guides, read on demand
│       │   ├── evidence-evaluation.md    source tiers, evidence strength, conflicts, consensus, fallacies
│       │   ├── study-designs.md          designs, bias catalogue, risk-of-bias tools, causal inference
│       │   ├── citation-verification.md  verification procedure, retractions, preprints, quotations, audit
│       │   ├── statistics.md             interpretation, red flags, recomputation, meta-analysis
│       │   ├── systematic-review-methods.md  question frameworks, protocol, search, PRISMA
│       │   ├── field-specific-methods.md standards per discipline and where to search
│       │   ├── scientific-writing.md     structures, synthesis, gaps, limitations, citation styles, figures
│       │   ├── research-integrity.md     ethics, conflicts of interest, misconduct, predatory venues, dual-use
│       │   └── audit-checklists.md       fact-check, citation audit, anti-hallucination, quality gate
│       ├── scripts/                      Python 3, standard library only
│       │   ├── verify_citations.py       DOIs/PMIDs/arXiv/reference text vs Crossref, DataCite, PubMed, OpenAlex, arXiv
│       │   ├── check_citation_consistency.py   in-text citations vs reference list, placeholders
│       │   └── stats_tools.py            p recomputation, GRIM, 2x2 effects, CI→SE, PPV, SMD, meta-analysis
│       └── templates/                    research log, evidence table, deep-research report
├── evals/                                16 native `claude plugin eval` cases (prompt + graders)
├── tests/
│   ├── test-prompts.md                   the 16 adversarial tests, human-readable, with pass/fail criteria
│   ├── skill-creator-evals.json          same suite in Anthropic's skill-creator format
│   ├── trigger-evals.json                should/shouldn't-trigger queries for description tuning
│   └── files/bp_trial.csv                synthetic dataset used by test 10
├── .gitignore
└── README.md
```

The plugin contains only a skill. It has no hooks, no MCP servers, and no `bin/` executables, so it installs on every surface (chat, Cowork, Claude Code). The scripts reach the network only when Claude runs them for citation checks.

---

## Scripts

Run them from the repository root:

```bash
S=skills/scientific-researcher/scripts

# Citation consistency (offline), then export the reference list for verification
python3 $S/check_citation_consistency.py draft.md --export-refs refs.txt

# Citation verification. Needs internet access to api.crossref.org, doi.org, api.datacite.org,
# eutils.ncbi.nlm.nih.gov, api.openalex.org, export.arxiv.org
python3 $S/verify_citations.py --file refs.txt --email you@example.org

# Statistics
python3 $S/stats_tools.py pcheck --test t --stat 2.10 --df 28 --reported-p 0.045
python3 $S/stats_tools.py twobytwo --a 8 --b 1992 --c 16 --d 1984
python3 $S/stats_tools.py meta --csv effects.csv --ratio --hksj --loo
```

The verifier reports one of these statuses for each reference: `OK`, `CORRECTED`, `PREPRINT`, `REGISTERED_ELSEWHERE`, `UNCHECKED`, `PROBABLE_MATCH`, `NO_CONFIDENT_MATCH`, `NOT_FOUND`, `MISMATCH`, `EXPRESSION_OF_CONCERN`, `PARTIALLY_RETRACTED`, `RETRACTED`.

`UNCHECKED` means the service couldn't be reached. It means *not verified*, never *does not exist*.

Optional environment variables (never hard-code keys): `CROSSREF_MAILTO`, `NCBI_EMAIL`, `NCBI_API_KEY`, `OPENALEX_API_KEY`.

---

## Test it

The `evals/` folder runs with `claude plugin eval`, which needs Claude Code v2.1.269 or later. Each case runs once per arm by default, with and without the plugin, and reports the difference. Runs use your Claude plan or API credits.

```bash
# Offline cases (statistics, data integrity, abstract appraisal, no-tools honesty)
claude plugin eval . --tag offline

# Research cases that need the web
claude plugin eval . --tag needs-web --allow-tools WebSearch WebFetch

# Confirm a result with more runs
claude plugin eval . --case reference-list-audit --runs 3 --allow-tools WebSearch WebFetch
```

- `crispr-references-no-tools` checks behavior **without** web access. Run it on its own with no `--allow-tools` grant.
- Granting `Bash` lets the skill run its Python checkers inside the eval sandbox. On Linux this needs `bubblewrap` and `socat`.
- Each case has three kinds of graders:
  - an `llm` rubric built from the pass/fail criteria in `tests/test-prompts.md`;
  - a `skill-fired` check showing whether Claude loaded the skill;
  - for some cases, deterministic regex checks (for example, no DOIs from memory in the no-tools case).

### What was verified before release

- `claude plugin validate .` passes with one expected warning (no `version`; see Update).
- The plugin installed from a local copy of this marketplace with `claude plugin install scientific-researcher@research-skills`. Claude Code found the skill, at about 80 tokens always-on and about 9k tokens when it fires.
- Sample eval runs:
  - `abstract-only-appraisal` scored 1.00 with the skill firing.
  - `drug-trial-relative-risk-and-p-value` passed its rubric, but Claude answered without loading the skill. Some tasks are within what Claude does well unaided, which is what the with/without comparison measures.
- `stats_tools.py`:
  - its distribution functions match SciPy (relative error below 1e-11);
  - its random-effects meta-analysis reproduces the classic BCG vaccine trials dataset (DerSimonian–Laird log RR −0.7141, τ² 0.3088, I² 92.1%).
- `verify_citations.py` was tested against mocked responses built from real Crossref, PubMed, and OpenAlex records, because direct API calls were blocked in the build environment. **Run it once against the live APIs before relying on it.**
- An independent review of the whole package (contradictions, dead references, coverage, factual accuracy, script edge cases) was run, and its findings were fixed.

---

## Design notes

- **Format:** `SKILL.md` follows the [Agent Skills specification](https://agentskills.io/specification). `name` is `scientific-researcher` (lowercase, matching its folder) and `description` is under the 1,024-character limit.
- **Progressive disclosure:** `SKILL.md` holds the rules, workflow, and quality gates. Detailed procedures live in `references/` and are read only when needed.
- **No citations inside the skill:** the skill names established frameworks (GRADE, PRISMA 2020, RoB 2, and others) but contains no bibliographic references, so it can't seed fabricated ones.

## License

Add a `LICENSE` file before publishing (for example MIT or CC BY 4.0). Anthropic's plugin directory requires one if you ever submit there.

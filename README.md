# Scientific Researcher

A Claude plugin with one skill that makes Claude work out **what the evidence actually supports** before it writes anything. It covers medicine, biology, chemistry, physics, astronomy, earth and climate science, mathematics, computer science, psychology, social science, and engineering.

The skill is built to prevent the failures that make AI-assisted research untrustworthy:

- invented references, and citations that don't support their sentences;
- made-up statistics and overstated certainty;
- association presented as causation;
- methods sections that describe work that never happened.

> No skill guarantees scientific correctness. This one is designed to maximize reliability and make uncertainty visible.

This repository is a **plugin marketplace**, so people can install the plugin straight from its GitHub address in the Claude apps and in Claude Code.

---

## Install

Replace `YOUR-GITHUB-USERNAME` with the account that hosts this repository.

### Claude apps (claude.ai, Claude Desktop, Cowork)

1. Open **Customize → Plugins**.
2. Choose **Add → Add marketplace** and enter `YOUR-GITHUB-USERNAME/scientific-researcher`, or the full URL `https://github.com/YOUR-GITHUB-USERNAME/scientific-researcher`.
3. Find **Scientific Researcher** in the list and select **Add**.
4. To let the skill run its Python checkers, turn on **Code execution and file creation** in Settings → Capabilities. On Team and Enterprise plans an Owner enables this.

The plugin is saved to your account. It is then available in chat and Cowork, and in Claude Code as a synced plugin when you sign in there.

### Claude Code (terminal, desktop Code tab, VS Code)

```text
/plugin marketplace add YOUR-GITHUB-USERNAME/scientific-researcher
/plugin install scientific-researcher@research-skills
```

To do both in one command (Claude Code v2.1.275 or later):

```text
/plugin install scientific-researcher --marketplace YOUR-GITHUB-USERNAME/scientific-researcher
```

From your shell, use `claude plugin marketplace add …` and `claude plugin install …` with the same arguments.

### Without GitHub

- **Upload the plugin:** zip this whole folder, then in the Claude apps go to **Customize → Plugins → Add → Upload plugin**.
- **Upload the skill only:** zip the `skills/scientific-researcher` folder so that folder is at the top of the zip, then go to **Customize → Skills → + → Create skill → Upload a skill**. If the uploader rejects the description length, replace the `description` line in `SKILL.md` with this shorter version:
  `description: Conduct rigorous scientific research, evaluate evidence, verify sources, synthesize literature, audit citations, and produce scientifically defensible articles across disciplines.`
- **Claude Code without a marketplace:** copy `skills/scientific-researcher` into `~/.claude/skills/`.

---

## Publish this repository to GitHub

The **contents** of this folder must sit at the top level of the repository: `.claude-plugin/` has to be at the repository root.

The easy mistake is losing the hidden folder. On macOS, Finder hides `.claude-plugin/` and `.gitignore`, so dragging the folder into GitHub's web uploader can silently leave them out, and the install then fails because Claude finds no marketplace file. To avoid that, use git, GitHub Desktop, or press `Cmd + Shift + .` in Finder to show hidden files before you drag.

With git:

```bash
cd scientific-researcher
git init
git add .
git commit -m "Scientific Researcher plugin v1"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/scientific-researcher.git
git push -u origin main
```

Then check on GitHub that you can see `.claude-plugin/marketplace.json` at the top of the repository.

**Private repositories** also work. In the Claude apps, connect your GitHub account when the dialog asks and give the Claude GitHub App access. In Claude Code, the git credentials on your machine are used.

---

## Use

Just ask for research work, for example:

- "What does the evidence say about intermittent fasting and longevity?"
- "Write a literature review on microplastics in human tissue."
- "Check these 20 references before I submit."
- "Appraise this abstract for risk of bias."
- "Analyze this dataset and write the Results section."
- "Is this Feynman quote real?"

Claude loads the skill when the request matches. You can also call it directly:

- **Claude apps:** type `/` and pick *scientific-researcher*.
- **Claude Code:** `/scientific-researcher:scientific-researcher`.

For the full evidence package (research log, evidence table, risk-of-bias and certainty ratings, citation audit), ask for **Deep** or "publication-quality" work.

**Best results need web access.** With search and fetch tools the skill verifies sources itself. Without them, it says so and labels everything unverified rather than inventing references.

---

## Update

No `version` is pinned in `plugin.json`, so each new commit is a new version.

- **To release:** edit, commit, and push.
- **Claude apps:** open the plugin's marketplace and select **Check for updates**, or turn on **Sync automatically**.
- **Claude Code:** run `claude plugin update scientific-researcher@research-skills`, or turn on auto-update for the `research-skills` marketplace in `/plugin` → **Marketplaces**.

`claude plugin validate .` shows one warning about the missing `version`. That is expected for this commit-based setup. If you'd rather use numbered releases, add `"version": "1.0.0"` to `.claude-plugin/plugin.json` and increase it every time you push.

---

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

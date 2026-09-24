# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

CodeJourneyPython is a Python learning platform: a collection of independent, self-contained
projects (`projects/`), library tutorials (`libraries/`), and reference material
(`resources/`) rather than a single deployable application. Each project under `projects/`
has its own README, dependencies, and test suite; there is no shared runtime between them
beyond `projects/utils/`.

## Commands

### Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt          # core dev tooling (pytest, black, flake8, isort, mypy)
pip install -r requirements-ml.txt            # only if touching ML projects/libraries
pip install -r requirements-agents.txt        # only if touching ai_agent_chatbot
pip install -r requirements-web.txt           # only if touching a web project
pip install -r projects/ai_agents/requirements.txt   # only if touching projects/ai_agents
pre-commit install
```

### Tests
Pytest is configured (`pyproject.toml`) with `testpaths = ["projects"]` and coverage against
`projects` on by default.
```bash
python -m pytest projects/ -v                                              # all tests
python -m pytest projects/guess_the_number/tests/test_game.py -v           # one file
python -m pytest projects/guess_the_number/tests/test_game.py::TestGuessTheNumberGame -v  # one class
python -m pytest projects/ --cov=projects --cov-report=html               # coverage report
```
Target coverage is 80%+ for new code (see CONTRIBUTING.md).

### Formatting & linting
```bash
black projects/       # line-length 100
isort projects/       # profile=black
flake8 projects/      # max-line-length 100, E203/W503/E501 ignored
mypy projects/        # non-strict: untyped defs allowed, but checks what's annotated
```
`pre-commit run --all-files` runs black, isort, flake8, and the standard pre-commit hygiene
hooks (trailing whitespace, EOF fixer, YAML check, large-file check, merge-conflict check) plus
mypy.

## Architecture

### Layout
- `projects/<name>/` — one folder per project, each independently runnable (`main.py` or
  equivalent entry point) with its own `README.md`, `requirements.txt`, and `tests/` package.
  Existing projects: `guess_the_number` (CLI basics), `ai_agent_chatbot` (LLM agent + tool use),
  `data_pipeline_etl` (ETL pipeline), `ai_agents` (five educational agent implementations —
  tool use, ReAct reasoning, multi-agent teams, memory/RAG, planning; see its own README and
  `CLAUDE.md`-equivalent hub doc at `projects/ai_agents/README.md`). Note: CONTRIBUTING.md
  references `ml_recommendation` and `web_api_service` as planned/example projects — they do
  not exist yet in `projects/`.
- `projects/utils/` — the only code shared across projects: `config.py` (env-var/`.env`-backed
  `Config` class), `errors.py` (exception hierarchy), `logging_config.py` (`setup_logger`/
  `get_logger` with rotating file handlers). New projects are expected to reuse these rather than
  rolling their own config/logging/error handling.
- `libraries/` — standalone Markdown tutorials/reference material for third-party libraries
  (NumPy, Pandas), not code that gets imported or tested.
- `resources/` — cheatsheets and curated links, documentation only.

### Conventions used throughout `projects/`
- **Error handling**: raise from the shared hierarchy in `projects/utils/errors.py`
  (`BaseProjectError` subclasses carry a `message` and machine-readable `error_code`) rather than
  bare exceptions. Project-specific error types (e.g. `InvalidGuessError`, `PipelineError`)
  subclass these.
- **Config**: dataclass-based `Config` per project (see `ai_agent_chatbot/config.py`) with a
  `from_env()` classmethod reading `os.getenv(...)` and a `validate()` method that raises
  `ValueError` on bad values, or the shared `projects/utils/config.Config` for simpler cases.
  Real secrets live in `.env` (gitignored); `.env.example` at the repo root and per-project
  documents the expected keys.
- **Logging**: modules call `logging.getLogger(__name__)` and rely on
  `projects/utils/logging_config.setup_logger()` to attach console/rotating-file handlers with a
  consistent format; loggers are cached by name.
- **Pipeline/agent-style projects** favor a small class hierarchy with `NotImplementedError`
  stubs for subclasses to fill in (e.g. `data_pipeline_etl.Pipeline.extract/transform/load`) plus
  a dataclass tracking run statistics/status (`PipelineStatistics`, `ConversationState`).
- **Docstrings**: Google-style docstrings (Args/Returns/Raises/Example) are expected on modules,
  classes, and functions — enforced stylistically, not by a linter rule beyond flake8's
  `docstring-convention = google` setting.
- **Tests**: colocated under `projects/<name>/tests/test_<module>.py`, class-based
  (`TestXxx`/`test_xxx`), using pytest fixtures for setup.
- **Imports — two conventions coexist, only one actually works from the repo root**:
  `guess_the_number` and `ai_agents` use absolute imports rooted at `projects.` (e.g.
  `from projects.ai_agents.agent1_web_search.agent import WebSearchAgent`), which is what
  makes `python -m pytest projects/ -v` succeed. `ai_agent_chatbot` instead uses flat,
  package-relative imports (`from agent import AIAgent`) that only resolve when run with
  that project's own directory on `sys.path` (e.g. `cd`'d into it) — running the documented
  `pytest projects/` from the repo root currently fails to collect
  `ai_agent_chatbot/tests/test_agent.py` with `ModuleNotFoundError: No module named 'agent'`.
  This is a pre-existing inconsistency, not a regression to "fix" reflexively — but always
  write **new** code using the `projects.`-rooted absolute-import style, and don't assume
  `pytest projects/` is fully green until you've checked.

### Adding a new project
Follow the structure in CONTRIBUTING.md: `projects/<name>/{__init__.py, main.py, module.py,
config.py, README.md, tests/{__init__.py, test_*.py}}`, reusing `projects/utils/` for
config/logging/errors, and register any new heavy dependencies in the relevant top-level
`requirements-*.txt` (and `pyproject.toml` optional-dependencies / `setup.py` extras if they
should be pip-installable).

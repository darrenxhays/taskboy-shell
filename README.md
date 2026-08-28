# taskboy-shell

This is the **shell** for a [TaskBoy](https://github.com/your-org/taskboy) deployment: everything that is *yours* — the pinned application version, operator config, personalities, conventions, skills, infrastructure, and the deploy pipeline — and nothing that is application code. The application itself is the `taskboy` package on PyPI; you never fork or edit its source.

Create your own private repository from this template ("Use this template" on GitHub — not a fork), then:

```bash
git clone <your-shell-repo> && cd <your-shell-repo>
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
taskboy setup          # guided setup: writes config/config.yaml + config/services/*.yaml + .env, installs skills
```

Commit what the wizard wrote (everything except `.env` — secrets never enter git). [SETUP.md](SETUP.md) is the full operator runbook: prerequisites, the wizard, host deployment, CI/CD, and end-to-end verification. Prefer editing files over answering prompts? See [MANUAL_SETUP.md](MANUAL_SETUP.md).

## Layout

```text
requirements.txt        the taskboy version this deployment runs (pinned)
config/                 operator policy: config.yaml, services/<name>.yaml per connected service, personalities, conventions, started messages
skills/                 installed skills, one directory per /skill
infrastructure/         reference AWS deployment (Pulumi)
.github/workflows/      PR config validation (develop + main) + deploy on merge to main
```

## How changes reach your deployment

This repo follows GitFlow via [HubFlow](https://datasift.github.io/gitflow/): day-to-day changes land on `develop` through PRs, and `main` only moves when `git hf release finish` (or `hotfix finish`) merges and pushes it. Every merge to `main` deploys: the workflow runs `pulumi up`, bundles `config/` + `skills/`, and invokes the host's updater over SSM, which pip-installs the pinned `taskboy` version, syncs the config bundle, and restarts the service (restarts are safe — running tasks requeue and resume).

- **Config change**: edit `config/` on a feature branch, open a PR to `develop` (CI validates it against the pinned version), merge.
- **Turn a service on/off**: flip `enabled` in `config/services/<name>.yaml` (slack, github, jira, confluence, sentry, aws), PR to `develop`, merge.
- **Upgrade**: bump the pin in `requirements.txt`, PR to `develop`, merge. Roll back by reverting the commit and cutting a new release.
- **Ship it**: `git hf release start <name> && git hf release finish <name>` — the merge to `main` is the deploy.
- **Dashboard edits**: point `dashboard.auto_commit.repo` at this repository (`auto_commit.branch: develop`) so live edits from Mission Control land on the integration branch and ship with the next release.

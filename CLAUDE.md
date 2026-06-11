# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a GitHub Actions CI/CD pipeline project for Python-based software. The repository contains reusable workflow definitions covering PR checks, deployments, releases, and security scanning.

## Workflow Structure

- All workflow files live in `.github/workflows/`
- Use descriptive filenames: `ci.yml`, `deploy-staging.yml`, `release.yml`, `security-scan.yml`
- Prefix job IDs with the workflow purpose (e.g., `build-`, `deploy-`, `release-`)

## Python Toolchain Conventions

- Use `actions/setup-python` with `python-version` pinned to a specific minor version (e.g., `"3.12"`)
- Cache dependencies with `actions/cache` keyed on `requirements*.txt` or `pyproject.toml` hash
- Prefer `pip install -e ".[dev]"` for editable installs with dev extras over bare `pip install -r requirements.txt`
- Use `uv` or `pip` consistently — do not mix package managers within a workflow

## Secrets and Environment Variables

- Never hardcode secrets; always reference `${{ secrets.SECRET_NAME }}`
- Use environment-scoped secrets for staging vs. production deployments (GitHub environment protection rules)
- Document required secrets in a top-of-file comment block within each workflow that uses them

## Workflow Authoring Rules

- Pin third-party actions to a full commit SHA, not a tag (e.g., `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af68a`)
- Use `concurrency` groups on PR workflows to cancel stale runs
- Set `permissions` explicitly at the job level — default to least privilege
- Always set a `timeout-minutes` on jobs that run tests or deployments

## Testing Workflows Locally

Use `act` to run GitHub Actions workflows locally before pushing:

```
act push                    # simulate a push event
act pull_request            # simulate a PR event
act -j <job-id>             # run a specific job
act --secret-file .secrets  # pass local secrets file
```

## Security Scanning

- Use `github/codeql-action` for static analysis on Python code
- Run `trivy` or `pip-audit` for dependency vulnerability scanning
- Dependabot config lives at `.github/dependabot.yml`

## Branch and PR Conventions

- Workflow changes should be tested on a feature branch before merging to main
- Use `workflow_dispatch` inputs for any manual-trigger parameters — document all inputs with `description` fields
- Reusable workflows live in `.github/workflows/` and are called with `uses: ./.github/workflows/<file>.yml`

# AGENTS.md

Repo-wide operating notes for agents working in this repository.

## Agent skills

### Issue tracker

Issues and specs live as GitHub issues in `wozhendeshifwa/shiyanpigai`, managed through the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles use the default label strings (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`) with no overrides. See `docs/agents/triage-labels.md`.

### Domain docs

The layout is single-context: one `CONTEXT.md` at the repo root, with architecture decisions in `docs/adr/`. See `docs/agents/domain.md`.

## 实验报告批改

批改《计算机网络》实验报告（PDF 评分、批改意见、成绩单）前先读 `docs/grading/lab-reports.md`；批改完跑 `python scripts/verify_batch.py`（参数见该文档）。

学生姓名、学号、成绩只留在本机 `C:\Users\27263\Documents\计网实验批改\`。本仓库是公开仓库，这些数据一律不要提交。

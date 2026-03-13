# ResearchOS Codex Working Rules

## Branching and baseline
- Always start from the latest `main` branch state before implementing a new task.
- Implement exactly one milestone at a time.

## Change scope discipline
- Do not recreate or overwrite files that are already merged unless a minimal targeted edit is strictly necessary for the current task.
- Keep architecture changes incremental and scoped to the requested milestone.

## Required task-close updates
For every completed Codex task, update all of:
- `docs/ROS_STATUS.md`
- `docs/ROS_NEXT_TASK.md`
- `docs/CODEX_EXPORT.md`

## Required validation
For every completed Codex task, run project validation before handoff.
- Preferred command: `bash scripts/ros_validate.sh`

## CODEX export minimum content
`docs/CODEX_EXPORT.md` must include:
- task goal
- files changed
- test command
- test output
- main run command
- main run output
- known limitations
- next recommended task

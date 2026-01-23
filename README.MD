# RepoGuard

RepoGuard is a **repo-aware pull request guideline validator**.

It evaluates code changes **only against a repository’s own written rules**
(README, CONTRIBUTING, optional CODE_OF_CONDUCT) and classifies the change as:

- **OK** – clearly complies with all applicable guidelines
- **Warning** – potentially violates a guideline (ambiguous or partial)
- **Violation** – clearly and unambiguously breaks a guideline

RepoGuard is **not**:

- a linter
- a CI replacement
- a code reviewer

It is a **pre-PR reasoning gate** focused on correctness, policy adherence, and trust.

---

## Why RepoGuard exists

Most automated checks enforce:

- syntax
- formatting
- generic best practices

But real engineering rules often live only in documentation:

- “Breaking changes must include migration notes”
- “Public APIs must be documented”
- “New endpoints require auth checks”

RepoGuard enforces **what the repository itself says**, not external opinions.

---

## Zero-setup usage (2 steps)

RepoGuard is designed to be usable **immediately**, with no configuration.

```bash
pip install repoguard
repoguard validate
```

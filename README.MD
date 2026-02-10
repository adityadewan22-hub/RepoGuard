## Usage (3 commands)

### 1. Install

pip install repoguard-ai

### 2. Analyze repository guidelines (one-time or when docs change)

repoguard-ai analyze

### 3. Validate repository

repoguard-ai validate

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
- “New endpoints require authentication”
- “Security-sensitive changes require justification”

RepoGuard enforces **what the repository itself declares**, not external opinions.

---

## How RepoGuard works

RepoGuard operates in **two explicit phases**:

1. **Analyze** – index the repository’s written guidelines
2. **Validate** – evaluate code diffs against those guidelines

This makes the system:

- deterministic
- explainable
- reusable across multiple validations

---

```mermaid

flowchart TD
    A[Pull Request or Code Diff] --> B[RepoGuard CLI or GitHub Action]

    B --> C[Load Repository Context]
    C --> C1[README.md]
    C --> C2[CONTRIBUTING.md]
    C --> C3[CODE_OF_CONDUCT.md optional]

    C --> D[Guideline Processing]
    D --> D1[Chunk Guidelines]
    D --> D2[Generate Embeddings]
    D --> D3[Store or Query Vector DB]

    A --> E[Diff Analysis]
    E --> E1[Extract Changed Files]
    E --> E2[Summarize Code Changes]

    D --> F[Semantic Retrieval]
    F --> F1[Top K Relevant Guidelines]

    E --> G[LLM Evaluation]
    F --> G

    G --> H{Compliance Decision}
    H --> I[OK]
    H --> J[Warning]
    H --> K[Violation]

    I --> L[Structured Report]
    J --> L
    K --> L

    L --> M[CLI Output or PR Comment]

```

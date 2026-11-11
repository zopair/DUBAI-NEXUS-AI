# Dubai Nexus AI

**Independent bilingual agentic-operations project.** This repository is intentionally separate from all other products and codebases.

## Engineering status

The initial repository foundation is a dependency-free, safety-first prototype. It currently provides:
- Deterministic Arabic/English request language and intent detection.
- Reviewable plans with explicit steps.
- A conservative policy gate: read-only steps may be planned; sensitive actions are blocked pending human approval.
- A local JSONL audit trail.
- A responsive Arabic/English dashboard with RTL/LTR support.
- A local Python HTTP server and automated CI tests.

This is **not yet a production-ready autonomous agent**. The intent router is a deterministic baseline, not an LLM. The executor is a simulator and does not send messages, move money, modify business systems, or access private accounts.

## Run locally

```bash
python -m app.server
```

Open `http://127.0.0.1:8080`.

## Tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs compilation and unit tests on Python 3.11, 3.12, and 3.13 for pushes to the foundation branch and pull requests to `main`.

## Safety and privacy

- Use synthetic data only.
- Unknown actions are denied by default.
- Sensitive actions are not executed; approval is a policy state, not a real approval workflow.
- The local audit file is append-only by application behavior, not tamper-proof.
- Authentication, tenant isolation, encrypted durable storage, key management, threat modelling, and deployment hardening are required before customer data is processed.
- No claim of absolute or “zero leakage” security is made.

## Zero-cost baseline

The runtime uses only the Python standard library. The CI workflow uses GitHub-hosted Actions and does not install paid or application dependencies.

## Architecture direction

`HTTP API -> Intent Provider -> Planner -> Policy Engine -> Tool Registry -> Verifier -> Audit Log`

Any future model provider must be isolated behind a typed interface. Model output must never grant itself tool permissions or bypass policy enforcement.

## License

MIT. See [LICENSE](LICENSE).

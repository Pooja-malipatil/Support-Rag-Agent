import ollama
import yaml
from pathlib import Path
from datetime import date
from rich.console import Console
from rich.progress import track

console = Console()

# Every topic area with 5 documents each
CORPUS_PLAN = [
    # Authentication
    {
        "source_name": "authentication-overview",
        "section": "Authentication",
        "doc_type": "guide",
        "topic": "Overview of API authentication methods including API keys, OAuth 2.0, and JWT tokens. When to use each method."
    },
    {
        "source_name": "api-keys-guide",
        "section": "Authentication",
        "doc_type": "guide",
        "topic": "Complete guide to API keys: generating, storing securely, rotating, revoking, and best practices for production use."
    },
    {
        "source_name": "oauth-guide",
        "section": "Authentication",
        "doc_type": "guide",
        "topic": "OAuth 2.0 implementation guide: authorization code flow, client credentials flow, scopes, and token refresh."
    },
    {
        "source_name": "authentication-faq",
        "section": "Authentication",
        "doc_type": "faq",
        "topic": "Frequently asked questions about API authentication: common errors, token expiry, scope issues, and troubleshooting."
    },
    {
        "source_name": "authentication-policy",
        "section": "Authentication",
        "doc_type": "policy",
        "topic": "Authentication security policy: key rotation requirements, prohibited uses, compliance requirements, and violation consequences."
    },

    # Rate Limiting
    {
        "source_name": "rate-limiting-overview",
        "section": "Rate Limiting",
        "doc_type": "guide",
        "topic": "How rate limiting works: request quotas, time windows, token bucket algorithm, and different limits per endpoint."
    },
    {
        "source_name": "rate-limit-tiers",
        "section": "Rate Limiting",
        "doc_type": "guide",
        "topic": "Rate limit tiers by plan: Free (100 req/min), Pro (1000 req/min), Enterprise (custom). Burst limits and daily quotas."
    },
    {
        "source_name": "handling-429-errors",
        "section": "Rate Limiting",
        "doc_type": "guide",
        "topic": "How to handle HTTP 429 Too Many Requests: exponential backoff implementation, retry-after headers, jitter strategies."
    },
    {
        "source_name": "rate-limiting-faq",
        "section": "Rate Limiting",
        "doc_type": "faq",
        "topic": "FAQ about rate limits: what counts as a request, shared limits across keys, monitoring usage, requesting limit increases."
    },
    {
        "source_name": "rate-limiting-policy",
        "section": "Rate Limiting",
        "doc_type": "policy",
        "topic": "Rate limiting policy: fair use requirements, consequences of limit abuse, how limits are calculated and enforced."
    },

    # Errors
    {
        "source_name": "error-codes-reference",
        "section": "Errors",
        "doc_type": "guide",
        "topic": "Complete HTTP error code reference: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests, 500 Internal Server Error. Causes and fixes for each."
    },
    {
        "source_name": "error-objects",
        "section": "Errors",
        "doc_type": "guide",
        "topic": "API error response format: error object structure, error codes, error messages, request IDs for debugging."
    },
    {
        "source_name": "debugging-api-errors",
        "section": "Errors",
        "doc_type": "guide",
        "topic": "How to debug API errors: reading error responses, using request IDs, checking logs, common mistakes and their fixes."
    },
    {
        "source_name": "error-handling-faq",
        "section": "Errors",
        "doc_type": "faq",
        "topic": "FAQ about API errors: difference between 401 and 403, what to do with 500 errors, idempotency for retries."
    },
    {
        "source_name": "error-handling-best-practices",
        "section": "Errors",
        "doc_type": "guide",
        "topic": "Best practices for error handling: retry logic, circuit breakers, logging errors, user-facing error messages."
    },

    # Webhooks
    {
        "source_name": "webhooks-overview",
        "section": "Webhooks",
        "doc_type": "guide",
        "topic": "What webhooks are, how they differ from polling, event types available, and when to use webhooks."
    },
    {
        "source_name": "webhook-setup",
        "section": "Webhooks",
        "doc_type": "guide",
        "topic": "Setting up webhooks: registering endpoints, selecting events, testing with CLI, verifying delivery."
    },
    {
        "source_name": "webhook-security",
        "section": "Webhooks",
        "doc_type": "guide",
        "topic": "Securing webhooks: signature verification using HMAC, replay attack prevention, IP allowlisting, HTTPS requirements."
    },
    {
        "source_name": "webhook-retries",
        "section": "Webhooks",
        "doc_type": "guide",
        "topic": "Webhook retry behavior: retry schedule, what triggers a retry, idempotency keys, handling duplicate events."
    },
    {
        "source_name": "webhooks-faq",
        "section": "Webhooks",
        "doc_type": "faq",
        "topic": "FAQ about webhooks: why events are delivered out of order, debugging failed webhooks, testing locally with ngrok."
    },

    # Versioning
    {
        "source_name": "api-versioning-overview",
        "section": "Versioning",
        "doc_type": "guide",
        "topic": "How API versioning works: version in URL vs header, current versions, how to specify version in requests."
    },
    {
        "source_name": "deprecation-policy",
        "section": "Versioning",
        "doc_type": "policy",
        "topic": "API deprecation policy: notice period (12 months), sunset headers, migration guides, end-of-life process."
    },
    {
        "source_name": "migration-guide-v2-v3",
        "section": "Versioning",
        "doc_type": "guide",
        "topic": "Migration guide from API v2 to v3: breaking changes, new endpoints, deprecated fields, code examples for each change."
    },
    {
        "source_name": "changelog",
        "section": "Versioning",
        "doc_type": "guide",
        "topic": "API changelog: recent additions, bug fixes, deprecation notices, and breaking changes by version."
    },
    {
        "source_name": "versioning-faq",
        "section": "Versioning",
        "doc_type": "faq",
        "topic": "FAQ about versioning: what happens when a version is deprecated, can I use multiple versions, how to test new versions."
    },

    # SDKs
    {
        "source_name": "python-sdk-quickstart",
        "section": "SDKs",
        "doc_type": "guide",
        "topic": "Python SDK quickstart: installation, initialization, making first request, handling responses and errors."
    },
    {
        "source_name": "javascript-sdk-quickstart",
        "section": "SDKs",
        "doc_type": "guide",
        "topic": "JavaScript SDK quickstart: npm install, CommonJS vs ESM, async/await usage, error handling."
    },
    {
        "source_name": "sdk-configuration",
        "section": "SDKs",
        "doc_type": "guide",
        "topic": "SDK configuration options: timeout settings, retry configuration, base URL override, logging, proxy settings."
    },
    {
        "source_name": "sdk-vs-raw-api",
        "section": "SDKs",
        "doc_type": "guide",
        "topic": "SDK vs raw HTTP API: when to use each, what SDKs handle automatically, performance considerations."
    },
    {
        "source_name": "sdk-faq",
        "section": "SDKs",
        "doc_type": "faq",
        "topic": "FAQ about SDKs: supported languages, SDK version compatibility with API version, contributing to open source SDKs."
    },

    # Billing
    {
        "source_name": "billing-overview",
        "section": "Billing",
        "doc_type": "guide",
        "topic": "How billing works: usage-based vs subscription pricing, billing cycle, invoice generation, payment methods."
    },
    {
        "source_name": "plans-comparison",
        "section": "Billing",
        "doc_type": "guide",
        "topic": "Plan comparison: Free (limited requests, no SLA), Pro ($49/month, 1M requests, 99.9% SLA), Enterprise (custom pricing, dedicated support)."
    },
    {
        "source_name": "usage-and-quotas",
        "section": "Billing",
        "doc_type": "guide",
        "topic": "Monitoring usage and quotas: usage dashboard, setting spending limits, alerts for quota thresholds, overage charges."
    },
    {
        "source_name": "billing-faq",
        "section": "Billing",
        "doc_type": "faq",
        "topic": "FAQ about billing: what counts as a billable request, how to upgrade or downgrade, prorated charges, invoice disputes."
    },
    {
        "source_name": "billing-policy",
        "section": "Billing",
        "doc_type": "policy",
        "topic": "Billing policy: payment terms (net 30), late payment consequences, refund policy (no refunds after 30 days), account suspension."
    },

    # Security
    {
        "source_name": "security-overview",
        "section": "Security",
        "doc_type": "guide",
        "topic": "API security overview: encryption in transit (TLS 1.2+), encryption at rest, SOC2 compliance, penetration testing."
    },
    {
        "source_name": "key-rotation-guide",
        "section": "Security",
        "doc_type": "guide",
        "topic": "API key rotation guide: why to rotate, rotation without downtime, automated rotation, emergency rotation after compromise."
    },
    {
        "source_name": "ip-allowlisting",
        "section": "Security",
        "doc_type": "guide",
        "topic": "IP allowlisting: restricting API access to specific IPs, CIDR notation, dynamic IPs, allowlisting for CI/CD pipelines."
    },
    {
        "source_name": "audit-logs",
        "section": "Security",
        "doc_type": "guide",
        "topic": "Audit logs: what events are logged, log retention (90 days), exporting logs, integrating with SIEM systems."
    },
    {
        "source_name": "security-policy",
        "section": "Security",
        "doc_type": "policy",
        "topic": "Security policy: responsible disclosure, bug bounty program, security incident response, data breach notification."
    },

    # Onboarding
    {
        "source_name": "quickstart-guide",
        "section": "Onboarding",
        "doc_type": "guide",
        "topic": "5-minute quickstart: create account, generate API key, make first request, understand the response format."
    },
    {
        "source_name": "environments-guide",
        "section": "Onboarding",
        "doc_type": "guide",
        "topic": "Test vs production environments: separate API keys per environment, sandbox behavior, test data, promoting to production."
    },
    {
        "source_name": "first-integration-guide",
        "section": "Onboarding",
        "doc_type": "guide",
        "topic": "Building your first integration: architecture decisions, error handling from day one, monitoring setup, going live checklist."
    },
    {
        "source_name": "onboarding-faq",
        "section": "Onboarding",
        "doc_type": "faq",
        "topic": "FAQ for new developers: how long does account approval take, free tier limitations, how to get help, SLA during trial."
    },
    {
        "source_name": "onboarding-checklist",
        "section": "Onboarding",
        "doc_type": "guide",
        "topic": "Production readiness checklist: authentication setup, error handling, rate limit handling, webhook verification, monitoring."
    },

    # Troubleshooting
    {
        "source_name": "common-errors-guide",
        "section": "Troubleshooting",
        "doc_type": "guide",
        "topic": "Common API errors and fixes: invalid API key, expired token, malformed request body, missing required fields."
    },
    {
        "source_name": "debugging-guide",
        "section": "Troubleshooting",
        "doc_type": "guide",
        "topic": "Debugging API integrations: using request IDs, reading error messages, checking API status page, isolating issues."
    },
    {
        "source_name": "performance-troubleshooting",
        "section": "Troubleshooting",
        "doc_type": "guide",
        "topic": "Performance troubleshooting: high latency causes, connection pooling, timeout configuration, geographic routing."
    },
    {
        "source_name": "troubleshooting-faq",
        "section": "Troubleshooting",
        "doc_type": "faq",
        "topic": "Troubleshooting FAQ: why is my request failing silently, how to test without affecting production, getting support."
    },
    {
        "source_name": "support-escalation",
        "section": "Troubleshooting",
        "doc_type": "guide",
        "topic": "Getting support: community forums, email support (Pro+), dedicated Slack (Enterprise), SLA response times by plan."
    },
]


def generate_document(plan: dict) -> str:
    """Uses Ollama to generate realistic documentation for a topic."""

    prompt = f"""Write realistic API documentation for a fictional company called "DevAPI".

Topic: {plan['topic']}
Document type: {plan['doc_type']}
Section: {plan['section']}

Requirements:
- Write in professional technical documentation style
- Include specific details like HTTP status codes, example values, code snippets
- Use ## headings to separate major sections
- Each section should be 3-6 sentences with concrete details
- Include at least 3-4 ## sections
- Make it realistic — include specific numbers, error codes, timeouts
- Do NOT include frontmatter — just the markdown content starting with # Title

Write the documentation now:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()


def build_frontmatter(plan: dict) -> str:
    """Builds the YAML frontmatter for a document."""
    return f"""---
source_name: {plan['source_name']}
section: {plan['section']}
last_updated: "2024-03-01"
doc_type: {plan['doc_type']}
access_level: public
---"""


def run():
    """Generates all 50 documents and saves them to docs/."""
    console.print("\n[bold cyan]Generating 50-document corpus...[/bold cyan]")
    console.print("[dim]This will take 10-15 minutes. Each doc is generated by Ollama.[/dim]\n")

    # Create folder structure
    sections = set(p["section"].lower().replace(" ", "_") for p in CORPUS_PLAN)
    for section in sections:
        Path(f"docs/{section}").mkdir(parents=True, exist_ok=True)

    success = 0
    failed  = 0

    for plan in track(CORPUS_PLAN, description="Generating docs..."):
        section_dir = plan["section"].lower().replace(" ", "_")
        file_path   = Path(f"docs/{section_dir}/{plan['source_name']}.md")

        # Skip if already exists
        if file_path.exists():
            console.print(f"[dim]Skipping (exists): {plan['source_name']}[/dim]")
            success += 1
            continue

        try:
            content      = generate_document(plan)
            frontmatter  = build_frontmatter(plan)
            full_doc     = f"{frontmatter}\n\n{content}"

            file_path.write_text(full_doc, encoding="utf-8")
            console.print(f"[green]✓[/green] {plan['source_name']}")
            success += 1

        except Exception as e:
            console.print(f"[red]✗ Failed: {plan['source_name']} — {e}[/red]")
            failed += 1

    console.print(f"\n[bold green]Done! {success} documents generated, {failed} failed.[/bold green]")
    console.print(f"[dim]Documents saved to docs/ folder[/dim]")


if __name__ == "__main__":
    run()
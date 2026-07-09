---
source_name: security-policy
section: Security
last_updated: "2024-03-01"
doc_type: policy
access_level: public
---

# Responsible Disclosure Policy

DevAPI is committed to maintaining the highest standards of security and transparency. Our responsible disclosure policy ensures that when a security vulnerability or bug is discovered, we take swift action to address it while also respecting the rights of the researcher who identified it.

## How to Report a Vulnerability

To report a vulnerability, please submit a detailed description of the issue, including any relevant technical details or proof-of-concept code. Please use the following format:

- **Format:** Email with subject "Security Vulnerability Report"
- **Content:**
  ```markdown
# Vulnerability Report

* **Vulnerability Title:** [Insert title]
* **Description:** [Insert description]
* **Severity:** High/Medium/Low
* **Reproduce Steps:** [Insert steps to reproduce the issue]
```
Our dedicated security team will review your report and respond within 72 hours. Please note that all reports are kept confidential until a fix is released.

## Bug Bounty Program

DevAPI operates a bug bounty program, which incentivizes responsible security researchers to identify vulnerabilities in our systems. To participate in the bug bounty program, submit a detailed description of the issue, including any relevant technical details or proof-of-concept code, via the following channels:

- **Format:** JSON payload with following fields
  ```json
{
    "title": "Vulnerability Title",
    "description": "Vulnerability Description",
    "severity": "High/Medium/Low",
    "reproduceSteps": "Reproduce Steps",
    "proofOfConcept": "Optional: Proof of concept code"
}
```
Rewards will be issued based on the severity and impact of the vulnerability. For more information, please refer to our [Bug Bounty Program Terms and Conditions](https://example.com/bug-bounty-terms).

## Security Incident Response

In the event of a security incident, DevAPI's incident response team will activate the following protocols:

- **Initial Response:** Within 24 hours, our incident response team will assess the situation and notify affected users.
- **Communication:** We will provide regular updates to impacted users via email or other channels as necessary.
- **Response Timeframe:** Our goal is to respond within 72 hours of identifying an incident.

## Data Breach Notification

In the event of a data breach, DevAPI will comply with applicable laws and regulations, including GDPR and CCPA. We will notify affected individuals and organizations within the required timeframe:

- **GDPR:** Within 72 hours
- **CCPA:** Within 30 days
- **Data breach notification format:**
  ```markdown
# Data Breach Notification

* **Data Elements Disclosed:** [Insert data elements disclosed]
* **Duration of Disclosure:** [Insert duration of disclosure]
```
Please note that our data breach notification policy is subject to change.
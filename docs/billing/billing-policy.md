---
source_name: billing-policy
section: Billing
last_updated: "2024-03-01"
doc_type: policy
access_level: public
---

# Billing Policy: Payment Terms and Consequences

## Payment Terms (Net 30)

All outstanding invoices must be paid within 30 days of receipt. Payments can be made via bank transfer, credit card, or check. DevAPI reserves the right to adjust payment terms with written notice.

Payment due dates are as follows:

* Payment is due on the date specified in the invoice.
* A late payment charge of 2% per month will be applied to outstanding balances.

Example request: `GET /invoices/{invoiceId}/due-date` returns a JSON object containing the due date for the specified invoice. Response status code: 200 OK.

## Late Payment Consequences

Late payments will incur additional charges as follows:

* First instance of late payment: $25
* Second and subsequent instances: $50
* Unpaid balances exceeding 90 days: DevAPI reserves the right to suspend or terminate accounts.

Example response for a late payment: `POST /invoices/{invoiceId}/late-fee` returns a JSON object containing the updated balance and late fee amount. Response status code: 202 Accepted (if request is successful) or 400 Bad Request (if invalid request).

## Refund Policy

DevAPI does not offer refunds for any reason, including but not limited to cancellations, requests for refunds within 30 days of invoice issuance.

Example request: `GET /invoices/{invoiceId}/refund` returns a JSON object indicating that no refund is possible. Response status code: 400 Bad Request.

## Account Suspension

DevAPI reserves the right to suspend or terminate accounts that are 90+ days in arrears, in accordance with our payment terms policy.

Example request to retrieve account suspension status: `GET /accounts/{accountId}/suspension-status` returns a JSON object containing the suspension status and reason. Response status code: 200 OK.

Note: API request timeouts are set at 60 seconds for all requests. Failure to respond within this time frame will result in a timeout error with response status code 408 Request Timeout.
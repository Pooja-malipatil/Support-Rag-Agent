---
source_name: billing-faq
section: Billing
last_updated: "2024-03-01"
doc_type: faq
access_level: public
---

# Billing FAQ

## What counts as a billable request?

A billable request is any API call that results in a visible change to your data or returns data that you can use. Examples of billable requests include:

* Creating, reading, updating, or deleting (CRUD) operations on resources such as users, projects, or files.
* Executing business logic operations such as sending emails, making payments, or generating reports.

Non-billable requests include things like retrieving metadata, testing API endpoints, or logging requests. These types of requests are still considered part of your usage and will be counted towards your billable limit. For more information on the current billable limit per user, see [User Limits](https://devapi.com/docs/user-limits).

## Upgrading or Downgrading Your Plan

To upgrade or downgrade your plan, you can use the following HTTP requests:

* `PATCH /users/me/plans` to update your plan: `curl -X PATCH \
  https://example.devapi.com/api/users/me/plans \
  -H 'Content-Type: application/json' \
  -d '{"plan_id": "new_plan_id"}'`

This will upgrade your plan to the new plan ID.

* `PATCH /users/me/plans` to downgrade your plan: `curl -X PATCH \
  https://example.devapi.com/api/users/me/plans \
  -H 'Content-Type: application/json' \
  -d '{"plan_id": "old_plan_id"}'`

This will downgrade your plan to the old plan ID.

If you are unable to make the request within the timeout period (30 seconds), an HTTP error will be returned. For more information on available HTTP status codes, see [HTTP Status Codes](https://devapi.com/docs/http-status-codes).

## Prorated Charges

Prorated charges apply when you downgrade your plan. The amount of prorated charge is calculated based on the difference between the original and new plan limits.

For example, if you were originally on a $1000/month plan with 10,000 requests, but downgraded to a $500/month plan with 5,000 requests, your prorated charge would be:

$1000 - ($500 / (10,000 / 5,000)) * (number of days since downgrade)

You can calculate the exact amount using our [Billing Calculator](https://devapi.com/billing-calculator).

## Invoice Disputes

If you have an invoice dispute, please contact our billing team at [support@devapi.com](mailto:support@devapi.com) with a detailed explanation of the issue. We will review your case and respond within 3-5 business days.

We require a valid reason for disputing an invoice, such as:

* An error in the charge amount
* A duplicate charge
* A charge that was not authorized

Please include any relevant documentation or evidence to support your dispute.

Note: The above examples are fictional and used only for demonstration purposes.
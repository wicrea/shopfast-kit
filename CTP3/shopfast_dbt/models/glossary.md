{% docs gross_revenue %}
**Gross revenue (EUR)** — total amount paid by the customer for an order, VAT included, shipping included, before refunds.
Owner: Head of Sales · Steward: Karim Benali · Status: approved (2026-11-10)
{% enddocs %}

{% docs net_revenue %}
**Net revenue (EUR)** — gross revenue minus refunded amounts, for the order. Excludes cancelled orders. This is the revenue figure used by the Finance report. Expressed as a decimal amount (not cents).
Owner: Head of Sales · Steward: Karim Benali · Status: approved (2026-11-10)
{% enddocs %}

{% docs active_customer %}
**Active customer** — a customer who has placed at least one non-cancelled order in the last 90 days. Used for retention and engagement reporting.
Owner: Head of Sales · Steward: Karim Benali · Status: approved (2026-11-10)
{% enddocs %}

{% docs churned_customer %}
**Churned customer** — a customer with no non-cancelled order in the last 365 days, who had at least one order before. Used for churn analysis and win-back campaigns.
Owner: Head of Sales · Steward: Karim Benali · Status: approved (2026-11-10)
{% enddocs %}

{% docs order %}
**Order** — a purchase placed by a customer account on a given date, through a single sales channel. One order can contain several product lines and several payment events.
Owner: Head of Sales · Steward: Karim Benali · Status: approved (2026-11-10)
{% enddocs %}

{% docs customer %}
**Customer** — a customer account in the shop. One person may hold several accounts; identity is keyed by customer_id, not by email. Personal data (name, email, phone, birth date, city) is classified confidential or restricted.
Owner: Head of Sales · Steward: Karim Benali · Status: approved (2026-11-10)
{% enddocs %}

{# TODO (Exercise 3): add the terms net_revenue, active_customer, churned_customer, order, customer #}
{# -> fait ci-dessus : les 5 doc blocks sont ajoutés. #}
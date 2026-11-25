# Impact — stg_payments.amount switches from cents to EUR

**What breaks:** anything reading `stg_payments.amount` assumes cents. In decimal EUR, `fct_orders` (net/gross revenue), the Finance report and the Sales dashboard see revenue ×100. Filters like `amount > 100` and `/100` conversions in SQL/BI break too.

**Who to warn:** Sara Martin (Sales, owns `fct_orders` and the reports), Karim Benali (steward of `stg_payments`), the Finance team consuming the monthly report, and the payments team to confirm the date and backfill.

**Test to add:** a reconciliation test `sum(stg_payments.amount) = sum(fct_orders.net_revenue_eur)` over a closed period, plus a type/range check on `amount` to catch a silent unit flip.

**Who approves:** Sara Martin (business) and Karim Benali (data) sign off; the payments lead approves the source-side change and the cut-over date.

**Rollout:** announce 5 days ahead, ship the change and the reconciliation test in the same PR, keep `amount_cents` for one release, monitor revenue for 24h before dropping the old column.
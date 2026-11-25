# In my head, not yet in the code

- **`stg_payments.amount` unit is unresolved.** Docs say cents, preview shows 217.38. I haven't read the SQL. Until I do, the docs lie.
- **No reconciliation test** between `sum(stg_payments.amount)` and `sum(fct_orders.gross_revenue_eur)`. That's the test that would have caught the cents bug.
- **`active_customer` / `churned_customer` doc blocks are orphaned** — no `is_active` / `is_churned` column exists.
- **`fct_orders` has no `meta.steward`** while the glossary credits Karim as steward.
- **`payment_date`, `method`, `card_last4`, `payment_status` aren't documented** in `_staging.yml`.
- **`status` enum is duplicated** in two YAML files — no single source of truth.
- **The data dictionary is hand-written**, not generated from `manifest.json`. It'll drift.
- **`card_last4` classification** (`confidential` vs `restricted`) is undecided.
- **`country_code` not tagged PII** is a deliberate call, but it's undocumented.

If I only fix one: **settle the `amount` unit and add the reconciliation test.**
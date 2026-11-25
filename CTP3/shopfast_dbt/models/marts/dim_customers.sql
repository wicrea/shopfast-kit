-- One row per customer with lifetime metrics.
select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.country_code,
    c.loyalty_tier,
    c.signup_date,
    c.has_marketing_consent,
    count(o.order_id)                          as lifetime_orders,
    max(o.order_date)                          as last_order_date,
    coalesce(sum(o.net_revenue_eur), 0)        as lifetime_net_revenue_eur
from {{ ref('stg_customers') }} c
left join {{ ref('fct_orders') }} o using (customer_id)
group by all

-- One row per order with its payment, used by the Sales dashboard and the Finance report.
with pay as (
    select order_id,
           sum(case when payment_status = 'captured' then amount else 0 end) as amount_captured,
           sum(case when payment_status = 'refunded' then amount else 0 end) as amount_refunded
    from {{ ref('stg_payments') }}
    group by order_id
)
select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.channel,
    o.shipping_country,
    o.total_amount_eur                                   as gross_revenue_eur,
    coalesce(p.amount_refunded, 0)                       as refunded_eur,
    round((o.total_amount_eur - coalesce(p.amount_refunded, 0)) / 1.20, 2) as net_revenue_eur
from {{ ref('stg_orders') }} o
left join pay p using (order_id)

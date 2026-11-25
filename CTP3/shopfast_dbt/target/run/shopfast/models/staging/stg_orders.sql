
  
  create view "shopfast"."main"."stg_orders__dbt_tmp" as (
    -- One row per order. Duplicate order_ids are removed (first occurrence kept).
with src as (
    select *, row_number() over (partition by order_id order by order_date) as rn
    from read_csv('../../data/orders.csv', header=true, all_varchar=true)
)
select
    cast(order_id as integer)                    as order_id,
    cast(customer_id as integer)                 as customer_id,
    try_cast(order_date as date)                 as order_date,
    case lower(trim(status)) when 'canceled' then 'cancelled' else lower(trim(status)) end as status,
    channel,
    shipping_country,
    cast(total_amount_eur as decimal(10,2))      as total_amount_eur
from src
where rn = 1
  );

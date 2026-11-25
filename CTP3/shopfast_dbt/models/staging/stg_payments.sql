select
    cast(payment_id as integer)        as payment_id,
    cast(order_id as integer)          as order_id,
    try_cast(payment_date as date)     as payment_date,
    method,
    cast(amount as decimal(12,2))      as amount,
    currency,
    card_last4,
    status                             as payment_status
from {{ source('shopfast_raw', 'payments') }}

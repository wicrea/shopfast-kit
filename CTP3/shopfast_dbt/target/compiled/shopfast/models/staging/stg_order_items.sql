select
    cast(order_item_id as integer)     as order_item_id,
    cast(order_id as integer)          as order_id,
    cast(product_id as integer)        as product_id,
    cast(quantity as integer)          as quantity,
    cast(unit_price_eur as decimal(10,2)) as unit_price_eur
from read_csv('../../data/order_items.csv', header=true, all_varchar=true)
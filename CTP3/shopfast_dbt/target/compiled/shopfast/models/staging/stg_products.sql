select
    cast(product_id as integer)                  as product_id,
    sku,
    product_name,
    (upper(substr(trim(category), 1, 1)) || lower(substr(trim(category), 2)))                      as category,
    try_cast(unit_price_eur as decimal(10,2))    as list_price_eur,
    supplier,
    is_active = 'Y'                              as is_active
from read_csv('../../data/products.csv', header=true, all_varchar=true)
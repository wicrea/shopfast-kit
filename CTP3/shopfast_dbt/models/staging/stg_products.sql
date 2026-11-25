select
    cast(product_id as integer)                  as product_id,
    sku,
    product_name,
    {{ proper_case("category") }}                      as category,
    try_cast(unit_price_eur as decimal(10,2))    as list_price_eur,
    supplier,
    is_active = 'Y'                              as is_active
from {{ source('shopfast_raw', 'products') }}

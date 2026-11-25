-- One row per customer account, cleaned (same rules as the OpenRefine recipe of CTP 2)
with src as (
    select distinct * from {{ source('shopfast_raw', 'customers') }}   -- removes exact duplicate rows
)
select
    cast(customer_id as integer)                                   as customer_id,
    {{ proper_case("first_name") }}                                    as first_name,
    {{ proper_case("last_name") }}                                     as last_name,
    lower(trim(email))                                             as email,
    phone,
    coalesce(try_strptime(birth_date, '%Y-%m-%d'), try_strptime(birth_date, '%d/%m/%Y'),
             try_strptime(birth_date, '%m-%d-%Y'), try_strptime(birth_date, '%Y/%m/%d'))::date   as birth_date,
    city,
    case when upper(trim(country)) in ('FR','FRANCE','FRA') then 'FR'
         when upper(trim(country)) in ('DE','GERMANY','ALLEMAGNE','DEU') then 'DE'
         when upper(trim(country)) in ('ES','SPAIN','ESPAGNE') then 'ES'
         when upper(trim(country)) in ('BE','BELGIUM','BELGIQUE','BEL') then 'BE' end   as country_code,
    coalesce(try_strptime(signup_date, '%Y-%m-%d'), try_strptime(signup_date, '%d/%m/%Y'),
             try_strptime(signup_date, '%m-%d-%Y'), try_strptime(signup_date, '%Y/%m/%d'))::date as signup_date,
    marketing_consent = 'true'                                     as has_marketing_consent,
    replace(lower(trim(loyalty_tier)), 'platinium', 'platinum')    as loyalty_tier
from src

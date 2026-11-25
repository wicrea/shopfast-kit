
    
    

with all_values as (

    select
        country_code as value_field,
        count(*) as n_records

    from "shopfast"."main"."stg_customers"
    group by country_code

)

select *
from all_values
where value_field not in (
    'FR','DE','ES','BE'
)



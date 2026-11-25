{# DuckDB has no initcap(): 'MARIE ' -> 'Marie' #}
{% macro proper_case(col) -%}
    (upper(substr(trim({{ col }}), 1, 1)) || lower(substr(trim({{ col }}), 2)))
{%- endmacro %}

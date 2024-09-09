{% macro remove_pts() %}

DELETE FROM dbt_omop.gold.person
WHERE person_id NOT IN (SELECT person_id FROM dbt_omop.gold.observation_period);

DELETE FROM dbt_omop.gold.death
WHERE person_id NOT IN (SELECT person_id FROM dbt_omop.gold.observation_period);

{% endmacro %}

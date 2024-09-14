from sqlmesh import macro, SQL, ExecutionContext
import sqlglot.expressions as exp
from sqlglot import select, condition, case


@macro()
def get_observation_period(
    evaluator: ExecutionContext,
    model: exp.Table,
    start_date: exp.Column,
    end_date: exp.Column,
) -> str:

    minimum_observation_period_start_date = evaluator.var(
        "minimum_observation_period_start_date"
    )

    # where = condition("x=1").and_("y=1")
    # select("*").from_("y").where(where).sql()

    # cond_1 = case().when(start_date>=minimum_observation_period_start_date and start_date <= exp.CurrentDate() )
    # fragment = select("*").from_(model).sql()
    fragment = f"""
select
    distinct person_id ,
    coalesce(observation_period_start_date, observation_period_end_date) as observation_period_start_date,
    coalesce(observation_period_end_date, observation_period_start_date) as observation_period_end_date
  from
    (
    select
        t.person_id ,
        case
            when
              {start_date}::DATE >= '{minimum_observation_period_start_date}'
              and {start_date}::DATE <= current_date
              then {start_date}
            else null
        end as observation_period_start_date,
        case
            when {end_date}::DATE >= '{minimum_observation_period_start_date}'
            and {end_date}::DATE <= current_date
            then {end_date}
            else null
        end as observation_period_end_date
    from {model} as t
    )
  where
    observation_period_start_date is not null
    or observation_period_end_date is not null
"""
    return fragment


@macro()
def get_observation_period_alternative(
    evaluator: ExecutionContext,
    model: exp.Table,
    start_date: exp.Column,
    end_date: exp.Column,
):

    exp.Condition()
    cond_1: exp.Case = (
        case()
        .when(
            condition(
                start_date >= evaluator.var("minimum_observation_period_start_date")
            ).and_(start_date <= exp.CurrentDate()),
            start_date,
        )
        .else_(condition=exp.null())
        .as_("observation_period_start_date")
    )
    cond_2: exp.Case = (
        case()
        .when(
            condition(
                end_date >= evaluator.var("minimum_observation_period_start_date")
            ).and_(end_date <= exp.CurrentDate()),
            end_date,
        )
        .else_(condition=exp.null())
        .as_("observation_period_end_date")
    )

    subquery1 = select("person_id", cond_1, cond_2).from_(model).distinct()

    # print(subquery1)

    return cond_1, cond_2

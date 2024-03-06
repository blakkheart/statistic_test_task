from datetime import date
from typing import List

from fastapi import APIRouter, Query, Response, status
from sqlalchemy import select, and_, case, Numeric, delete
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import cast

from src.database.db import async_session_factory
from src.statistic.models import Statistic
import src.statistic.schemas as schemas


router = APIRouter(tags=['statistic'])


@router.get('/')
async def get_statistic(
    from_: date = Query(..., alias='from'), to: date = Query(...)
) -> List[schemas.StatisticRead]:
    async with async_session_factory() as session:
        query = (
            select(
                Statistic.date,
                func.sum(Statistic.views).label('views'),
                func.sum(Statistic.clicks).label('clicks'),
                func.round(func.avg(cast(Statistic.cost, Numeric)), 2).label('cost'),
                case(
                    (
                        func.sum(Statistic.clicks) > 0,
                        func.round(
                            cast((func.avg(Statistic.cost) / func.sum(Statistic.clicks)), Numeric),
                            2,
                        ),
                    ),
                    else_=0,
                ).label('cps'),
                case(
                    (
                        func.sum(Statistic.views) > 0,
                        func.round(
                            cast((func.avg(Statistic.cost) / func.sum(Statistic.views)), Numeric),
                            2,
                        ),
                    ),
                    else_=0,
                ).label('cpm'),
            )
            .where(and_(Statistic.date >= from_, Statistic.date <= to))
            .group_by(
                Statistic.date,
            )
            .order_by(Statistic.date)
        )
        result = await session.execute(query)
        statistics = list(result.mappings())
        return statistics


@router.post('/')
async def post_statistic(statistic: schemas.StatisticCreate) -> schemas.Statistic:
    async with async_session_factory() as session:
        db_statistic = Statistic(**statistic.model_dump())
        session.add(db_statistic)
        await session.commit()
        await session.refresh(db_statistic)
        return db_statistic


@router.delete('/')
async def delete_statistic() -> Response:
    async with async_session_factory() as session:
        query = delete(Statistic)
        await session.execute(query)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

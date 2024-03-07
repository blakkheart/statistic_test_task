from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy import and_, case, delete, select, Numeric
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import cast
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session
from src.statistic.models import Statistic
import src.statistic.schemas as schemas


router = APIRouter(tags=['statistic'])


@router.get('/', status_code=200)
async def get_statistic(
    session: AsyncSession = Depends(get_async_session),
    from_: date = Query(..., alias='from'),
    to: date = Query(...),
    sort_by: str = 'date',
) -> List[schemas.StatisticRead]:
    """Получение статистики.
    Принимает search параметры дату from и дату to, а также опциональный
    параметр sort_by, позволяющий сортировать данные."""

    query = (
        select(
            Statistic.date.label('date'),
            func.sum(Statistic.views).label('views'),
            func.sum(Statistic.clicks).label('clicks'),
            func.round(func.avg(cast(Statistic.cost, Numeric)), 2).label('cost'),
            case(
                (
                    func.sum(Statistic.clicks) > 0,
                    func.round(
                        cast(
                            (func.avg(Statistic.cost) / func.sum(Statistic.clicks)),
                            Numeric,
                        ),
                        2,
                    ),
                ),
                else_=0,
            ).label('cps'),
            case(
                (
                    func.sum(Statistic.views) > 0,
                    func.round(
                        cast(
                            (
                                func.avg(Statistic.cost)
                                / (func.sum(Statistic.views) * 1000)
                            ),
                            Numeric,
                        ),
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
        .order_by(sort_by)
    )
    result = await session.execute(query)
    statistics = list(result.mappings())
    return statistics


@router.post('/', status_code=201)
async def post_statistic(
    statistic: schemas.StatisticCreate,
    session: AsyncSession = Depends(get_async_session),
) -> schemas.Statistic:
    """Сохранение статистики."""

    db_statistic = Statistic(**statistic.model_dump())
    session.add(db_statistic)
    await session.commit()
    await session.refresh(db_statistic)
    return db_statistic


@router.delete('/', status_code=204)
async def delete_statistic(
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    """Удаление статистики."""

    query = delete(Statistic)
    await session.execute(query)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

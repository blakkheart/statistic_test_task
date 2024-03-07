from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StatisticCreate(BaseModel):
    date: date
    views: Optional[int] = None
    clicks: Optional[int] = None
    cost: Optional[float] = None


class Statistic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    views: Optional[int] = None
    clicks: Optional[int] = None
    cost: Optional[float] = None


class StatisticRead(BaseModel):
    date: date
    views: Optional[int] = None
    clicks: Optional[int] = None
    cost: Optional[float] = None
    cps: Optional[float] = 0
    cpm: Optional[float] = 0

import datetime

from pydantic import BaseModel, Field

LOCALITIES = [
    "Łódź Bałuty",
    "Łódź Górna",
    "Łódź Śródmieście",
    "Łódź Widzew",
    "Łódź Polesie",
]


class PredictRequest(BaseModel):
    area_m2: float = Field(..., gt=0, le=500, example=50.0)
    rooms: int = Field(..., ge=1, le=10, example=3)
    photos: int = Field(10, ge=0, le=100, example=10)
    owner_direct: bool = Field(True, example=True)
    locality: str = Field(..., example="Łódź Śródmieście")
    date_posted: datetime.date = Field(default_factory=datetime.date.today)
    street: str | None = Field(None, example=None)


class PredictResponse(BaseModel):
    price_zl: float
    price_per_m2_zl: float
    locality: str
    area_m2: float

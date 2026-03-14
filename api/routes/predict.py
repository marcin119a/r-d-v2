from fastapi import APIRouter

from api.model import predict_price
from api.schemas import PredictRequest, PredictResponse

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    price = predict_price(
        area_m2=req.area_m2,
        rooms=req.rooms,
        photos=req.photos,
        locality=req.locality,
        owner_direct=req.owner_direct,
        date_posted=req.date_posted.strftime("%Y-%m-%d"),
        street=req.street,
    )
    return PredictResponse(
        price_zl=round(price, 2),
        price_per_m2_zl=round(price / req.area_m2, 2),
        locality=req.locality,
        area_m2=req.area_m2,
    )

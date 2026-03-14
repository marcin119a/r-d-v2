from fastapi import APIRouter

from api.schemas import LOCALITIES

router = APIRouter()


@router.get("/localities")
def localities():
    return {"localities": LOCALITIES}

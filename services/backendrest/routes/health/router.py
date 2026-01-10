from fastapi import APIRouter


router = APIRouter(tags=["Health"])


@router.get(
    path="/ping",
    summary="Пинг работы API.",
)
async def ping() -> str:
    return "pong"

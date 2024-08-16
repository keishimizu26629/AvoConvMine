from fastapi import APIRouter, Depends
from app.utils.jwt import get_current_user_id

router = APIRouter()

@router.get("/test-auth")
async def test_auth(current_user_id: int = Depends(get_current_user_id)):
    return {"message": "認証成功", "user_id": current_user_id}

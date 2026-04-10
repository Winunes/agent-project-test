from fastapi import APIRouter

# 这个 router 专门放健康检查接口
router = APIRouter(tags=["health"])

# GET /health/：健康检查接口，返回一个简单的状态信息。
@router.get("/")
async def health_check():
    # 返回一个最小可用状态，方便本地和部署探活
    return {"status": "ok"}

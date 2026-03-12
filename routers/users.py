from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_cfg import get_database
from crud import users
from models.users import User
from schemas.users import UserAuthResponse, UserChangePasswordRequest, UserInfoResponse, UserRequest, UserUpdateRequest
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/register")
async def register(data: UserRequest, db: AsyncSession = Depends(get_database)):
    existed = await users.get_user_by_username(db, data.username)
    if existed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

    try:
        user = await users.create_user(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    token = await users.create_token(db, user.id)

    resp = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=resp)


@router.post("/login")
async def login(data: UserRequest, db: AsyncSession = Depends(get_database)):
    user = await users.authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码错误")

    token = await users.create_token(db, user.id)
    resp = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功", data=resp)


@router.get("/info")
async def info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))


@router.put("/update")
async def update_user_info(
    data: UserUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_database),
):
    updated = await users.update_user(db, user.username, data)
    return success_response(message="更新用户信息成功", data=UserInfoResponse.model_validate(updated))


@router.put("/password")
async def change_password(
    data: UserChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_database),
):
    try:
        ok = await users.change_password(db, user, data.old_password, data.new_password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="旧密码错误")

    return success_response(message="修改密码成功")

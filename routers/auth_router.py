from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import EmailStr
from typing import Annotated
from dependencies import get_mail, get_session
from fastapi_mail import FastMail, MessageSchema, MessageType
from models import AsyncSession
import string
import random
from models.user import User
from aiosmtplib import SMTPResponseException
from fastapi import Depends
from repository.user_repo import EmailCodeRepository, UserRepository
from schemas import ResponseOut
from schemas.user import RegisterIn, UserCreateSchema,LoginIn, LoginOut
from core.auth import AuthHandler



router = APIRouter(prefix = "/auth", tags = ["user"])

auth_handler = AuthHandler()

@router.get("/code", response_model=ResponseOut)
async def get_email_code(
    email: Annotated[EmailStr, Query(...)],
    mail: FastMail = Depends(get_mail),
    session: AsyncSession = Depends(get_session)
):
    #生成4位数验证码
    source = string.digits * 4
    code = "".join(random.sample(source, 4))
    #创建消息对象
    message = MessageSchema(
        subject = "验证码",
        recipients = [email],
        body = f"验证码为：{code}",
        subtype = MessageType.plain
    )
    try:
        await mail.send_message(message)
    except SMTPResponseException as e:
        if e.code == -1 and b"\\x00\\x00\\x00" in str(e).encode():
            print("忽略qq邮箱 SMTP 关闭阶段的非标志响应")
            #将邮箱和验证码存在数据库中
            email_code_repo = EmailCodeRepository(session=session)
            await email_code_repo.create(str(email), code)
        else:
            raise HTTPException(status_code=500, detail="邮件发送失败")
    return ResponseOut

@router.post("/register", response_model=ResponseOut)
async def register(
    data: RegisterIn,
    session: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(session=session)
    #校验邮箱是否存在
    email_exist = await user_repo.email_is_exist(email = str(data.email))
    if email_exist:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    #校验验证码是否正确
    email_code_repo = EmailCodeRepository(session=session)
    email_code_match =  email_code_repo.check_email_code(email=str(data.email), code=str(data.code))
    if not email_code_match:
        raise HTTPException(400, detail="验证码错误")
    try:
        await user_repo.create(UserCreateSchema(email=str(data.email), password=data.password, username=data.username))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ResponseOut()

@router.post("/login", response_model=LoginOut)
async def login(
    data: LoginIn,
    session: AsyncSession = Depends(get_session)
):
    #创建user_repo对象
    user_repo = UserRepository(session=session)
    #根据邮箱查找用户
    user: User|None = await user_repo.get_by_email(str(data.email))
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")
    if not user.check_password(data.password):
        raise HTTPException(status_code=400, detail="密码错误")
    #生成token
    tokens = auth_handler.encode_login_token(user.id)
    return {
        "user": user,
        "token": tokens['access_token']
    }





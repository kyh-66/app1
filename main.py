from fastapi import FastAPI
from fastapi_mail import FastMail,MessageSchema,MessageType
from fastapi import Depends
from dependencies import get_mail
from aiosmtplib import SMTPResponseException
from routers.auth_router import router as auth_router
from routers.name_router import router as name_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(name_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/mail/test")
async def mail_test(
        email: str,
        mail: FastMail = Depends(get_mail),

):
    message = MessageSchema(
        subject="测试邮件",
        recipients=[email],
        body=f"hello{email}",
        subtype = MessageType.plain#子类型

    )
    try:

        await mail.send_message(message)#异步等待
    except SMTPResponseException as e:
        if e.code == -1 and b"\\x00\\x00\\x00" in str(e).encode():
            print("忽略QQ邮箱SMTP关闭阶段的非标准响应（邮件已成功发送）")
    return {"message": "发送成功"}

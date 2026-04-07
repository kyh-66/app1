from datetime import timedelta

DB_URI = "mysql+aiomysql://root:123456@127.0.0.1:3306/zhiliao_ainame?charset=utf8mb4"


#邮箱
MAIL_USERNAME = "3493598861@qq.com"
MAIL_PASSWORD = "sfmqivayuifzchcd"
MAIL_FROM = "3493598861@qq.com"
MAIL_PORT = 587
MAIL_SERVER = "smtp.qq.com"
MAIL_FROM_NAME = "知了课堂"
MAIL_STARTTLS = True
MAIL_SSL_TLS = False

JWT_SECRET_KEY = "secret"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days = 15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days = 30)
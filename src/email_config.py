from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="patidardharmendra830@gmail.com",  
    MAIL_PASSWORD="tafd yfhf hvyg wxty",  
    MAIL_FROM="patidardharmendra830@gmail.com",  
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,   
    MAIL_SSL_TLS=False, 
    USE_CREDENTIALS=True
)

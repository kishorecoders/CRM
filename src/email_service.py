from fastapi_mail import FastMail, MessageSchema
from src.email_config import conf  # Import email settings


async def send_welcome_email(email: str, full_name: str , newform:object):
    message = MessageSchema(
        subject="Welcome to WingStair-World!",
        recipients=[email],
        body=f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
            <p>Hi <b>{full_name}</b>,</p>

            <h2 style="color: #d9534f;">Welcome to  WingStair-World!! 🎉</h2>

            <p>Your registration has been successfully created. Our support team will contact you as soon as possible.</p>

            <h3>Here are your registration details:</h3>
            <ul>
                <li><b>Name:</b> {full_name}</li>
                <li><b>Email ID:</b> {email}</li>
                <li><b>Password:</b> {newform.password}</li>
                <li><b>Created Date:</b>{newform.created_at}</li>
                <li><b>Plan Type:</b> {newform.plan_id}</li>
                <li><b>Free Trial:</b>{newform.demo_period_day}</li>
                <li><b>Expired Date:</b> {newform.expiry_date}</li>
            </ul>

           

            <p>Thanks<br>
            Onkar Deshpande<br>
            CEO,Wingstair elevator Pvt Ltd.<br>
            behind Bharati Vidyapith School, Shindevadi, Maharashtra 412205</p>

            <h3>WINGSTAIR ELEVATORS PVT. LTD</h3>
            <p>In less than a decade, Wingstair Elevators has risen to become a premier manufacturer of elevators and escalators. Serving both India and international markets, we are celebrated for our precision engineering, innovative solutions, and a commitment to excellence driven by our dedicated team and advanced technology.</p>
            

        </body>
        </html>
        """,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)





async def send_status_update_email(email: str, full_name: str, is_active: bool):
    """
    Sends an email notification when a user's status is updated (Activated/Deactivated).
    """
    if is_active:
        subject = "🎉 Congratulations! Your Account is Now Active!"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
            <h2 style="color: #28a745;">Welcome Back, {full_name}!</h2>
            <li><b>Email ID:</b> {email}</li>
            <li><b>Account Status:</b> {'Active' if is_active else 'Inactive'}</li>
            <p>We are happy to inform you that your account has been successfully activated. You can now log in and enjoy our services.</p>
            <p>If you have any issues, feel free to contact our support team.</p>
            <br>

            <p>Thanks<br>
            Onkar Deshpande<br>
            CEO,Wingstair elevator Pvt Ltd.<br>
            behind Bharati Vidyapith School, Shindevadi, Maharashtra 412205</p>

            <h3>WINGSTAIR ELEVATORS PVT. LTD</h3>
            <p>In less than a decade, Wingstair Elevators has risen to become a premier manufacturer of elevators and escalators. Serving both India and international markets, we are celebrated for our precision engineering, innovative solutions, and a commitment to excellence driven by our dedicated team and advanced technology.</p>
            
        </body>
        </html>
        """
    else:
        subject = "⚠️ Your Account has been Deactivated"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
            <h2 style="color: #d9534f;">Dear {full_name},</h2>
            <li><b>Email ID:</b> {email}</li>
            <li><b>Account Status:</b> {'Active' if is_active else 'Inactive'}</li>
            <p>Your account has been deactivated. If this was a mistake or you need assistance, please contact our support team.</p>
            <p>Thank you for being with WingStair.</p>
            <br>

            <p>Thanks<br>
            Onkar Deshpande<br>
            CEO,Wingstair elevator Pvt Ltd.<br>
            behind Bharati Vidyapith School, Shindevadi, Maharashtra 412205</p>

            <h3>WINGSTAIR ELEVATORS PVT. LTD</h3>
            <p>In less than a decade, Wingstair Elevators has risen to become a premier manufacturer of elevators and escalators. Serving both India and international markets, we are celebrated for our precision engineering, innovative solutions, and a commitment to excellence driven by our dedicated team and advanced technology.</p>
            
        </body>
        </html>
        """

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

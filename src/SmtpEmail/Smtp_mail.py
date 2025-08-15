import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()  # This loads the .env file

# Environment variables for security
sender_email = os.getenv('SENDER_EMAIL')  # Use environment variable for sender email
smtp_username = os.getenv('SMTP_USERNAME')  # Use environment variable for SMTP username
smtp_password = os.getenv('SMTP_PASSWORD')  # Use environment variable for SMTP password
smtp_server = "smtp-relay.brevo.com"
smtp_port = 587

def send_login_email(to_email: str, subject: str, body: str):
    # Check if environment variables are set
    if not sender_email or not smtp_password:
        print("Error: Missing environment variables for email or password.")
        exit(1)

    # Create the MIMEText object
    msg = MIMEMultipart()
    # msg['From'] = sender_email
    msg['From'] = f"SphuritCRM <anantkaaldeveloper@gmail.com>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create an SMTP session and start TLS for secure communication
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

def send_password_reset_confirmation_email(email: str, full_name: str):
    subject = "Password Reset Confirmation - SphuritCRM"
    body = f"""Hello {full_name},

Your password has been successfully reset.

If you did not perform this action, please contact support immediately.

Regards,  
SphuritCRM Team
"""
    send_login_email(
        to_email=email,
        subject=subject,
        body=body
    )


import os
import smtplib
import requests
import tempfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_rqf(to_email: str, subject: str, body: str, attachment_path: str = None):
    if not sender_email or not smtp_password:
        print("Error: Missing environment variables for email or password.")
        exit(1)

    msg = MIMEMultipart()
    msg['From'] = f"SphuritCRM <{sender_email}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    temp_file_path = None

    # Handle attachment: remote URL or local file
    if attachment_path:
        is_url = attachment_path.startswith("http://") or attachment_path.startswith("https://")
        try:
            if is_url:
                # Download the file temporarily
                response = requests.get(attachment_path)
                response.raise_for_status()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(response.content)
                    temp_file_path = tmp_file.name
                    filename = os.path.basename(attachment_path)
            else:
                if not os.path.exists(attachment_path):
                    raise FileNotFoundError(f"File does not exist: {attachment_path}")
                temp_file_path = attachment_path
                filename = os.path.basename(attachment_path)

            # Attach the file
            with open(temp_file_path, "rb") as f:
                part = MIMEApplication(f.read(), _subtype="pdf")
                part.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=filename
                )
                msg.attach(part)
        except Exception as e:
            print(f"Attachment error: {e}")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Email send error: {e}")
    finally:
        # Clean up temporary file if it was downloaded
        if temp_file_path and is_url and os.path.exists(temp_file_path):
            os.remove(temp_file_path)



# import smtplib
# from email.message import EmailMessage

# def send_login_email(to_email: str, subject: str, body: str):
#     # Replace with your SMTP configuration
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     smtp_username = "tuleshkatre7@gmail.com"
#     smtp_password = "paqk dkvi ermo jsjs"  # Use App Passwords if using Gmail with 2FA

#     msg = EmailMessage()
#     msg["Subject"] = subject
#     msg["From"] = smtp_username
#     msg["To"] = to_email
#     msg.set_content(body)

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(smtp_username, smtp_password)
#             server.send_message(msg)
#         return True
#     except Exception as e:
#         print(f"Email sending failed: {e}")
#         return False




# def send_password_reset_confirmation_email(email: str, full_name: str):
#     subject = "Password Reset Confirmation - SphuritCRM"
#     body = f"""Hello {full_name},

# Your password has been successfully reset.

# If you did not perform this action, please contact support immediately.

# Regards,  
# SphuritCRM Team
# """
#     send_login_email(
#         to_email=email,
#         subject=subject,
#         body=body
#     )

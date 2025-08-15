import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Environment variables for security
sender_email = "anantkaaldeveloper@gmail.com"
username = "7560cc001@smtp-brevo.com"
sender_password = "tY41hIz3s08jdHxn"
smtp_server = "smtp-relay.brevo.com"
smtp_port = 587

# Check if environment variables are set
if not sender_email or not sender_password:
    print("Error: Missing environment variables for email or password.")
    exit(1)

# Email content
receiver_email = "vraj.anantkaal@gmail.com"
subject = "Secure Email Test"
body = "This is a test email sent securely from a cPanel-based web server."

# Create the MIMEText object
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

try:
    # Create an SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)  # SSL connection
    server.login(username, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from cryptography.fernet import Fernet
# import os

# # Environment variables for security
# sender_email = "password@sphurit.com"
# sender_password = "Modi@123456"
# smtp_server = "mail.sphurit.com"
# smtp_port = 465

# # Encryption key (in practice, this should be securely stored)
# encryption_key = Fernet.generate_key()
# cipher_suite = Fernet(encryption_key)

# # Encrypt the admin ID (assuming admin_id is known)
# admin_id = 1  # Example admin_id
# encrypted_admin_id = cipher_suite.encrypt(str(admin_id).encode()).decode()

# # Generate the link with the encrypted admin ID
# base_url = "https://yourdomain.com/update-password"  # Replace with your actual URL
# encrypted_link = f"{base_url}?token={encrypted_admin_id}"

# # Email content
# receiver_email = "vraj.anantkaal@gmail.com"
# subject = "Secure Email Test"
# body = f"This is a test email sent securely from a cPanel-based web server. Click the link to update your password: {encrypted_link}"

# # Create the MIMEText object
# msg = MIMEMultipart()
# msg['From'] = sender_email
# msg['To'] = receiver_email
# msg['Subject'] = subject
# msg.attach(MIMEText(body, 'plain'))

# try:
#     # Create an SMTP session
#     server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # SSL connection
#     server.login(sender_email, sender_password)
#     server.sendmail(sender_email, receiver_email, msg.as_string())
#     server.quit()
#     print("Email sent successfully!")
# except Exception as e:
#     print(f"Error: {e}")

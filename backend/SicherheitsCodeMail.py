import smtplib
import ssl

smtp_server = "smtp.office365.com"
port = 587
sender_email = "Your-Mail"
password = "password"


receiver_email = "receiver-mail"
message = """\
Subject: Test Email

Das ist dein Code, willkommen  ..."""

context = ssl.create_default_context()

try:
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login("Your-Mail", "password")
        server.sendmail("Your-Mail", "receiver-mail", message)
        print("Email sent successfully!")
except Exception as e:
    print("Error occurred while sending email:", e)
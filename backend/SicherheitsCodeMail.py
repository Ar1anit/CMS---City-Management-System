import smtplib
import ssl

smtp_server = "smtp.office365.com"
port = 587
sender_email = "nmikhaeel00@gmail.com"
password = "KarpovMikhaeel1"


receiver_email = "SEPVgruppeB@outlook.de"
message = """\
Subject: Test Email

Das ist dein Code, willkommen  ..."""

context = ssl.create_default_context()

try:
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login("SEPVgruppeB@outlook.de", "KarpovMikhaeel1")
        server.sendmail("SEPVgruppeB@outlook.de", "nmikhaeel00@gmail.com", message)
        print("Email sent successfully!")
except Exception as e:
    print("Error occurred while sending email:", e)
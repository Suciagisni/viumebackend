import pyotp
import smtplib
import ssl
import base64
import logging

logging.basicConfig(level=logging.DEBUG)

salt = "@ViuM32k23s3cr3t"

def generate_otp(email):
    email_bytes = email.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    base32_secret = base64.b32encode(email_bytes + salt_bytes)
    totp = pyotp.TOTP(base32_secret, interval=900)
    return totp.now()


def verify_otp(email, otp):
    email_bytes = email.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    base32_secret = base64.b32encode(email_bytes + salt_bytes)
    totp = pyotp.TOTP(base32_secret, interval=900)
    return totp.verify(otp)


def send_otp_email(email, otp):
    smtp_server = "localhost"
    port = 25
    sender_email = "no-reply@yarsi.ai"
    password = "R}4lh5&PK(WK"
    receiver_email = email

    subject = "Viume: Kode Verifikasi (OTP) untuk Verifikasi Identitas"

    message_body = f"""\
    Hi User,

    Kode Verifikasi (OTP) Viume Kamu:

    {otp}

    Berlaku selama 15 Menit. JANGAN BERIKAN kode ini ke siapa pun.

    Best regards,
    Viume Support Team
    """

    message = f"Subject: {subject}\nFrom: {sender_email}\n\n{message_body}"

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.sendmail(sender_email, receiver_email, message)

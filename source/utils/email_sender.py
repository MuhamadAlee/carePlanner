import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.parameters import *



def send_email(to_email, subject, email_content):
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        BODY = f"""
        <html>
        <body>
            <table width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    <td align="left">
                        <img src="cid:logo" alt="CarePlanner Logo" width="100" height="50">
                    </td>
                </tr>
            </table>
            <h2>{subject}</h2>
            <p>Dear,</p>
            <p>{email_content}</p>
            <p>Thank you for choosing CarePlanner.</p>
            <p>Best Regards,<br>CarePlanner Team</p>
            <hr>
            <p>This is an automated message. Please do not reply.</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(BODY, "html"))

        # Establish connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade to secure connection
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")


import os
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
THRESHOLD = 80  # Disk usage percentage threshold
EMAIL_SENDER = "vembu123@gmail.com"
EMAIL_RECEIVER = "vembu321@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "vembu123@gmail.com"
SMTP_PASSWORD = "January@2024"

def get_disk_usage():
    """Returns a list of partitions exceeding the threshold."""
    alert_partitions = []
    partitions = ["/", "/home", "/var", "/tmp"]  # Customize partitions if needed

    for partition in partitions:
        total, used, free = shutil.disk_usage(partition)
        percent_used = (used / total) * 100

        if percent_used > THRESHOLD:
            alert_partitions.append((partition, percent_used))

    return alert_partitions

def send_email(alert_partitions):
    """Sends an email alert if disk usage is above threshold."""
    subject = "Disk Space Alert: High Usage Detected"
    body = "The following partitions have exceeded the disk usage threshold:\n\n"

    for partition, usage in alert_partitions:
        body += f"{partition}: {usage:.2f}% used\n"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    alert_partitions = get_disk_usage()

    if alert_partitions:
        send_email(alert_partitions)
    else:
        print("Disk usage is within limits.")

if __name__ == "__main__":
    main()

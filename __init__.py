import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import timedelta
import requests

import azure.functions as func
import logging

# Gmail hesap bilgileri
sender_email = "krycnylmz@gmail.com"
password = "rvqe mujy sgeh stgu"

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    # subscription key'i kullanarak GET isteği gönderme
    url = "https://prescriptionmanagementsystemresource.azure-api.net/medicine/Medicine/DeleteAndPopulate"
    subscription_key = '8e6b081556e842c99687d44c5ef5ebe3'
    response_text = send_get_request(url, subscription_key)

    # Eğer istek başarılıysa, loglama yapabilirsiniz
    if response_text is not None:
        logging.info(f"GET request response: {response_text}")
    
    sendMail("krycnylmz@gmail.com", "Tüm İlaçlar Güncellendi", "Time:")

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

def sendMail(receiver_email, subject, body):
    # E-posta oluşturma
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    
    # Saat, dakika ve saniye eklenmiş tarih oluşturulması
    now = datetime.datetime.now()
    future_time = now + timedelta(hours=1)
    formatted_time = future_time.strftime("%H:%M:%S")

    # E-posta içeriğinin oluşturulması
    body += f"\nSaat: {formatted_time}"

    msg.attach(MIMEText(body, 'plain'))

    # Gmail SMTP sunucusuna bağlanma ve e-postayı gönderme
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


def send_get_request(url, subscription_key):
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info(f"GET request to {url} successful.")
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending GET request to {url}: {e}")
        return None





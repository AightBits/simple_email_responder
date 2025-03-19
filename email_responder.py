import imaplib
import email
import smtplib
import requests
import time
from email.mime.text import MIMEText

# Email and API Configuration
IMAP_SERVER = "imap.example.com"  # Replace with your email provider's IMAP server
SMTP_SERVER = "smtp.example.com"  # Replace with your email provider's SMTP server
EMAIL_ACCOUNT = "your_email@example.com"
EMAIL_PASSWORD = "your_password"
LLM_API_URL = "https://api.openai.com/v1/chat/completions"  # Replace with compatible API
LLM_API_KEY = ""  # Optional API key
SYSTEM_PROMPT = "You are a helpful AI assistant. Keep responses concise and professional."
MODEL = ""  # Optional model

def fetch_unread_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")
    
    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()
    
    emails = []
    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender = msg["From"]
                subject = msg["Subject"]
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                emails.append((e_id, sender, subject, body))
    
    mail.logout()
    return emails

def call_llm(prompt):
    headers = {"Content-Type": "application/json"}
    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"
    
    data = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    }
    
    if MODEL:
        data["model"] = MODEL
    
    response = requests.post(LLM_API_URL, json=data, headers=headers)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

def send_email(to_email, subject, body):
    if not body:
        return
    
    msg = MIMEText(body)
    msg["Subject"] = "Re: " + subject
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = to_email
    
    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, to_email, msg.as_string())

def main():
    while True:
        try:
            print("Checking for new emails...")
            emails = fetch_unread_emails()
            for e_id, sender, subject, body in emails:
                print(f"Processing email from {sender} with subject: {subject}")
                response_text = call_llm(body)
                send_email(sender, subject, response_text)
                print(f"Replied to {sender} with: {response_text[:50]}...")
            print("Sleeping for 60 seconds...\n")
            time.sleep(60)  # Wait before polling again
        except KeyboardInterrupt:
            print("Polling stopped by user.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

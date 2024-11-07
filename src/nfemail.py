import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("NFEMAIL")
password = os.getenv("NFEMAILPASS")

def read_emails(femail):
    imap_server = "imap.gmail.com"
    nfsubject = ''
    nfbody = ''
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select("inbox")
        status, messages = mail.search(None, f"UNSEEN TO {femail}")
        email_ids = messages[0].split()
        
        for num in email_ids[-1:]:
            status, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")
                    nfsubject = subject

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            try:
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    body = part.get_payload(decode=True).decode()
                                    nfbody = body
                            except Exception as e:
                                print("Error decoding message:", e)
                    else:
                        body = msg.get_payload(decode=True).decode()
                        nfbody = body

        mail.logout()
        return nfsubject, nfbody

    except imaplib.IMAP4.error as e:
        print(f"IMAP connection error: {e}")
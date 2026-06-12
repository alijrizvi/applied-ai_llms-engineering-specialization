# Here, we build a simple, IMAP-based Listener that checks for new Unread emails
# Email Trigger layer

import imapclient
import pyzmail
import os

from dotenv import load_dotenv
load_dotenv()

def check_email():

    host = os.getenv("EMAIL_IMAP")
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    print("\n--- EMAIL DEBUG ---")
    print("HOST:", repr(host))
    print("USER:", repr(user))
    print("PASSWORD LENGTH:", len(password) if password else 0)
    print("-------------------\n")

    imap = imapclient.IMAPClient(host, ssl=True)

    try:
        imap.login(user, password)
        print("✅ Login successful!")

    except Exception as e:
        print(f"❌ Login failed: {e}")
        return None

    imap.select_folder("INBOX")

    ids = imap.search(["UNSEEN"])

    if not ids:
        print("📭 No unread emails found.")
        imap.logout()
        return None

    msg_id = ids[0]

    raw = imap.fetch([msg_id], ["BODY[]"])[msg_id][b"BODY[]"]

    msg = pyzmail.PyzMessage.factory(raw)

    subject = msg.get_subject()

    body = (
        msg.text_part.get_payload().decode(errors="ignore")
        if msg.text_part
        else ""
    )

    sender = msg.get_addresses("from")[0][1]

    imap.logout()

    return {
        "subject": subject,
        "body": body,
        "from": sender
    }
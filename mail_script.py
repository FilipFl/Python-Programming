import smtplib
import imaplib
import email
import ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import os

# task given was to create a script capable of sending email message(with an image attachment) and downloading last mails
# also with an image attachment

my_email = 'example@gmail.com'
receiver = 'example@gmail.com'


def send_message(smtp_handle):
    subject = input("Temat wiadomości: ")
    message_text = "Sprawdzam czy wszystko dziala. Pozdrawiam, Filip"
    message = MIMEMultipart()
    message["From"] = my_email
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(message_text, "plain"))
    file = input("Nazwa załącznika: ")
    with open(file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file}",
    )
    message.attach(part)
    text = message.as_string()
    smtp_handle.sendmail(my_email,receiver,text)


def get_last_message(imap_handle):
    imap_handle.select('Inbox')
    type, data = imap_handle.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    last_mail = id_list[-1]
    result, data = mailbox.fetch(last_mail, "(RFC822)")
    msg = data[0][1].decode('utf-8')
    message = email.message_from_string(msg)
    sender = message['from']
    title = message['title']
    if message.is_multipart():
        mail_content = ''

        for part in message.get_payload():
            if part.get_content_type() == 'text/plain':
                mail_content += part.get_payload()
    else:
        mail_content = message.get_payload()
    return sender, title, mail_content,message

def get_all_emails(imap_handle, emails ):
    imap_handle.select('Inbox')
    type, data = imap_handle.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    for element in id_list:
        result, data = mailbox.fetch(element, "(RFC822)")
        msg = data[0][1].decode('utf-8')
        message = email.message_from_string(msg)
        sender = message['from']
        title = message['subject']
        title = title.encode('utf-8')
        lista = sender.split('<')
        adres = ""
        if len(lista) != 1:
            adres = lista[1]
            adres = adres[:-1]
        else:
            adres = lista[0]
        emails.append([lista[0], adres, title])

def get_attachment(message):
    for part in message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            print(fileName)
            filename = input("Nazwa dla zapisywanego obrazka: ")
            filename += ".jpg"
            DIR = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(DIR, filename)
            if not os.path.isfile(path):
                fp = open(path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()


server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
password = input("Podaj hasło: ")
server.login(my_email, password)
mailbox = imaplib.IMAP4_SSL('imap.gmail.com', 993)
mailbox.login(my_email,password)
print("Zalogowano!")
emails = []
get_all_emails(mailbox, emails)
for element in emails:
    print(element)
send_message(server)
adres = ""
sender, title, content, message = get_last_message(mailbox)
while adres!= my_email:
    sender, title, content, message = get_last_message(mailbox)
    lista = sender.split('<')
    adres = ""
    if len(lista) != 1:
        adres = lista[1]
        adres = adres[:-1]
    else:
        adres = lista[0]
get_attachment(message)




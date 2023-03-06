import os
import smtplib
import imghdr
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

contacts = ['test@gmail.com', 'test1@gmail.com']

msg = EmailMessage()
msg['Subject'] = "Check out these photo's"
msg['From'] = EMAIL_ADDRESS
msg['To'] = ', '.join(contacts)

msg.set_content('This is a plain text email...')

msg.add_alternative('''\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">This is an HTML Email!</h1>
    </body>
</html>
''', subtype='html')


attachments = [
    ('images', ['2.jpg', '3.jpg', '4.jpg'], 'image'),
    ('pdf', ['1.pdf'], 'application'),
]

for path, files, maintype in attachments:
    for file in files:
        file_path = os.path.join(path, file)
        with open(file_path, 'rb') as f:
            file_data = f.read()
            if maintype == 'image':
                file_type = imghdr.what(f.name)
            else:
                file_type = 'octet-stream'
            file_name = os.path.basename(f.name)

        msg.add_attachment(file_data, maintype=maintype, subtype=file_type, filename=file_name)


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

# Watcher Plugin to send e-mail Notifications
# Trigger: Post-processing Finished

import sys
import json
import smtplib
from datetime import datetime
from email.message import EmailMessage
from email import utils

title = sys.argv[1]
new_file = sys.argv[6]
conf_json = sys.argv[11]
conf = json.loads(conf_json)

smtp_server = conf['smtp_server']
smtp_port = conf['smtp_port']
smtp_username = conf['smtp_username']
smtp_password = conf['smtp_password']
smtp_sendtoname = conf['smtp_sendtoname']

msg = EmailMessage()
msg.set_content('{} finished processing on {}:\n {}'.format(title, datetime.now().strftime("%a, %b %d, at %I:%M%p"), new_file))
msg['Subject'] = 'Watcher Finished Processing {}'.format(title)
msg['From'] = smtp_username
msg['To'] = smtp_sendtoname
msg['Date'] = utils.format_datetime(datetime.now())

try:
    if conf['smtp_usessl']:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    else:
        server = smtplib.SMTP(smtp_server, smtp_port)
        try:
            server.starttls()
        except SMTPNotSupportedError:
            pass
    server.login(smtp_username, smtp_password)
    server.send_message(msg)
    server.quit()

except Exception as e:
    print(str(e))
    sys.exit(1)

sys.exit(0)

import os
import smtplib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import html2text

COMMASPACE = ', '


class Mail:
    def __init__(self, **kwargs):
        self.properties = kwargs

    # Subject
    @property
    def subject(self):
        return self.properties.get('subject', 'None')

    @subject.setter
    def subject(self, s):
        self.properties['subject'] = s

    @subject.deleter
    def subject(self):
        del self.properties['subject']

    # Recipients
    @property
    def recipients(self):
        return self.properties.get('recipients', 'None')

    @recipients.setter
    def recipients(self, r):
        self.properties['recipients'] = r

    @recipients.deleter
    def recipients(self):
        del self.properties['recipients']

    # CC
    @property
    def cc(self):
        return self.properties.get('cc', 'None')

    @cc.setter
    def cc(self, r):
        self.properties['cc'] = r

    @cc.deleter
    def cc(self):
        del self.properties['cc']

    # BCC
    @property
    def bcc(self):
        return self.properties.get('bcc', 'None')

    @bcc.setter
    def bcc(self, r):
        self.properties['bcc'] = r

    @bcc.deleter
    def bbc(self):
        del self.properties['bcc']

    # Send From
    @property
    def send_from(self):
        return self.properties.get('send_from', 'None')

    @send_from.setter
    def send_from(self, s_from):
        self.properties['send_from'] = s_from

    @send_from.deleter
    def send_from(self):
        del self.properties['send_from']

    @property
    def smtp_password(self):
        return self.properties.get('smtp_password', 'None')

    @smtp_password.setter
    def gmail_password(self, g_pass):
        self.properties['smtp_password'] = g_pass

    @smtp_password.deleter
    def smtp_password(self):
        del self.properties['smtp_password']

    @property
    def message(self):
        return self.properties.get('message', 'None')

    @message.setter
    def message(self, m):
        self.properties['message'] = m

    @message.deleter
    def message(self):
        del self.properties['message']

    @property
    def attachments(self):
        return self.properties.get('attachments', 'None')

    @attachments.setter
    def attachments(self, a):
        self.properties['attachments'] = a

    @attachments.deleter
    def attachments(self):
        del self.properties['attachments']

    def send_email(self):
        # Create the enclosing (outer) message
        outer = MIMEMultipart('alternative')
        outer['Subject'] = self.subject
        outer['To'] = COMMASPACE.join(self.recipients)
        outer['Cc'] = COMMASPACE.join(self.cc)
        outer['Bcc'] = COMMASPACE.join(self.bcc)
        outer['From'] = self.send_from

        msg = MIMEBase('application', "octet-stream")

        # Add the text of the email
        h = html2text.HTML2Text()
        h.ignore_links = True
        email_plain = MIMEText(h.handle(self.message), 'plain')
        email_html = MIMEText(self.message, 'html')
        outer.attach(email_plain)
        outer.attach(email_html)

        # Add the attachments
        if 1 == 2:
            for file in self.attachments:
                try:
                    with open(file, 'rb') as fp:
                        msg.set_payload(fp.read())
                    encoders.encode_base64(msg)
                    msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                    outer.attach(msg)
                except:
                    print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                    raise

        composed = outer.as_string()

        try:
            with smtplib.SMTP('mail.gandi.net', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(self.send_from, self.smtp_password)
                s.sendmail(self.send_from, self.recipients+self.cc+self.bcc, composed)
                s.close()
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise


def main():
    pass


if __name__ == '__main__':
    main()

from scrapy.utils.project import get_project_settings
from ozBargainer.settings import TARGET_WORDS
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from ast import literal_eval
import time
import os


class Utility(object):

    @staticmethod
    def sendMailToUser():
        filename = os.path.join(os.environ.get("_MEIPASS2", os.path.abspath(os.getcwd())), 'output.txt')
        with open(filename, 'r') as f:
            message = ''
            lines = f.readlines()
            for line in lines:
                target_comment = ''
                line_dict = literal_eval(line)

                if (time.time() - line_dict['time']) < 300:
                    print('Processing data')
                    for target in TARGET_WORDS:
                        target_comment += "\n".join(list(el for el in (line_dict['post'] + line_dict['content']) if target in el))
                        target_comment = target_comment.replace(target, '____ %s ____' % target)
                    # post = "\n".join(line_dict["post"])
                    message += 'Title: %s \nComment: \n%s \nLink: %s \n\n' % (
                    line_dict['title'], target_comment, line_dict['url'])
                else:
                    message += ''
                continue

        if message is not '':
            print('Sending email...')
            Utility.send_mail(message, 'New Price Error Tag!')
        else:
            print('No data returned, waiting for next crawling...')

    @staticmethod
    def send_mail(message, title):
        settings = get_project_settings()
        gmailUser = settings['GMAIL_USER']
        gmailPassword = settings['GMAIL_PASSWORD']

        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = gmailUser
        msg['Subject'] = title
        msg.attach(MIMEText(message))

        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, gmailUser, msg.as_string())
        mailServer.close()
        print("Mail sent")

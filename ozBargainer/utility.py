from scrapy.utils.project import get_project_settings
from ozBargainer.settings import TARGET_PRICE_ERROR
from ozBargainer.settings import TARGET_GOOD_DEAL
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
            price_error_message = ''
            good_deal_message = ''
            lines = f.readlines()
            for line in lines:
                price_error_comment = ''
                good_deal_comment = ''

                line_dict = literal_eval(line.lower())

                if (time.time() - line_dict['time']) < 120:
                    print('Processing data')
                    for target in TARGET_PRICE_ERROR:
                        price_error_comment += "\n".join(list('  - ' + el.capitalize() + '\n' for el in (line_dict['post'] + line_dict['content']) if target in el))
                        price_error_comment = price_error_comment.replace(target, '____ %s ____' % target)
                        if target in line_dict['title']:
                            line_dict['title'] = line_dict['title'].replace(target, '____ %s ____' % target)

                    for target in TARGET_GOOD_DEAL:
                        good_deal_comment += "\n".join(list('  - ' + el.capitalize() + '\n' for el in (line_dict['post'] + line_dict['content']) if target in el))
                        good_deal_comment = good_deal_comment.replace(target, '____ %s ____' % target)
                        if target in line_dict['title']:
                            line_dict['title'] = line_dict['title'].replace(target, '____ %s ____' % target)

                    # post = "\n".join(line_dict["post"])
                    if price_error_comment is not '':
                        price_error_message += 'Title: %s \nComment: \n%s \nLink: %s \n\n' % (
                        line_dict['title'].capitalize(), price_error_comment, line_dict['url'])
                    if good_deal_comment is not '':
                        good_deal_message += 'Title: %s \nComment: \n%s \nLink: %s \n\n' % (
                        line_dict['title'].capitalize(), good_deal_comment, line_dict['url'])

                continue

            if price_error_message is not '':
                print('Sending email...')
                Utility.send_mail(price_error_message, 'Price Error Deal!')
            else:
                print('No price error returned, waiting for next crawling...')

            if good_deal_message is not '':
                print('Sending email...')
                Utility.send_mail(good_deal_message, 'Good Deal!')
            else:
                print('No good deal returned, waiting for next crawling...')

    @staticmethod
    def send_mail(message, title):
        settings = get_project_settings()
        gmailUser = settings['GMAIL_USER']
        gmailPassword = settings['GMAIL_PASSWORD']
        recipients = settings['RECIPIENTS']

        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = title
        msg.attach(MIMEText(message))

        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipients, msg.as_string())
        mailServer.close()
        print("Mail sent")

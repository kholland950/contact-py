#! /usr/local/bin/python

import sys
import os
import re

from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

# old version
# from email.MIMEText import MIMEText
from email.mime.text import MIMEText

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket
import cgi

SMTPserver = 'smtp.mailgun.org'
sender =     'sender@send.com'
destination = ['dest@dest.com']
USERNAME = "it@mail.com"
PASSWORD = "pass"
# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'

def send_mail(name, email, subject, message):
    template="""\
    Name: {}\n
    Email: {}\n
    Subject: {}\n\n
    Message: {}\n
    """

    subject=name + " contacted you from your portfolio"
    content=template.format(name, email, subject, message)

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']=       subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

    except Exception, exc:
        sys.exit( "mail failed; %s" % str(exc) ) # give a error message


class S(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         }
                 )

            send_mail(
                form['name'].value,
                form['email'].value,
                form['subject'].value,
                form['message'].value
            )
            self.send_response(200)
        except Exception, exc:
            print(Exception, exc)
            self.send_response(500)
        finally:
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

        return

def run(server_class=HTTPServer, handler_class=S, port=9090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()

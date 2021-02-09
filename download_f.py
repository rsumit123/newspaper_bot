import datetime
import requests 
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os
from scrapy.http import HtmlResponse
# from google_drive_downloader import GoogleDriveDownloader as gdd


def get_link(url,date):
    
    response = requests.get(url)
    
    response = HtmlResponse(url = url,body=response.text,encoding='utf-8')
    link = response.xpath('//*[@id="post-810"]/div/p[13]/a/@href').extract()[0]
    response = requests.get(link)
    with open('ff.html','w') as dp:
        dp.write(response.text)
    response = HtmlResponse(url = link,body=response.text,encoding='utf-8')
    f_link = response.xpath('//*[@id="iframe"]/@src').extract()[0]

    
    return f_link
    

def send_mail(send_from, send_to, subject, message, files=[],
              server="smtp.gmail.com", port=587, username='thecolossus018', password='8877041257',
              use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(Path(path).name))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
##############################Downloading PDF###########################################3
url = "https://dailyepaper.in/indian-express-epaper/"
date = datetime.datetime.today().strftime('%d %b %Y')
tdate = datetime.datetime.today().strftime('%d-%m-%Y')
ydate = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d-%m-%Y')

url = get_link(url,date)
# url = "https://pdf.indianexpress.com/pdfupload/icici/ie-delhi-27-01-2021.pdf"

# url = url.replace('03_February_2021',date) 

print("downloading paper..."+"Newspaper_"+tdate+".pdf")
if not os.path.exists("Newspaper_"+tdate+".pdf"):
    try:
        os.remove('Newspaper_'+ydate+".pdf")
        print("Newspaper deleted of date: "+ydate)
    except:
        pass

# # gdd.download_file_from_google_drive(file_id='1kbdeFXc25V9RvZaCogH2WFaACiy8oIwg',
# #                                     dest_path='./'+"Newspaper_"+date+".pdf",
# #                                     unzip=True)
r = requests.get(url) 
with open("Newspaper_"+tdate+".pdf",'wb') as f: 


    f.write(r.content) 
print("sending email..."+" Newspaper_"+tdate+".pdf")

send_mail("thecolossus018@gmail.com",["rsumit123@gmail.com","gogetmayank23@gmail.com"],date+" Indian Express","Greetings from Sumit's Bot , Find today's Indian Express paper in attachment",files = ["Newspaper_"+tdate+".pdf"])

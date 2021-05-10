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
import time
from scrapy.http import HtmlResponse
# from google_drive_downloader import GoogleDriveDownloader as gdd


def get_link(url,date):
    
    response = requests.get(url)
    # with open('ff_ie.html','w') as dp:
    #     dp.write(response.text)
    
    response = HtmlResponse(url = url,body=response.text,encoding='utf-8')

    # re = response.xpath(f'//*[@id="post-810"]/div/p/span/text()').extract()
    # print(re)
    # for i in range(1,15):
    #     try:
    #         re = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/text()').extract()[0]
    #         print(re)
    #         print(i)
    #     except:
    #         pass
        

    # link = response.xpath('//*[@id="post-810"]/div/p[13]/a/@href').extract()[0]
    # text = response.xpath('//*[@id="post-810"]/div/p[13]/text()').extract()[0]
    link = None
    for i in range(16,1,-1):
        try:
            text = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/text()').extract()[0]
            if date.strip().lower() in text.strip().lower():
                link = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/a/@href').extract()[0]
                print(link)
                break

        except Exception as e:
            print(e)

    if link is not None:
        # f_link = link

        response = requests.get(link)
        # with open('ff.html','w') as dp:
        #     dp.write(response.text)
        response = HtmlResponse(url = link,body=response.text,encoding='utf-8')
        f_link = response.xpath('//*[@id="iframe"]/@src').extract()[0]
        return f_link
    else:
        return 0
        # print(link)

    
    # return f_link
######################################################################################
def get_link_hindu(url,date):
    
    response = requests.get(url)
    # with open('ff_hindu.html','w') as dp:
    #     dp.write(response.text)
    
    response = HtmlResponse(url = url,body=response.text,encoding='utf-8')

    # re = response.xpath(f'//*[@id="post-810"]/div/p/span/text()').extract()
    # print(re)
    # for i in range(1,15):
    #     try:
    #         re = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/text()').extract()[0]
    #         print(re)
    #         print(i)
    #     except:
    #         pass
        

    # link = response.xpath('//*[@id="post-810"]/div/p[13]/a/@href').extract()[0]
    # text = response.xpath('//*[@id="post-810"]/div/p[13]/text()').extract()[0]
    link = None
    for i in range(16,1,-1):
        try:
            text = response.xpath(f'//*[@id="post-17698"]/div/p[{i}]/text()').extract()[0]
            if date.strip().lower() in text.strip().lower():
                link = response.xpath(f'//*[@id="post-17698"]/div/p[{i}]/a/@href').extract()[0]
                print(link)
                break

        except Exception as e:
            print(e)

    if link is not None:
        # f_link = link

        response = requests.get(link)
        # with open('ff.html','w') as dp:
        #     dp.write(response.text)
        response = HtmlResponse(url = link,body=response.text,encoding='utf-8')
        f_link = response.xpath('//*[@id="iframe"]/@src').extract()[0]
        return f_link
    else:
        return 0


########################################################################################



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
def download_pdf():
    print("Checking paper availability..")
    url = "https://dailyepaper.in/indian-express-epaper/"
    url_hindu = "https://dailyepaper.in/the-hindu-pdf-epaper-downloa-now/"
    date = datetime.datetime.today().strftime('%d %b %Y')
    tdate = datetime.datetime.today().strftime('%d-%m-%Y')
    ydate = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    # date = "09 May 2021"
    # tdate = "09-05-2021"
    # url = get_link(url,date)
    url = get_link(url,date)
    url_hindu = get_link_hindu(url_hindu,date)
    print("IE == ",url)
    print("TH == ",url_hindu)
    if url !=0 or url_hindu !=0 :
        print("Paper found , downloading..")

        print("downloading paper..."+"IE_Newspaper_"+tdate+".pdf"+" , " +"TH_Newspaper_"+tdate+".pdf")
        if not os.path.exists("IE_Newspaper_"+tdate+".pdf"):
            try:
                os.remove('IE_Newspaper_'+ydate+".pdf")
                os.remove('TH_Newspaper_'+ydate+".pdf")
                print("Newspaper deleted of date: "+ydate)
            except:
                pass

    
        ###########################DOWNLOAD###################################################
        r = requests.get(url) 
        with open("IE_Newspaper_"+tdate+".pdf",'wb') as f: 


            f.write(r.content) 

        r = requests.get(url_hindu) 
        with open("TH_Newspaper_"+tdate+".pdf",'wb') as f: 


            f.write(r.content)
        print("sending email..."+"IE_Newspaper_"+tdate+".pdf"+","+"TH_Newspaper_"+tdate+".pdf")
        
        ################################################################################

        send_mail("thecolossus018@gmail.com",["kumarisuruchi707@gmail.com","rsumit123@gmail.com","rpuja132@gmail.com","gogetmayank23@gmail.com","praachi.nk@gmail.com"],date+" Indian Express and The Hindu","Greetings from Sumit's Bot , Find today's Indian Express and The Hindu paper in attachment",files = ["IE_Newspaper_"+tdate+".pdf","TH_Newspaper_"+tdate+".pdf"])
        # send_mail("thecolossus018@gmail.com",["praachi.nk@gmail.com"],date+" Indian Express and The Hindu","Greetings from Sumit's Bot , Find today's Indian Express and The Hindu paper in attachment",files = ["IE_Newspaper_"+tdate+".pdf","TH_Newspaper_"+tdate+".pdf"])
        # send_mail("thecolossus018@gmail.com",["rsumit123@gmail.com"],date+" Indian Express and The Hindu","Greetings from Sumit's Bot , Find today's Indian Express paper in attachment",files = ["IE_Newspaper_"+tdate+".pdf","TH_Newspaper_"+tdate+".pdf"])

        return 1
    else:
        
        return 0

downloaded = 0
 
while downloaded == 0:
    downloaded = download_pdf()
    if downloaded==0:
        print("Paper not available yet, Trying again after 1000 secs")
        time.sleep(1000)
    else:
        break



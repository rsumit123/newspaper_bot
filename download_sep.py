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
from google_drive_downloader import GoogleDriveDownloader as gdd

headers = {
        'authority': 'iasbano.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'sec-fetch-dest': 'document',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'referer': 'https://www.google.com/',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
        'cookie': 'PHPSESSID=d970c547db1be950aee16c9af6199ef4; _ga=GA1.2.706512715.1612284912; _gid=GA1.2.1930882388.1612284912; __gads=ID=06c316b8dde33f3c-2233b2cfe8c5006a:T=1612284911:RT=1612284911:S=ALNI_Mb7vUOJGddWGzIqz7RtHbocZAdGMw',
    }
def get_link(url,date):
    try:
    
        response = requests.get(url,headers = headers)
    except Exception as e:
        try:
            response = requests.get(url,headers = headers)
        except Exception as e:
            print(e)
            return 0


 
    
    response = HtmlResponse(url = url,body=response.text,encoding='utf-8')

    
    link = None
    for i in range(1,0,-1):
        try:
           
            text = response.xpath(f'/html/body/div[2]/div[2]/div/table/tbody/tr[{i}]/td[1]/text()').extract()[0]
            
            if date.strip().replace(',','').lower().replace('jun','june').replace('jul','july') == text.strip().replace(',','').lower():
               
                link = response.xpath(f'/html/body/div[2]/div[2]/div/table/tbody/tr[{i}]/td[2]/a/@href').extract()[0]
                print(link)
                break
           

        except Exception as e:
            print("from here")
            print(e)

    if link is not None:
        f_link = link

        
        return f_link
    else:
        return 0
        
def get_link_hindu(url,date):
    
    try:
    
        response = requests.get(url,headers = headers)
    except Exception as e:
        try:
            response = requests.get(url,headers = headers)
        except Exception as e:
            print(e)
            return 0
    
    
    response = HtmlResponse(url = url,body=response.text,encoding='utf-8')

    
    link = None
    for i in range(16,0,-1):
        try:
            text = response.xpath(f'/html/body/div[2]/div[2]/div/table/tbody/tr[{i}]/td[1]/text()').extract()[0]
            if date.strip().replace(',','').lower().replace('jun','june').replace('jul','july') == text.strip().replace(',','').lower():
                link = response.xpath(f'/html/body/div[2]/div[2]/div/table/tbody/tr[{i}]/td[2]/a/@href').extract()[0]
                print(link)
                break

        except Exception as e:
            print(e)

    if link is not None:
        f_link = link

        
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
    url = "https://iasbano.com/indian-express-upsc.php#download_the_hindu"
    url_hindu = "https://iasbano.com/the-hindu-pdf-download-1.php#download_the_hindu"
    date = datetime.datetime.today().strftime('%-d %b, %Y')
    tdate = datetime.datetime.today().strftime('%d-%m-%Y')
    ydate = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    # date = "1 June 2021"
    # tdate = "09-05-2021"
    # url = get_link(url,date)

    print("date",date)
    url = get_link(url,date)
    url_hindu = get_link_hindu(url_hindu,date)
    print("IE == ",url)
    print("TH == ",url_hindu)
    if url !=0 and url_hindu !=0 :
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
        f_id_ie = url.split("file/d/")[1].split("/view")[0]
        print("FILE ID ",f_id_ie)
        gdd.download_file_from_google_drive(file_id=f_id_ie,
                                    dest_path="./IE_Newspaper_"+tdate+".pdf"
                                    )

        file_size_ie = os.path.getsize("./IE_Newspaper_"+tdate+".pdf")/1000000
        

        f_id_th = url_hindu.split("file/d/")[1].split("/view")[0]
        print("FILE ID HINDU ",f_id_th)
        gdd.download_file_from_google_drive(file_id=f_id_th,
                                    dest_path="./TH_Newspaper_"+tdate+".pdf"
                                    )

        file_size_th = os.path.getsize("./TH_Newspaper_"+tdate+".pdf")/1000000

        


        

        
        if file_size_ie >=2 and file_size_th>=2:
            print("sending email..."+"IE_Newspaper_"+tdate+".pdf"+","+"TH_Newspaper_"+tdate+".pdf")
        
        ################################################################################
            # if file_size_ie+file_size_th < 25:
            #     # print("Less than 25")
            #     # pass
        

            #     send_mail("thecolossus018@gmail.com",["kumarisuruchi707@gmail.com","rpuja132@gmail.com","rsumit123@gmail.com","gogetmayank23@gmail.com","praachi.nk@gmail.com"],date+" Indian Express and The Hindu","Greetings from Sumit's Bot , Find today's Indian Express and The Hindu paper in attachment",files = ["IE_Newspaper_"+tdate+".pdf","TH_Newspaper_"+tdate+".pdf"])
            # else:
            #     # pass

            #     send_mail("thecolossus018@gmail.com",["kumarisuruchi707@gmail.com","rpuja132@gmail.com","rsumit123@gmail.com","gogetmayank23@gmail.com","praachi.nk@gmail.com"],date+" Indian Express and The Hindu","Greetings from Sumit's Bot , Find today's Indian Express and The Hindu paper in attachment. PDF of The Hindu exceeded gmail's size limit for attachments. Please view The Hindu paper from the following link => "+url_hindu,files = ["IE_Newspaper_"+tdate+".pdf"])

        
        
        else:
            print("File size error... ")
            return 0

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



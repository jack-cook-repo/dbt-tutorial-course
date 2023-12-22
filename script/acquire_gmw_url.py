

from bs4 import BeautifulSoup
from html import unescape
import argparse
import requests
import urllib3
import random
import sys
import re
import pandas as pd
import numpy as np
from io import StringIO # python3; python2: BytesIO 
import boto3
from google.cloud import bigquery

USER_AGENT_LIST = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]
HEADER = {
    'User-Agent': random.choice(USER_AGENT_LIST)
    }
BUCKET = 'test-instance1' # already created on S3

def get_datetime(soup, datetime_lt):
    
    for datetime in soup.find_all('time', attrs={'class':"entry-date published"}):
        datetime_lt.append(datetime.get("datetime"))
    
    return datetime_lt

def get_perview_url(soup, perview_url):
    #for link in soup.findAll('p'):
    try:
        for link in soup.find_all('div', attrs={'class':"entry-content"}):
            img_lt = []
            img_lt_html = link.parent.find_all(decoding='async')
            if len(img_lt_html) > 0:
                for img in img_lt_html:
                    # print(img)
                    if len(img.get("data-src")) > 0:
                        # print(img.get("data-src"))
                        img_lt.append(img.get("data-src"))
                if len(img_lt)>0: # some are wired
                    perview_url.append(img_lt)
            else:
                perview_url.append(img_lt)      
    except:
        perview_url.append([])

    return perview_url

def get_download_url(soup, download_url_lt):
    #for link in soup.findAll('p'):
    try:
        for link in soup.find_all('div', attrs={'class':"entry-content"}):
            download_lt = []
            download_lt_html = link.parent.find_all('a', attrs={'href': re.compile(r'https?://(?:katfile|filemarkets)')})
            if len(download_lt_html) > 0:
                for download in download_lt_html:
                    if len(download.get("href")) > 0:
                        download_lt.append(download.get("href"))
                if len(download_lt)>0: # some are wired
                    download_url_lt.append(download_lt)
            else:
                download_url_lt.append(download_lt)      
    except:
        download_url_lt.append([])

    return download_url_lt

"""
def get_download_url(soup, download_url_lt, name_lt):
    download_lt_all = []
    for link in soup.findAll('a', attrs={'href': re.compile(r'https?://katfile')}):
        href_lt = link.get('href').split('/')
        if href_lt[2] == 'katfile.com':
            suffix_lt = href_lt[-1].split('.')
            file_name = suffix_lt[0]
            download_lt_all.append(file_name)
    download_lt_all = set(download_lt_all)
    for download in download_lt_all:
        parts = []
        for link in soup.findAll('a', attrs={'href': re.compile(r'https?://katfile')}):
            href_lt = link.get('href').split('/')
            suffix_lt = href_lt[-1].split('.')
            katfile_file_name = suffix_lt[0]
            if katfile_file_name == download:
                parts.append(link.get('href'))
        download_url_lt.append(parts)
    while len(download_url_lt) != len(name_lt):
        download_url_lt.append([])
    return download_url_lt
"""
def get_download_info(soup, page_suffix, name_lt, size_lt, page_lt, video_lt, image_lt):
    current_name = []
    for link in soup.findAll('h2', attrs={'class': re.compile("entry-title")}):
            
            full_name = link.get_text()
            full_name_lt = full_name.rpartition('[')
            # check the len 
            if full_name_lt[0] == "":
                modified_text = re.sub(r'(\d+P|MP4|\d+V)', r'[\1', full_name)
                full_name_lt = modified_text.rpartition('[')             
            name = full_name_lt[0]
            detail = full_name_lt[2]
            detail_lt = detail.split('/')
            name_lt.append(name)
            current_name.append(name)
            size_lt.append(detail_lt[-1][:-1])
            page_lt.append(int(page_suffix))
            if len(detail_lt) == 3:
                if detail_lt[0][-1] == "P":
                    image_lt.append(detail_lt[0])
                else:
                    image_lt.append('')
                if detail_lt[1][-1] == "V":
                    video_lt.append(detail_lt[1])
                else:
                    video_lt.append('')
            elif len(detail_lt) == 2:
                if detail_lt[0][-1] == "P":
                    image_lt.append(detail_lt[0])
                    video_lt.append("")
                elif detail_lt[0][-3:] == "MP4":
                    video_lt.append("1V")
                    image_lt.append("")
                elif detail_lt[0][-1] == "V":
                    video_lt.append(detail_lt[0])
                    image_lt.append("")
                else:
                    video_lt.append("")
                    image_lt.append("")
            elif len(detail_lt)== 4:
                if detail_lt[0][-1] == "P":
                    image_lt.append(detail_lt[0])
                else:
                    image_lt.append('')
                if detail_lt[1][-1] == "V":
                    video_lt.append(detail_lt[1])
                else:
                    video_lt.append('')
            else:
                print("here")
                image_lt.append("")
                video_lt.append("")

    return name_lt, size_lt, page_lt, video_lt, image_lt, current_name

def main(args):
    current_page = 1
    datetime_lt = []
    download_url_lt = []
    perview_url_lt = []
    name_lt = []
    size_lt = []
    page_lt = []
    video_lt = []
    image_lt = []
    current_name = []
    s = requests.Session()
    http = urllib3.PoolManager()
    url = args.url
    csv_buffer = StringIO()
    page_suffix = args.page_suffix
    while current_page != int(page_suffix)+1:
        if s.get(url+str(current_page), allow_redirects=True, headers = HEADER, stream=True).status_code == 200:
    # for page_suffix in range(815, int(page_suffix)+1):

            response = http.request('GET', url+str(current_page))
            soup = BeautifulSoup(response.data, 'html.parser')
            print("You are visting: " + url + str(current_page))
            name_lt, size_lt, page_lt, video_lt, image_lt, current_name = get_download_info(soup, current_page, name_lt, size_lt, page_lt, video_lt, image_lt)
            download_url_lt = get_download_url(soup, download_url_lt)
            perview_url_lt = get_perview_url(soup, perview_url_lt)
            datetime_lt = get_datetime(soup, datetime_lt)
            current_page += 1
            if(not(len(datetime_lt) == len(download_url_lt) == len(perview_url_lt) == len(name_lt) == len(size_lt) == len(page_lt) == len(video_lt) == len(image_lt))):
                break
        else:
            break
    print(len(datetime_lt))
    print(len(download_url_lt))
    print(len(perview_url_lt))
    print(len(name_lt))
    print(len(size_lt))

    print(len(page_lt))
    print(len(video_lt))
    print(len(image_lt))
    if(len(datetime_lt) == len(download_url_lt) == len(perview_url_lt) == len(name_lt) == len(size_lt) == len(page_lt) == len(video_lt) == len(image_lt)):
        df = pd.DataFrame({'name':name_lt, 
                        "perview_url": perview_url_lt, 
                        "download_url": download_url_lt, 
                        "page": page_lt,
                        "video": video_lt,
                        "image": image_lt,
                        "size": size_lt,
                        "datetime": datetime_lt
                        })
        df.to_csv(csv_buffer, index= False)
        s3 = boto3.client('s3')
        s3.put_object(Bucket=BUCKET, Key="dbt-bigquery/landing/gmw.csv", Body=csv_buffer.getvalue())
    else:
        print("Error")
if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-u", "--url", help="The url you want to clone", default="https://gm45.xyz/page")
    argParser.add_argument("-p", "--page_suffix", help="The page you want to clone", default="1")
    args = argParser.parse_args()
    main(args)
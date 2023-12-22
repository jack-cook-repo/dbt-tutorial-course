import aiohttp
import asyncio
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

BUCKET = 'test-instance1'

def upload_to_s3(df, csv_buffer):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=BUCKET, Key="dbt-bigquery/landing/gmw.csv", Body=csv_buffer.getvalue())

async def get_datetime(soup, datetime_lt):
    
    for datetime in soup.find_all('time', attrs={'class':"entry-date published"}):
        datetime_lt.append(datetime.get("datetime"))
    
    return datetime_lt


async def get_perview_url(soup, perview_url):
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

async def get_download_url(soup, download_url_lt):
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

async def get_download_info(soup, page_suffix, name_lt, size_lt, page_lt, video_lt, image_lt):
    current_name = []
    for link in soup.findAll('h2', attrs={'class': re.compile("entry-title")}):
            print(link.get_text())
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
            page_lt.append(page_suffix)
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

    return name_lt, size_lt, page_lt, video_lt, image_lt


async def fetch_html(session, url, header):
    async with session.get(url, allow_redirects=True, headers = header) as response:
        datetime_lt = []
        download_url_lt = []
        perview_url_lt = []
        name_lt = []
        size_lt = []
        page_lt = []
        video_lt = []
        image_lt = []
        html_content = await response.text()
        soup = BeautifulSoup(html_content, 'html.parser')
        print(soup)
        name_lt, size_lt, page_lt, video_lt, image_lt = await get_download_info(soup, url, name_lt, size_lt, page_lt, video_lt, image_lt)
        download_url_lt = await get_download_url(soup, download_url_lt)
        perview_url_lt = await get_perview_url(soup, perview_url_lt)
        datetime_lt = await get_datetime(soup, datetime_lt)
        print("You are visiting:", url)
        return name_lt, size_lt, page_lt, video_lt, image_lt, download_url_lt, perview_url_lt, datetime_lt

async def process_batch(start_page, end_page):
    async with aiohttp.ClientSession() as session:
        header = {
        'User-Agent': random.choice(USER_AGENT_LIST)
        }
        tasks = []
        for page_number in range(start_page, end_page + 1):
            url = f'https://gm45.xyz/page/{page_number}/'
            tasks.append(fetch_html(session, url, header))
        
        # Wait for all tasks in the batch to complete
        batch_html = await asyncio.gather(*tasks)
        merged_names, merged_size, merged_page, merged_video, merged_image, merged_download_url, merged_perview_url, merged_datetime = process_html(batch_html)
        print(len(merged_names))
        if(len(merged_names) == len(merged_size) == len(merged_page) == len(merged_video) == len(merged_image) == len(merged_download_url) == len(merged_perview_url) == len(merged_datetime)):
            df = pd.DataFrame({'name':merged_names, 
                            "perview_url": merged_perview_url, 
                            "download_url": merged_download_url, 
                            "page": merged_page,
                            "video": merged_video,
                            "image": merged_image,
                            "size": merged_size,
                            "datetime": merged_datetime
                            })
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index= False)
            upload_to_s3(df, csv_buffer)
        else:
            print("Error")


def process_html(batch_results):
    # Implement your logic to process the gathered HTML content
    merged_names = []
    merged_size = []
    merged_page = []
    merged_video = []
    merged_image = []
    merged_download_url = []
    merged_perview_url = []
    merged_datetime = []
    for result in batch_results:
        # Unpack the results for each page
        name_lt, size_lt, page_lt, video_lt, image_lt, download_url_lt, perview_url_lt, datetime_lt = result
        # Process each page's information
        merged_names.extend(name_lt)
        merged_size.extend(size_lt)
        merged_page.extend(page_lt)
        merged_video.extend(video_lt)
        merged_image.extend(image_lt)
        merged_download_url.extend(download_url_lt)
        merged_perview_url.extend(perview_url_lt)
        merged_datetime.extend(datetime_lt)
    return merged_names, merged_size, merged_page, merged_video, merged_image, merged_download_url, merged_perview_url, merged_datetime

async def main(args):
    total_pages = int(args.page_suffix)
    batch_size = 100

    # Divide pages into batches
    for start_page in range(1, total_pages + 1, batch_size):
        end_page = min(start_page + batch_size - 1, total_pages)
        print(start_page, end_page)
        await process_batch(start_page, end_page)

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-u", "--url", help="The url you want to clone", default="https://gm45.xyz/page")
    argParser.add_argument("-p", "--page_suffix", help="The page you want to clone", default="1")
    args = argParser.parse_args()
    asyncio.run(main(args))
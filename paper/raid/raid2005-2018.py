# https://link.springer.com/conference/raid

import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Springer 图书基本信息
base_url = "https://link.springer.com"
book_id = "978-3-319-66332-6"

# 所有 TOC 分页链接（注意修改页数范围）
toc_urls = [
    f"https://link.springer.com/book/10.1007/{book_id}?page={i}#toc"
    for i in range(1, 3)  # 有几页就写几页，比如 1~3 页
]

# 下载目录
download_folder = r"C:\Users\lyz\Desktop\crawler\RAID\RAID_2017"
os.makedirs(download_folder, exist_ok=True)

# 清理非法文件名字符
def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '_', title)

# 浏览器伪装
headers = {
    "authority": "link.springer.com",
    "method": "GET",
    "path": "/chapter/10.1007/978-3-030-00470-5_1",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "idp_marker=95ad0a9b-03bd-4fea-847b-a5dd83dcf91c; user.uuid.v2=\"2ec1672b-aa25-4857-a3b5-bfa94aebdb4f\"; optimizelyEndUserId=oeu1741768615848r0.07761518582342197; ajs_anonymous_id=4adb9d00-1ad6-4887-871a-9a55f85d52b5; _fbp=fb.1.1741769913655.561293384506287514; _ga=GA1.1.621268513.1741769916; _hjSessionUser_5176049=eyJpZCI6IjA1ZDdjNGRmLTM4ZTItNTMyNC1iMDQ0LTEyODE4MWFhOGY5ZiIsImNyZWF0ZWQiOjE3NDE3Njk5MTY4OTEsImV4aXN0aW5nIjpmYWxzZX0=; permutive-id=e1895676-4222-4d24-b7c5-e9698a59f0d5; sncc=P%3D17%3AV%3D54.0.0%26C%3DC01%2CC02%2CC03%2CC04%26D%3Dtrue; Hm_lvt_e1214cdac378990dc262ce2bc824c85a=1743500960; Hm_lvt_aef3043f025ccf2305af8a194652d70b=1741769914,1743500966,1743515178; trackid=\"rjzrez58krpsi8divwadppeja\"; idp_session=sVERSION_1419d6c8a-cc0a-4cb0-8a9c-e0be5bf389fd; idp_session_http=hVERSION_1ee782912-ffce-488d-b53a-d09ccea28591; sim-inst-token=\"1::1743613959497:3c305485\"; cto_bundle=_sx0Y191Nm1ZR0hPaUVNTEclMkZnOWRpOFE0eHVDYzllRDJ0QWZ6aWJjdmpTVFAxMkZzSmVFTHRhZ2xQSmh4c05ReGk4R3FMb1clMkJjSHg2MUtmN3RGcnpWM204bUVlcHV2V0hVT1BlZHlFSjIyUmZZQnlpaXg5NlE0NUlqS3FvQU1pbjklMkY3QTFHYlExYjM2RSUyRiUyRkJQRTI5VVc4VjZZVEFMbVclMkJlJTJCc0dia0ZkOWlUdDlFYyUzRA; __gads=ID=7ff83539a9182100:T=1741769917:RT=1743584658:S=ALNI_MaO0jvxmuKfhvEW2qr7qQcYa9IllQ; __gpi=UID=0000105e64e3077b:T=1741769917:RT=1743584658:S=ALNI_MbZCMAdZ2MwywlBvuECUeuUP1HJ-w; __eoi=ID=dd9a8c3a429b1f3d:T=1741769917:RT=1743584658:S=AA-AfjZ6-fM_EWZISFfcuNhUDMt5; _uetsid=955bd2600ede11f0b5397b9a20b749a4; _uetvid=2d7c6e10ff2011ef835fc14883ef49b2; permutive-session=%7B%22session_id%22%3A%2230ab8784-6266-48f7-b352-6634884b2a12%22%2C%22last_updated%22%3A%222025-04-02T09%3A06%3A00.421Z%22%7D; amp_72dea4=-qj4vLgk-4TrJLdQ7mmqiI...1inqr7a0n.1inqs04k5.j.6.p; _ga_B3E4QL2TPR=GS1.1.1743583946.4.1.1743584899.60.0.0; _ga_5V24HQ1XD5=GS1.1.1743583946.4.1.1743584899.0.0.0",
    "if-none-match": "\"ea03121715cfc76ebf41e39b0fe464ce\"",
    "priority": "u=0, i",
    "referer": "https://link.springer.com/book/10.1007/978-3-030-00470-5",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

idx = 1  # 全局编号
for toc_url in toc_urls:
    print(f"\n🌐 Processing TOC page: {toc_url}\n")

    try:
        response = requests.get(toc_url, headers=headers)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch page: {toc_url}")
            continue
    except Exception as e:
        print(f"❌ Exception while fetching TOC page: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # 提取章节标题块和 PDF 块
    card_main_list = soup.find_all("div", class_="app-card-open__main")
    card_side_list = soup.find_all("div", class_="app-card-open__side")

    for main_div, side_div in zip(card_main_list, card_side_list):
        a_tag = main_div.find("a")
        if not a_tag or not a_tag.get("href"):
            continue

        title = a_tag.get_text(strip=True)
        chapter_url = urljoin(base_url, a_tag["href"])

        # PDF 下载链接
        pdf_a_tag = side_div.find("a", class_="c-pdf-chapter-download__link")
        if not pdf_a_tag or not pdf_a_tag.get("href"):
            print(f"{idx}. Title: {title}")
            print("   ⚠️ PDF link not found.")
            idx += 1
            continue

        pdf_link = urljoin(base_url, pdf_a_tag["href"])

        # 输出信息
        print(f"{idx}. Title: {title}")
        print(f"   Chapter URL: {chapter_url}")
        print(f"   PDF Link: {pdf_link}")

        try:
            pdf_response = requests.get(pdf_link, headers=headers)
            if pdf_response.status_code == 200:
                sanitized_title = sanitize_filename(title)
                pdf_path = os.path.join(download_folder, f"{sanitized_title}.pdf")
                with open(pdf_path, "wb") as f:
                    f.write(pdf_response.content)
                print(f"   ✅ PDF saved: {pdf_path}")
            else:
                print(f"   ❌ Failed to download PDF: {pdf_link}")
        except Exception as e:
            print(f"   ❌ Exception while downloading PDF: {e}")

        idx += 1

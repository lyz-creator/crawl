import os
import requests
import re
from bs4 import BeautifulSoup

# 目标网页
url = "https://raid2024.github.io/accepted_open.html"
base_url = "https://raid2024.github.io/"

# 下载目录
download_folder = r"C:\Users\lyz\Desktop\crawler\RAID\RAID_2024"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '_', title)

# 请求网页内容
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有 class="responsive" 的 div 中的 p 标签
responsive_div = soup.find("div", class_="responsive")
papers = responsive_div.find_all("p")

for idx, p_tag in enumerate(papers, start=1):
    b_tag = p_tag.find("b")
    if not b_tag:
        continue

    # 提取标题
    raw_text = b_tag.get_text()
    title = raw_text.strip().replace("[PDF]", "").strip('“”" ')
    print(f"{idx}. Title: {title}")

    # 提取 PDF 链接
    a_tag = b_tag.find("a")
    if a_tag and a_tag.get("href"):
        pdf_link = base_url + a_tag["href"]
        print(f"   PDF Link: {pdf_link}")

        # 下载 PDF
        try:
            pdf_response = requests.get(pdf_link)
            if pdf_response.status_code == 200:
                sanitized_title = sanitize_filename(title)
                pdf_path = os.path.join(download_folder, f"{sanitized_title}.pdf")
                with open(pdf_path, "wb") as f:
                    f.write(pdf_response.content)
                print(f"   ✅ PDF saved: {pdf_path}")
            else:
                print(f"   ❌ Failed to download PDF: {pdf_link}")
        except Exception as e:
            print(f"   ❌ Exception during PDF download: {e}")
    else:
        print("   ⚠️ No PDF link found.")

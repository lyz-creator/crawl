import os
import requests
from bs4 import BeautifulSoup
import re
import time
import random

# 清理文件名，使其合法
def sanitize_filename(title):
    return re.sub(r'[^a-zA-Z0-9-_\s]', '_', title)

# 目标网页 URL（2010年）
url = 'https://www.usenix.org/legacy/events/sec10/tech/'

# 下载目录
download_folder = r"C:\Users\lyz\Desktop\crawler\Security\Security_2010"

# 如果下载目录不存在，创建该目录
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# 自定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

# 发送 HTTP 请求获取网页内容
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到所有 class 为 'fullpaper1' 的 p 标签
    paper_tags = soup.find_all('p', class_='fullpaper1')
    
    for paper_tag in paper_tags:
        title_tag = paper_tag.find('b')
        if title_tag:
            title = title_tag.get_text(strip=True)
            sanitized_title = sanitize_filename(title)
            
            # 找到下一个 class 为 'abs' 的 p 标签
            next_p = paper_tag.find_next_sibling('p', class_='abs')
            if next_p:
                # 在 'abs' 标签内找到包含PDF链接的 <a> 标签
                pdf_link_tag = next_p.find('a', string='Full paper')
                if pdf_link_tag and pdf_link_tag.get('href'):
                    pdf_link = url + pdf_link_tag.get('href')
                    
                    print(f"标题: {sanitized_title}")
                    print(f"PDF 链接: {pdf_link}")
                    
                    # 下载 PDF
                    try:
                        pdf_response = requests.get(pdf_link, headers=headers, timeout=30)
                        if pdf_response.status_code == 200:
                            if len(sanitized_title) > 200:
                                sanitized_title = sanitized_title[:200]
                            
                            pdf_filename = f"{sanitized_title}.pdf"
                            pdf_path = os.path.join(download_folder, pdf_filename)
                            
                            with open(pdf_path, 'wb') as f:
                                f.write(pdf_response.content)
                            print(f"已成功下载 PDF: {pdf_filename}")
                        else:
                            print(f"下载 PDF 失败，状态码: {pdf_response.status_code}")
                    except Exception as e:
                        print(f"下载 PDF 时出错: {str(e)}")
                    
                    time.sleep(random.uniform(0.5, 2))  # 随机延迟，避免请求过快
                else:
                    print("未找到 PDF 下载链接")
            else:
                print("未找到对应的 PDF 详情标签")
else:
    print(f'请求网页失败，状态码：{response.status_code}')

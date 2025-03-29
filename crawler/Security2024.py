import os
import requests
from bs4 import BeautifulSoup
import re
import time
import random

# 清理文件名，使其合法
def sanitize_filename(title):
    """清理文件名，使其合法"""
    return re.sub(r'[<>:"/\\|?*]', '_', title)

# 目标网页 URL
url = 'https://www.usenix.org/conference/usenixsecurity24/summer-accepted-papers'

# 下载目录
download_folder = r"C:\Users\lyz\Desktop\crawler\Security_2024"

# 如果下载目录不存在，创建该目录
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# 发送 HTTP 请求获取网页内容
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析 HTML 内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到所有包含多个 <span class="usenix-schedule-media pdf"> 的 <div> 标签
    divs = soup.find_all('div', class_='required-fields group-available-media field-group-html-element')
    
    for div in divs:
        # 找到第一个 <span class="usenix-schedule-media pdf"> 标签
        span = div.find('span', class_='usenix-schedule-media pdf')
        if span and span.a and span.a.get('href'):
            # 提取链接
            link = span.a.get('href')
            # 确保链接是完整的 URL
            if not link.startswith('http'):
                link = 'https://www.usenix.org' + link
            
            # 发送请求访问链接页面
            link_response = requests.get(link)
            if link_response.status_code == 200:
                # 解析链接页面内容
                link_soup = BeautifulSoup(link_response.text, 'html.parser')
                # 查找论文标题
                title_tag = link_soup.find('h1', id='page-title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    # 使用 sanitize_filename 来清理标题
                    sanitized_title = sanitize_filename(title)
                    
                    # 查找 PDF 链接
                    pdf_div = link_soup.find('div', class_='field-name-field-presentation-pdf')
                    if pdf_div:
                        pdf_link_tag = pdf_div.find('a', href=True)
                        if pdf_link_tag:
                            pdf_link = pdf_link_tag['href']
                            # 确保 PDF 链接是完整的
                            if not pdf_link.startswith('http'):
                                pdf_link = 'https://www.usenix.org' + pdf_link
                            
                            # 下载 PDF 文件
                            pdf_response = requests.get(pdf_link)
                            if pdf_response.status_code == 200:
                                # 使用论文标题作为文件名，确保路径安全
                                pdf_filename = f"{sanitized_title}.pdf"
                                pdf_path = os.path.join(download_folder, pdf_filename)
                                
                                # 保存 PDF 文件
                                with open(pdf_path, 'wb') as f:
                                    f.write(pdf_response.content)
                                print(f"已保存 PDF：{pdf_path}")
                            else:
                                print(f"无法下载 PDF: {pdf_link}")
                        else:
                            print('未找到 PDF 链接。')
                    else:
                        print('未找到 PDF 链接区域。')
                else:
                    print('未找到论文标题。')
            else:
                print(f'无法访问链接，状态码：{link_response.status_code}')
        else:
            print('未找到有效的 <span class="usenix-schedule-media pdf"> 标签或链接。')
        
        # 随机延迟 1 到 3 秒
        time.sleep(random.randint(1, 3))
else:
    print(f'请求主网页失败，状态码：{response.status_code}')

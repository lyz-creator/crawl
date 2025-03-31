import os
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import threading

# 清理文件名，使其合法
def sanitize_filename(title):
    return re.sub(r'[^a-zA-Z0-9-_\s]', '_', title)

# 下载目录基础路径
base_download_folder = r"C:\Users\lyz\Desktop\crawler\Security"

# 自定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

# 目标网页 URL 列表
urls = [
    'https://www.usenix.org/legacy/events/sec04/tech/',
    'https://www.usenix.org/legacy/events/sec05/tech/',
    'https://www.usenix.org/legacy/events/sec06/tech/',
    'https://www.usenix.org/legacy/events/sec07/tech/'
]

# 爬取单个页面的函数
def crawl_page(url):
    # 提取年份
    year = url.split('/')[-3]  # 从 URL 中提取年份
    
    # 创建该年份的下载目录
    year_folder = os.path.join(base_download_folder, f"Security_{year}")
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)

    # 发送 HTTP 请求获取网页内容
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有的 a 标签，且 a 标签的 href 属性以 .html 结尾
        paper_tags = soup.find_all('a', href=re.compile(r'.*\.html$'))
        
        for paper_tag in paper_tags:
            title_tag = paper_tag.find('b')
            if title_tag:
                title = title_tag.get_text(strip=True)
                sanitized_title = sanitize_filename(title)
                
                # 构造论文的详细页面 URL
                paper_url = url + paper_tag.get('href')
                
                # 请求论文详细页面
                paper_response = requests.get(paper_url, headers=headers)
                if paper_response.status_code == 200:
                    paper_soup = BeautifulSoup(paper_response.text, 'html.parser')
                    
                    # 在详细页面中找到PDF链接
                    pdf_tag = paper_soup.find('a', href=re.compile(r'.*\.pdf$'))
                    if pdf_tag and pdf_tag.get('href'):
                        pdf_link = url + pdf_tag.get('href')
                        
                        print(f"年份: {year} | 标题: {sanitized_title}")
                        print(f"PDF 链接: {pdf_link}")
                        
                        # 下载 PDF
                        try:
                            pdf_response = requests.get(pdf_link, headers=headers, timeout=30)
                            if pdf_response.status_code == 200:
                                if len(sanitized_title) > 200:
                                    sanitized_title = sanitized_title[:200]
                                
                                pdf_filename = f"{sanitized_title}.pdf"
                                pdf_path = os.path.join(year_folder, pdf_filename)
                                
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
                    print(f"无法访问论文详细页面，状态码: {paper_response.status_code}")
            else:
                print("未找到论文标题")
    else:
        print(f'请求网页失败，状态码：{response.status_code}')

# 创建线程列表
threads = []

# 为每个 URL 创建一个线程
for url in urls:
    thread = threading.Thread(target=crawl_page, args=(url,))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

print("所有页面爬取完成。")

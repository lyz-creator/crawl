import os
import requests
from bs4 import BeautifulSoup
import re
import time
import random

# 清理文件名，使其合法
def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '_', title)

# 基础URL模板
base_url_template = 'https://www.usenix.org/conference/usenixsecurity{}/technical-sessions'

# 下载目录基础路径
base_download_folder = r"C:\Users\lyz\Desktop\crawler\Security"

# 自定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

# 枚举2012年到2016年的URL
years = range(12, 17)
urls = [base_url_template.format(year) for year in years]

# 遍历每个URL
for year, url in zip(years, urls):
    # 当年的下载目录
    download_folder = os.path.join(base_download_folder, f"Security_20{year}")
    
    # 如果下载目录不存在，创建该目录
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    print(f"开始爬取 {year} 年的论文")
    print(f"访问的URL: {url}")
    
    # 发送 HTTP 请求获取网页内容
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有包含论文信息的 div
        paper_divs = soup.find_all('div', class_='node node-paper view-mode-teaser node-teaser clearfix')
        
        if not paper_divs:
            print(f"未找到论文信息的div，可能是页面结构发生变化或URL不正确。")
            continue
        
        for div in paper_divs:
            h2 = div.find('h2')
            if h2:
                a_tag = h2.find('a')
                if a_tag and a_tag.get('href'):
                    title = a_tag.get_text(strip=True)
                    paper_page_link = 'https://www.usenix.org' + a_tag.get('href')
                    
                    # 清理文件名
                    sanitized_title = sanitize_filename(title)
                    
                    print(f"标题: {sanitized_title}")
                    print(f"论文详情页URL: {paper_page_link}")
                    
                    time.sleep(random.randint(0, 1))  # 随机延迟
                    
                    # 访问论文详情页
                    paper_response = requests.get(paper_page_link, headers=headers)
                    if paper_response.status_code == 200:
                        paper_soup = BeautifulSoup(paper_response.text, 'html.parser')
                        
                        # 找到 PDF 下载链接
                        pdf_span = paper_soup.find('span', class_='file')
                        pdf_link_tag = pdf_span.find('a') if pdf_span else None
                        
                        if pdf_link_tag and pdf_link_tag.get('href'):
                            pdf_link = pdf_link_tag.get('href')
                            
                            if not pdf_link.startswith('http'):
                                pdf_link = 'https://www.usenix.org' + pdf_link
                            
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
                        else:
                            print("未找到 PDF 下载链接")
                    else:
                        print(f"访问论文页面失败，状态码: {paper_response.status_code}")
                    
                    time.sleep(random.randint(0, 1))  # 避免请求过快
    else:
        print(f'请求网页失败，状态码：{response.status_code}')
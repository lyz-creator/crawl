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
urls = {
    2017: 'https://www.usenix.org/conference/usenixsecurity17/technical-sessions',
    2018: 'https://www.usenix.org/conference/usenixsecurity18/technical-sessions'
}

# 下载目录
base_download_folder = r"C:\Users\lyz\Desktop\crawler\Security"

# 自定义请求头，模拟浏览器行为
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

# 遍历每个年份
for year, url in urls.items():
    print(f"开始处理 {year} 年的数据...")
    
    # 创建对应年份的下载目录
    download_folder = os.path.join(base_download_folder, f"Security_{year}")
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # 发送 HTTP 请求获取网页内容
    response = requests.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有包含 <div class="field-item odd"> 和 <div class="field-item even"> 标签
        divs = soup.find_all('div', class_=lambda c: c in ['field-item odd', 'field-item even'])
        
        for div in divs:
            # 找到 h2 标签中的 a 标签
            h2 = div.find('h2')
            if h2:
                a_tag = h2.find('a')
                if a_tag and a_tag.get('href'):
                    title = a_tag.get_text(strip=True)
                    paper_page_link = 'https://www.usenix.org' + a_tag.get('href')
                    
                    # 清理文件名
                    sanitized_title = sanitize_filename(title)
                    
                    # 输出标题和链接
                    print(f"{year} 年 - 标题: {sanitized_title}")
                    print(f"{year} 年 - URL: {paper_page_link}")
                    
                    # 随机延迟 1 到 3 秒，避免请求过快
                    time.sleep(random.randint(1, 3))
                    
                    # 访问论文页面
                    paper_response = requests.get(paper_page_link, headers=headers)
                    if paper_response.status_code == 200:
                        paper_soup = BeautifulSoup(paper_response.text, 'html.parser')
                        
                        # 寻找 PDF 下载链接
                        # 根据提供的信息查找 PDF 链接
                        pdf_div = paper_soup.find('div', class_='field-name-field-presentation-pdf')
                        
                        if not pdf_div:
                            # 通用查找方法，查找所有包含 PDF 链接的 a 标签
                            pdf_links = paper_soup.find_all('a', href=lambda href: href and '.pdf' in href)
                            if pdf_links:
                                pdf_link_tag = pdf_links[0]  # 使用第一个找到的 PDF 链接
                            else:
                                pdf_link_tag = None
                        else:
                            # 如果找到了特定的 div，从中提取 a 标签
                            pdf_link_tag = pdf_div.find('a')
                        
                        if pdf_link_tag and pdf_link_tag.get('href'):
                            pdf_link = pdf_link_tag.get('href')
                            
                            # 判断是否为完整 URL
                            if not pdf_link.startswith('http'):
                                pdf_link = 'https://www.usenix.org' + pdf_link
                            
                            print(f"{year} 年 - PDF 链接: {pdf_link}")
                            
                            # 下载 PDF 文件
                            try:
                                pdf_response = requests.get(pdf_link, headers=headers, timeout=30)
                                if pdf_response.status_code == 200:
                                    # 确保文件名不超过 Windows 最大长度限制
                                    if len(sanitized_title) > 200:
                                        sanitized_title = sanitized_title[:200]
                                    
                                    pdf_filename = f"{sanitized_title}.pdf"
                                    pdf_path = os.path.join(download_folder, pdf_filename)
                                    
                                    with open(pdf_path, 'wb') as f:
                                        f.write(pdf_response.content)
                                    print(f"{year} 年 - 已成功下载 PDF: {pdf_filename}")
                                else:
                                    print(f"{year} 年 - 下载 PDF 失败，状态码: {pdf_response.status_code}")
                            except Exception as e:
                                print(f"{year} 年 - 下载 PDF 时出错: {str(e)}")
                        else:
                            print(f"{year} 年 - 未找到 PDF 下载链接")
                    else:
                        print(f"{year} 年 - 访问论文页面失败，状态码: {paper_response.status_code}")
                    
                    # 随机延迟 2 到 5 秒，避免请求过快被封
                    time.sleep(random.randint(2, 5))
    else:
        print(f"{year} 年 - 请求网页失败，状态码：{response.status_code}")
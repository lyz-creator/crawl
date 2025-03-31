import os
import requests
from bs4 import BeautifulSoup
import re

# 清理文件名，使其合法，去除换行及其他非法字符
def sanitize_filename(title):
    # 去除换行符等非打印字符
    title = title.replace('\n', ' ')
    # 使用正则表达式替换其他非法字符
    return re.sub(r'[^a-zA-Z0-9-_\s]', '_', title)

# 目标网页 URL（2003年）
url = 'https://www.usenix.org/legacy/events/sec03/tech.html'

# 下载目录
download_folder = r"C:\Users\lyz\Desktop\crawler\Security\Security_2003"

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
    
    # 找到所有 b 标签下的 a 标签
    paper_tags = soup.find_all('b')
    
    for paper_tag in paper_tags:
        a_tag = paper_tag.find('a')
        if a_tag and 'href' in a_tag.attrs:
            href = a_tag['href']
            # 检查 href 是否以 'tech/' 开头并且以 '.html' 结尾
            if href.startswith('tech/') and href.endswith('.html'):
                title = a_tag.get_text(strip=True)
                sanitized_title = sanitize_filename(title)
                
                # 获取a标签的href，进入详细页面
                tech_page_url = 'https://www.usenix.org/legacy/events/sec03/' + href
                
                # 访问每个论文的详细页面
                tech_page_response = requests.get(tech_page_url, headers=headers)
                if tech_page_response.status_code == 200:
                    tech_page_soup = BeautifulSoup(tech_page_response.text, 'html.parser')
                    
                    # 查找以 .pdf 结尾的链接
                    pdf_link_tag = tech_page_soup.find('a', href=re.compile(r'.*\.pdf$'))
                    if pdf_link_tag and pdf_link_tag.get('href'):
                        pdf_link = pdf_link_tag['href']
                        
                        # 如果 pdf_link 是相对路径，补充完整的 URL
                        if not pdf_link.startswith('http'):
                            pdf_link = 'https://www.usenix.org/legacy/events/sec03/tech/' + pdf_link
                        
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
                    else:
                        print("未找到 PDF 下载链接")
                else:
                    print(f"访问详细页面失败，状态码: {tech_page_response.status_code}")
        else:
            print("未找到有效的链接或href属性缺失")
else:
    print(f'请求网页失败，状态码：{response.status_code}')
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
url = "https://www.ndss-symposium.org/ndss2017/accepted-papers/"  

# 下载目录
download_folder = r"C:\Users\lyz\Desktop\crawler\NDSS\NDSS_2017"  

# 如果下载目录不存在，创建该目录
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

try:
    # 发送 HTTP 请求
    response = requests.get(url)
    # 检查请求是否成功
    response.raise_for_status()  # 如果请求失败，会抛出异常

    # 解析 HTML 内容
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 找到所有 <p class="paper-link-abs"> 标签
    paper_links = soup.find_all('p', class_='paper-link-abs')
    
    if not paper_links:
        print("未找到任何论文链接。")
    
    for link in paper_links:
        # 找到 <a> 标签
        a_tag = link.find('a')
        if a_tag:
            # 提取 href 属性（这是论文详细页面的链接）
            href = a_tag.get('href')
            
            # 使用正则表达式从 URL 中提取论文标题
            match = re.search(r'/([^/]+)/?$', href)
            if match:
                # 提取最后一部分作为标题
                title = match.group(1)
                
                # 输出 URL 和标题
                print(f'论文 URL: {href}')
                print(f'Title: {title}')
                
                # 构建完整的论文 URL
                paper_url = f"https://www.ndss-symposium.org{href}" if not href.startswith("http") else href
                
                # 进一步访问每篇论文的详细页面
                paper_response = requests.get(paper_url)
                paper_response.raise_for_status()  # 检查请求是否成功
                
                # 解析论文页面内容
                paper_soup = BeautifulSoup(paper_response.content, 'html.parser')
                
                # 查找包含 PDF 下载链接的部分
                new_wrapper_section = paper_soup.find('section', class_='new-wrapper')
                if new_wrapper_section:
                    p_tags = new_wrapper_section.find_all('p')
                    if len(p_tags) >= 2:
                        pdf_link_tag = p_tags[1].find('a', href=re.compile(r'.*\.pdf$'))
                        if pdf_link_tag:
                            pdf_url = pdf_link_tag['href']
                            pdf_url = f"https://www.ndss-symposium.org{pdf_url}" if not pdf_url.startswith('http') else pdf_url
                            
                            # 输出 PDF 链接
                            print(f"PDF 链接: {pdf_url}")
                            
                            # 下载 PDF 文件
                            pdf_response = requests.get(pdf_url)
                            if pdf_response.status_code == 200:
                                # 使用 sanitize_filename 确保文件名合法
                                sanitized_title = sanitize_filename(title)
                                pdf_path = os.path.join(download_folder, f"{sanitized_title}.pdf")
                                
                                # 保存 PDF 文件
                                with open(pdf_path, 'wb') as f:
                                    f.write(pdf_response.content)
                                print(f"已保存 PDF：{pdf_path}")
                            else:
                                print(f"PDF 下载失败: {pdf_url}")
                        else:
                            print(f"未能找到 PDF 链接：{paper_url}")
                    else:
                        print(f"未能找到第二个 <p> 标签：{paper_url}")
                else:
                    print(f"未找到 'new-wrapper' 部分：{paper_url}")
                
                # 随机延迟 1 到 3 秒
                time.sleep(random.randint(1, 3))
            else:
                print(f"在链接 '{href}' 中未能提取到标题。")
        else:
            print("未找到 <a> 标签，跳过此项。")
except requests.exceptions.RequestException as e:
    print(f"请求过程中发生错误: {e}")
except Exception as e:
    print(f"发生未知错误: {e}")

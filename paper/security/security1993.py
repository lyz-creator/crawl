import os
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import threading
from urllib.parse import urljoin

# 清理文件名，使其合法
def sanitize_filename(title)
    # 去除换行符和多余的空格
    title = title.replace('n', '').strip()
    # 限制文件名长度，避免过长导致问题
    title = title[200] if len(title)  200 else title
    # 替换非法字符
    return re.sub(r'[^a-zA-Z0-9-_s]', '_', title)

# 下载目录基础路径
base_download_folder = rCUserslyzDesktopcrawlerSecurity

# 自定义请求头
headers = {
    'User-Agent' 'Mozilla5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 (KHTML, like Gecko) Chrome134.0.0.0 Safari537.36',
}

# 目标网页 URL
url = 'httpswww.usenix.orglegacypublicationslibraryproceedingssec4'

# 提取年份
year = '1993'  # 手动指定年份，因为URL结构可能不同

# 创建该年份的下载目录
year_folder = os.path.join(base_download_folder, fSecurity_{year})
if not os.path.exists(year_folder)
    os.makedirs(year_folder)

# 爬取单个页面的函数
def crawl_page(url)
    try
        # 发送 HTTP 请求获取网页内容
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有的 dt 标签
        dt_tags = soup.find_all('dt')
        
        for dt_tag in dt_tags
            # 在 dt 标签中查找 a 标签，且 a 标签中包含 i 标签
            a_tag = dt_tag.find('a')
            if a_tag
                title = a_tag.get_text(strip=True)
                sanitized_title = sanitize_filename(title)
                paper_url = urljoin(url, a_tag.get('href'))
                
                print(f论文标题 {title})
                print(f论文详细页面链接 {paper_url})
                
                # 请求论文详细页面
                try
                    paper_response = requests.get(paper_url, headers=headers, timeout=30)
                    paper_response.raise_for_status()
                    
                    paper_soup = BeautifulSoup(paper_response.text, 'html.parser')
                    
                    # 在详细页面中优先查找 PDF 链接
                    pdf_tag = paper_soup.find('a', href=re.compile(r'..pdf$'))
                    if pdf_tag
                        pdf_link = urljoin(paper_url, pdf_tag.get('href'))
                        
                        print(fPDF 链接 {pdf_link})
                        
                        # 下载 PDF
                        try
                            pdf_response = requests.get(pdf_link, headers=headers, timeout=30)
                            pdf_response.raise_for_status()
                            
                            pdf_filename = f{sanitized_title}.pdf
                            pdf_path = os.path.join(year_folder, pdf_filename)
                            
                            with open(pdf_path, 'wb') as f
                                f.write(pdf_response.content)
                            print(f已成功下载 PDF {pdf_filename})
                        except Exception as e
                            print(f下载 PDF 时出错 {str(e)})
                    
                    # 如果没有找到 PDF 链接，则查找 HTML 链接
                    else
                        html_tag = paper_soup.find('a', string='HTML', href=re.compile(r'..html$'))
                        if html_tag
                            html_link = urljoin(paper_url, html_tag.get('href'))
                            
                            print(fHTML 链接 {html_link})
                            
                            # 下载 HTML
                            try
                                html_response = requests.get(html_link, headers=headers, timeout=30)
                                html_response.raise_for_status()
                                
                                html_filename = f{sanitized_title}.html
                                html_path = os.path.join(year_folder, html_filename)
                                
                                with open(html_path, 'w', encoding='utf-8') as f
                                    f.write(html_response.text)
                                print(f已成功下载 HTML {html_filename})
                            except Exception as e
                                print(f下载 HTML 时出错 {str(e)})
                        else
                            # 查找 ASCII 下载链接
                            ascii_tag = paper_soup.find('a', string='ASCII', href=re.compile(r'.'))
                            if ascii_tag
                                ascii_link = urljoin(paper_url, ascii_tag.get('href'))
                                
                                print(fASCII 链接 {ascii_link})
                                
                                # 下载 ASCII
                                try
                                    ascii_response = requests.get(ascii_link, headers=headers, timeout=30)
                                    ascii_response.raise_for_status()
                                    
                                    ascii_filename = f{sanitized_title}.txt
                                    ascii_path = os.path.join(year_folder, ascii_filename)
                                    
                                    with open(ascii_path, 'wb') as f
                                        f.write(ascii_response.content)
                                    print(f已成功下载 ASCII {ascii_filename})
                                except Exception as e
                                    print(f下载 ASCII 时出错 {str(e)})
                            else
                                print(未找到 ASCII 下载链接)
                except Exception as e
                    print(f访问论文详细页面时出错 {str(e)})
                
                time.sleep(random.uniform(0.5, 2))  # 随机延迟，避免请求过快
            else
                print(未找到符合条件的 a 标签)
    except Exception as e
        print(f爬取页面时出错 {str(e)})

# 创建线程
thread = threading.Thread(target=crawl_page, args=(url,))
thread.start()
thread.join()

print(爬取完成。)

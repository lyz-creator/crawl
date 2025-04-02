import os
import re
import requests
from bs4 import BeautifulSoup

# 本地 HTML 文件路径
html_path = rCUserslyzDesktophtml.txt

# 下载 PDF 文件夹路径
download_folder = rCUserslyzDesktopcrawlerWiSecWiSec_2024
if not os.path.exists(download_folder)
    os.makedirs(download_folder)

# 清理非法字符用于保存文件名
def sanitize_filename(title)
    return re.sub(r'[]', '_', title)

# 读取本地 HTML 内容
import chardet

# 读取原始字节内容
with open(html_path, 'rb') as f
    raw_data = f.read()

# 自动检测编码
detected = chardet.detect(raw_data)
encoding = detected['encoding'] or 'utf-8'  # fallback

print(f✅ Detected encoding {encoding})

# 解码成字符串
html_content = raw_data.decode(encoding)

# 解析 HTML
soup = BeautifulSoup(html_content, html.parser)
papers = soup.find_all(div, class_=issue-item__content-right)

# ✅ 你提供的完整真实请求头
headers = {
    authority dl.acm.org,
    method GET,
    scheme https,
    accept texthtml,applicationxhtml+xml,applicationxml;q=0.9,imageavif,imagewebp,imageapng,;q=0.8,applicationsigned-exchange;v=b3;q=0.7,
    accept-encoding gzip, deflate, br, zstd,
    accept-language zh-CN,zh;q=0.9,
    cache-control max-age=0,
    cookie MAID=+5ymwe4HodPY103KVZcFJA==; _ga=GA1.2.1593989978.1739954373; CookieConsent={stamp'De0rZoNRZRyQpksVNMpyyWbgzUPx9T9vFW0frMs6rfF3zm8DEFNQ+g==',necessarytrue,preferencestrue,statisticstrue,marketingtrue,method'explicit',ver1,utc1739954384641,region'sg'}; _hjSessionUser_1290436=eyJpZCI6ImYyNjQ3NjA5LTU0YmItNTc0NC1hZmNlLThiY2VkZjdmZDY5ZCIsImNyZWF0ZWQiOjE3Mzk5NTQzNzcwNjUsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1712288833.1743256440; _cfuvid=AE9bzQ.HBrGZA5ny0ug0P_akiZ66F2lUrvleL0zn9Q8-1743581385179-0.0.1.1-604800000; MACHINE_LAST_SEEN=2025-04-02T053007.466-0700; JSESSIONID=23397205450A6FD935B272DC2A6AED05; __cf_bm=9m6FbW1Ez8RX..D5H3RVGCxBOzPKks.k8mo8oBjXmIc-1743597007-1.0.1.1-UOOU2MayXqf1W6gEfkOIF9clBSX4RDgS30Ff_pk86IkapR.DFUfU50dCIi_4VFIPRGxQrl4EMf_5qr4LVzGtqqwn6u00OjnvRUY5A8K5y8M; _hjSession_1290436=eyJpZCI6IjU2MWE5NzlmLWJmYjctNGI1ZS05YmEyLWFlMDFlMWQ2N2M0YiIsImMiOjE3NDM1OTcwMTAxMzQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; cf_clearance=LM_xxgkQQmWNMFpWSiawaDmpmEPPup_anLeAMl0R2Ts-1743597010-1.2.1.1-WeX_8zaLHZIaJch1qLa9euGQa5AEDa7AjT9LKehs50fzZmct8L8vNhTMOOUAT2sc6t.dkyNCCDU3onikRv9Ym9di9QNjD3.5J5DrCvPX98EW7YjSqWzuM6I47N2Q8CyYez0RghcLU5fdhs5DBQulrUNShY3zMxx.lea1FCnvJ8iGFTqPnfgy2ZYyOWsk9wqE4Thz7v0_VdyTkXw36NwxfdZuieSBHABp1s83_eWAuxMzo7Z9YrLmuaQmEi5JdzRXUsJAme5k_uRQ1VcSeZf2aTb1xmNpKe47L4w7BTMcz7EVsDcv_vBo35_dFVJRCXgoDZs.UaH4QqCdkETOsULckB6PTFMQcngF5ir3qXRM35PYv0DPcgtg.NK3JK79wFhEFpmJjPszMe91dOTC_jRIguMKd.EwPsyMx4_tPih3Kro; _hp2_ses_props.1083010732={rhttpsdl.acm.orgdoi10.11453643833.3656118__cf_chl_tk=FZbY0Znr4IzPv9y.fniNrHNoQgMA2pbHHrpJCXUW4yA-1743597000-1.0.1.1-20baSBPe.OkTjbt5m6SgHRIvL4NjbfVRnaecVAhhPws,ts1743597010161,ddl.acm.org,hdoi10.11453643833.3656118}; _ga_JPDX9GZR59=GS1.2.1743597011.16.1.1743597056.0.0.0; _hp2_id.1083010732={userId6381453916055621,pageviewId3893643468371889,sessionId5377959260452717,identitynull,trackerVersion4.0},
    priority u=0, i,
    referer httpsdl.acm.org,
    sec-ch-ua 'Chromium;v=134, NotA-Brand;v=24, Google Chrome;v=134',
    sec-ch-ua-arch 'x86',
    sec-ch-ua-bitness '64',
    sec-ch-ua-full-version '134.0.6998.178',
    sec-ch-ua-full-version-list 'Chromium;v=134.0.6998.178, NotA-Brand;v=24.0.0.0, Google Chrome;v=134.0.6998.178',
    sec-ch-ua-mobile 0,
    sec-ch-ua-model '',
    sec-ch-ua-platform 'Windows',
    sec-ch-ua-platform-version '10.0.0',
    sec-fetch-dest document,
    sec-fetch-mode navigate,
    sec-fetch-site cross-site,
    sec-fetch-user 1,
    upgrade-insecure-requests 1,
    user-agent Mozilla5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 (KHTML, like Gecko) Chrome134.0.0.0 Safari537.36
}


# ⚠️ 注意：请将 headers[cookie] 值中的换行和缩进全部删除，保持为一整行字符串

for idx, paper in enumerate(papers, start=1)
    title_tag = paper.find(h5, class_=issue-item__title)
    if not title_tag
        continue
    a_title = title_tag.find(a)
    if not a_title
        continue
    title = a_title.text.strip()
    sanitized_title = sanitize_filename(title)
    print(f{idx}. Title {title})

    pdf_link_tag = paper.find(a, class_=btn--icon simple-tooltip__block--b red btn)
    if not pdf_link_tag
        print(   ⚠️ No PDF link found.)
        continue

    pdf_href = pdf_link_tag.get(href)
    if not pdf_href.startswith(http)
        pdf_href = httpsdl.acm.org + pdf_href

    print(f   PDF URL {pdf_href})

    # 下载 PDF（使用真实请求头）
    try
        pdf_response = requests.get(pdf_href, headers=headers)
        if pdf_response.status_code == 200
            pdf_path = os.path.join(download_folder, f{sanitized_title}.pdf)
            with open(pdf_path, wb) as f
                f.write(pdf_response.content)
            print(f   ✅ Saved {pdf_path})
        else
            print(f   ❌ Failed to download PDF. Status code {pdf_response.status_code})
    except Exception as e
        print(f   ❌ Exception during download {e})

import os
import re
import requests
from bs4 import BeautifulSoup

# 本地 HTML 文件路径
html_path = r"C:\Users\lyz\Desktop\html.txt"

# 下载 PDF 文件夹路径
download_folder = r"C:\Users\lyz\Desktop\crawler\RAID\RAID_2023_local"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# 清理非法字符用于保存文件名
def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '_', title)

# 读取本地 HTML 内容
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 解析 HTML
soup = BeautifulSoup(html_content, "html.parser")
papers = soup.find_all("div", class_="issue-item__content-right")

# ✅ 你提供的完整真实请求头
headers = {
    "authority": "dl.acm.org",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "MAID=+5ymwe4HodPY103KVZcFJA==; _ga=GA1.2.1593989978.1739954373; CookieConsent={stamp:%27De0rZoNRZRyQpksVNMpyyWbgzUPx9T9vFW0frMs6rfF3zm8DEFNQ+g==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1739954384641%2Cregion:%27sg%27}; _hjSessionUser_1290436=eyJpZCI6ImYyNjQ3NjA5LTU0YmItNTc0NC1hZmNlLThiY2VkZjdmZDY5ZCIsImNyZWF0ZWQiOjE3Mzk5NTQzNzcwNjUsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1712288833.1743256440; MACHINE_LAST_SEEN=2025-04-02T00%3A55%3A57.769-07%3A00; JSESSIONID=EB31464DC30156B63671693204AF388A; _hp2_ses_props.1083010732=%7B%22r%22%3A%22https%3A%2F%2Fraid2023.org%2Faccepted_open.html%22%2C%22ts%22%3A1743580560684%2C%22d%22%3A%22dl.acm.org%22%2C%22h%22%3A%22%2Fdoi%2F10.1145%2F3607199.3607200%22%7D; _hjSession_1290436=eyJpZCI6ImI3ZjI1ZmI5LTZiZDEtNDE4NS05MTcyLTA4OGI3NGYxMDUzNSIsImMiOjE3NDM1ODA1NjE5ODYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; __cf_bm=r1ZCMiESsl1rRDIXiaXrpyfos_62bWsmoJGYaxTp2aM-1743581385-1.0.1.1-Lk3sGzDCyDznfnBLRysnu4BmhxB16hcxq9ZCHthS8U.dNLkk7Qxyi7TlMcKA5V33biSsLySwrmAVRMXLStq9H4TLPptBMUQeucIpm4WyL3g; _cfuvid=AE9bzQ.HBrGZA5ny0ug0P_akiZ66F2lUrvleL0zn9Q8-1743581385179-0.0.1.1-604800000; cf_clearance=7lY9w55uhGLQibEvvVY.LaTVC95o_3x8tEuZ_Z5p0F4-1743581392-1.2.1.1-UxZAaCM5Ewu6in0_L9GhKOm9L2RjcYHtvGOaO5svvUOvHJvDwcT50zvqqtX_gl6RrZIpO1hYPLZ9dW3WLefkdHgQuz6Kaox6GY9XH5hXN_BX2w.yqPIzxsr6V2zKc4wjjEwdRqUZ2peW2U8FgkpwdlbblresYq3QpHILiNzhedS1GKpDry04nBCGpaLOf7sYxXGA0aYO9Yq0od.T_njrBjGhtUUrZRlCcSbjagRDA55qSknH_8sz3I3rZ1KMVMZlPYhMCDDYvsrkrzv7NZlZ1AqqkjtGkcWa1ATvpaSZOvbvUK30WSB7Su5i3Qxj4fsrccVsoi1yS.tB28pQ5OHFb0pI5UGNo892xOEgu4xvTAty7SH8RmlHzVkx88QtuYk83sVo9blRVRHT5wudXuYKfG79HGcv_lRMuuDAJFvmf2k; _ga_JPDX9GZR59=GS1.2.1743580563.15.1.1743581405.0.0.0; _hp2_id.1083010732=%7B%22userId%22%3A%226381453916055621%22%2C%22pageviewId%22%3A%223577861714203958%22%2C%22sessionId%22%3A%227236345621725937%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D",
    "referer": "https://dl.acm.org/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"134.0.6998.178"',
    "sec-ch-ua-full-version-list": '"Chromium";v="134.0.6998.178", "Not:A-Brand";v="24.0.0.0", "Google Chrome";v="134.0.6998.178"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"10.0.0"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

# ⚠️ 注意：请将 headers["cookie"] 值中的换行和缩进全部删除，保持为一整行字符串

for idx, paper in enumerate(papers, start=1):
    title_tag = paper.find("h5", class_="issue-item__title")
    if not title_tag:
        continue
    a_title = title_tag.find("a")
    if not a_title:
        continue
    title = a_title.text.strip()
    sanitized_title = sanitize_filename(title)
    print(f"{idx}. Title: {title}")

    pdf_link_tag = paper.find("a", class_="btn--icon simple-tooltip__block--b red btn")
    if not pdf_link_tag:
        print("   ⚠️ No PDF link found.")
        continue

    pdf_href = pdf_link_tag.get("href")
    if not pdf_href.startswith("http"):
        pdf_href = "https://dl.acm.org" + pdf_href

    print(f"   PDF URL: {pdf_href}")

    # 下载 PDF（使用真实请求头）
    try:
        pdf_response = requests.get(pdf_href, headers=headers)
        if pdf_response.status_code == 200:
            pdf_path = os.path.join(download_folder, f"{sanitized_title}.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf_response.content)
            print(f"   ✅ Saved: {pdf_path}")
        else:
            print(f"   ❌ Failed to download PDF. Status code: {pdf_response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception during download: {e}")

# filter_streaming_zh.py
from datasets import load_dataset
import json
from tqdm.auto import tqdm

class ChineseTextFilter:
    """按中文关键词命中数与密度过滤文本。"""
    def __init__(self, keywords, hit_times=5, hit_ratio=0.05):
        """
        keywords: 可迭代的中文关键词列表（无需小写化）
        hit_times: 不同关键词最少命中数
        hit_ratio: 命中字符数／文本总长度最小比例
        """
        self.hit_times = hit_times
        self.hit_ratio = hit_ratio
        # 这里不做长短关键词区分，中文直接全部当 short_kw
        self.keywords = list(dict.fromkeys(keywords))  # 去重但保留顺序

    def match(self, text: str) -> bool:
        """
        返回 True 当文本 text 中：
         - 至少 hit_times 个不同关键词出现
         - 总命中字符数 / len(text) >= hit_ratio
        """
        total_len = len(text)
        if total_len == 0:
            return False

        unique_hits = 0
        char_hits   = 0
        for kw in self.keywords:
            cnt = text.count(kw)
            if cnt:
                unique_hits += 1
                char_hits   += cnt * len(kw)
            # 如果已经既达词数又达比例，可提前返回
            if (unique_hits >= self.hit_times and 
                char_hits / total_len >= self.hit_ratio):
                return True

        return unique_hits >= self.hit_times and (char_hits / total_len) >= self.hit_ratio


def main():
    # 1. 填入你的 200 条中文关键词
    zh_crypto_keywords = [
    "密码学", "对称加密", "非对称加密", "公钥", "私钥", "密钥交换", "密钥生成", "密钥管理", 
    "RSA算法", "ECC椭圆曲线加密", "AES算法", "DES算法", "3DES算法", "Blowfish算法", "Twofish算法", 
    "RC4算法", "RC5算法", "RC6算法", "SM2算法", "SM3算法", "SM4算法", "国密算法", "哈希函数", "MD5算法", 
    "SHA-1算法", "SHA-2算法", "SHA-256", "SHA-3算法", "哈希碰撞", "信息摘要", "数字签名", "认证机制", 
    "身份认证", "消息认证码", "HMAC", "零知识证明", "密码协议", "SSL/TLS协议", "HTTPS安全传输", 
    "VPN虚拟专用网", "SSH协议", "区块链安全", "密码攻击", "暴力破解", "字典攻击", "彩虹表", "侧信道攻击", 
    "时序攻击", "差分密码分析", "线性密码分析", "中间人攻击", "重放攻击", "拒绝服务攻击", "密码泄露", 
    "密码存储", "盐值", "PBKDF2", "bcrypt", "scrypt", "密码复杂度", "一次性密码", "二次验证", 
    "生物识别认证", "数据加密", "端到端加密", "全盘加密", "数据脱敏", "数据完整性", "数据隐私保护", 
    "安全通信", "信息安全", "网络安全", "无线安全", "数据包捕获", "封包分析", "数据泄露", "密码恢复", 
    "密码管理器", "口令喷射", "钓鱼攻击", "社会工程学", "网络钓鱼", "虚假网站", "恶意软件", "木马病毒", 
    "勒索软件", "蠕虫病毒", "后门", "零日漏洞", "漏洞利用", "安全审计", "风险评估", "安全合规", "隐写术", 
    "安全多方计算", "同态加密", "格式加密", "门限密码学", "量子密码学", "后量子密码学", "格密码学", "哈希锁定", 
    "Merkle树", "零知识电路", "安全引导", "加密货币", "比特币", "以太坊", "区块链智能合约", "加密钱包", "去中心化", 
    "多重签名", "密钥恢复", "密钥托管", "密钥轮换", "密钥生命周期", "数据溯源", "审计日志", "安全令牌", "硬件安全模块", 
    "安全芯片", "身份管理", "访问控制", "RBAC角色权限控制", "ABAC属性权限控制", "安全策略", "多因子认证", 
    "单点登录", "数字证书", "证书颁发机构", "证书撤销", "PKI基础设施", "信任锚", "根证书", "中间证书", 
    "OCSP协议", "CRL证书吊销列表", "证书透明性", "双向认证", "硬件加密", "软件加密", "Web加密", "邮件加密", 
    "信息隐藏", "密码推测", "敏感信息保护", "防火墙", "入侵检测", "入侵防御", "漏洞扫描", "渗透测试", "安全防护",
    "安全运营中心", "安全事件响应", "恢复机制", "异常检测", "行为分析", "网络流量分析", "数据包嗅探", "证书劫持", 
    "安全更新", "漏洞修复", "零信任安全", "云安全", "虚拟化安全", "物联网安全", "移动安全", "应用安全", "代码审计", 
    "软件供应链安全", "可信计算", "TPM可信平台模块", "虚拟专用网络", "反病毒软件", "恶意流量检测", "证据保全", 
    "网络取证", "法证分析", "数据恢复", "网络追踪", "DNS安全", "域名劫持", "网络隔离", "跨站脚本攻击", "SQL注入", 
    "命令注入", "CSRF攻击", "会话劫持", "Cookie安全"
    ]

    # 2. 初始化过滤器
    filterer = ChineseTextFilter(
        keywords=zh_crypto_keywords,
        hit_times=5,
        hit_ratio=0.05
    )

    # 3. 流式加载 Hugging Face 数据集（中文分支），使用身份认证
    ds = load_dataset(
        "uonlp/CulturaX",
        "zh",             # 切换到中文
        split="train",
        streaming=True,
    )

    # 4. 逐条过滤，写入本地 JSONL
    output_path = "filtered_zh.jsonl"
    with open(output_path, "w", encoding="utf-8") as fout:
        for example in tqdm(ds, desc="Streaming & Filtering (ZH)"):
            text = example.get("text", "")
            if text and filterer.match(text):
                # 这里只保留 text 字段，也可加其它字段
                fout.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")

    print(f"完成！过滤结果已保存到 {output_path}")

if __name__ == "__main__":
    main()

    
    
'''
# filter_streaming_parallel.py

from datasets import load_dataset
import json
from tqdm.auto import tqdm
from concurrent.futures import ProcessPoolExecutor
from functools import partial

# 重用你原来的过滤器，只不过移成顶层可 picklable
class ChineseTextFilter:
    def __init__(self, keywords, hit_times=5, hit_ratio=0.05):
        self.hit_times, self.hit_ratio = hit_times, hit_ratio
        self.keywords = list(dict.fromkeys(keywords))
    def match(self, text: str) -> bool:
        total_len = len(text)
        if total_len == 0:
            return False
        u, c = 0, 0
        for kw in self.keywords:
            cnt = text.count(kw)
            if cnt:
                u += 1
                c += cnt * len(kw)
            if u >= self.hit_times and c/total_len >= self.hit_ratio:
                return True
        return u >= self.hit_times and c/total_len >= self.hit_ratio

def chunked(iterator, size):
    """每次从 iterator 里拿 size 条，返回 list"""
    chunk = []
    for x in iterator:
        chunk.append(x)
        if len(chunk) >= size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

def worker_match(text, keywords, hit_times, hit_ratio):
    """供子进程调用的函数"""
    # 每个子进程都会重新构造自己的过滤器实例
    filt = ChineseTextFilter(keywords, hit_times, hit_ratio)
    return text if filt.match(text) else None

def main():
    # 1. 中文关键词列表（补齐你的200条）
    zh_crypto_keywords = [
    "密码学", "对称加密", "非对称加密", "公钥", "私钥", "密钥交换", "密钥生成", "密钥管理", 
    "RSA算法", "ECC椭圆曲线加密", "AES算法", "DES算法", "3DES算法", "Blowfish算法", "Twofish算法", 
    "RC4算法", "RC5算法", "RC6算法", "SM2算法", "SM3算法", "SM4算法", "国密算法", "哈希函数", "MD5算法", 
    "SHA-1算法", "SHA-2算法", "SHA-256", "SHA-3算法", "哈希碰撞", "信息摘要", "数字签名", "认证机制", 
    "身份认证", "消息认证码", "HMAC", "零知识证明", "密码协议", "SSL/TLS协议", "HTTPS安全传输", 
    "VPN虚拟专用网", "SSH协议", "区块链安全", "密码攻击", "暴力破解", "字典攻击", "彩虹表", "侧信道攻击", 
    "时序攻击", "差分密码分析", "线性密码分析", "中间人攻击", "重放攻击", "拒绝服务攻击", "密码泄露", 
    "密码存储", "盐值", "PBKDF2", "bcrypt", "scrypt", "密码复杂度", "一次性密码", "二次验证", 
    "生物识别认证", "数据加密", "端到端加密", "全盘加密", "数据脱敏", "数据完整性", "数据隐私保护", 
    "安全通信", "信息安全", "网络安全", "无线安全", "数据包捕获", "封包分析", "数据泄露", "密码恢复", 
    "密码管理器", "口令喷射", "钓鱼攻击", "社会工程学", "网络钓鱼", "虚假网站", "恶意软件", "木马病毒", 
    "勒索软件", "蠕虫病毒", "后门", "零日漏洞", "漏洞利用", "安全审计", "风险评估", "安全合规", "隐写术", 
    "安全多方计算", "同态加密", "格式加密", "门限密码学", "量子密码学", "后量子密码学", "格密码学", "哈希锁定", 
    "Merkle树", "零知识电路", "安全引导", "加密货币", "比特币", "以太坊", "区块链智能合约", "加密钱包", "去中心化", 
    "多重签名", "密钥恢复", "密钥托管", "密钥轮换", "密钥生命周期", "数据溯源", "审计日志", "安全令牌", "硬件安全模块", 
    "安全芯片", "身份管理", "访问控制", "RBAC角色权限控制", "ABAC属性权限控制", "安全策略", "多因子认证", 
    "单点登录", "数字证书", "证书颁发机构", "证书撤销", "PKI基础设施", "信任锚", "根证书", "中间证书", 
    "OCSP协议", "CRL证书吊销列表", "证书透明性", "双向认证", "硬件加密", "软件加密", "Web加密", "邮件加密", 
    "信息隐藏", "密码推测", "敏感信息保护", "防火墙", "入侵检测", "入侵防御", "漏洞扫描", "渗透测试", "安全防护",
    "安全运营中心", "安全事件响应", "恢复机制", "异常检测", "行为分析", "网络流量分析", "数据包嗅探", "证书劫持", 
    "安全更新", "漏洞修复", "零信任安全", "云安全", "虚拟化安全", "物联网安全", "移动安全", "应用安全", "代码审计", 
    "软件供应链安全", "可信计算", "TPM可信平台模块", "虚拟专用网络", "反病毒软件", "恶意流量检测", "证据保全", 
    "网络取证", "法证分析", "数据恢复", "网络追踪", "DNS安全", "域名劫持", "网络隔离", "跨站脚本攻击", "SQL注入", 
    "命令注入", "CSRF攻击", "会话劫持", "Cookie安全"
    ]
    HIT_TIMES = 5
    HIT_RATIO = 0.05

    # 2. 流式加载
    ds = load_dataset(
        "uonlp/CulturaX", "zh",
        split="train",
        streaming=True,
    )

    # 3. 准备进程池
    max_workers = 10
    # worker_match 接受 (text, keywords, hit_times, hit_ratio)
    fn = partial(worker_match, keywords=zh_crypto_keywords,
                 hit_times=HIT_TIMES, hit_ratio=HIT_RATIO)

    out_path = "filtered_zh_parallel.jsonl"
    with open(out_path, "w", encoding="utf-8") as fout, \
         ProcessPoolExecutor(max_workers=max_workers) as executor:

        # 4. 分批取，每 batch_size 条文本提交一次并行
        batch_size = 100    
        for batch in tqdm(chunked((ex["text"] for ex in ds), batch_size),
                          desc="Batching"):
            # executor.map 返回与 batch 等长的结果序列
            for res in executor.map(fn, batch):
                if res is not None:
                    fout.write(json.dumps({"text": res}, ensure_ascii=False) + "\n")

    print("Done! Results in", out_path)

if __name__ == "__main__":
    main()
'''
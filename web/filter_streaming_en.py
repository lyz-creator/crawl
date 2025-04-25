# filter_streaming.py

from datasets import load_dataset
import json
from tqdm.auto import tqdm

class CryptoTextFilter:
    """按关键词命中数与密度过滤文本。"""
    def __init__(self, keywords, hit_times=5, hit_ratio=0.04):
        self.hit_times = hit_times
        self.hit_ratio = hit_ratio
        long_kw, short_kw = [], []
        for kw in set(keywords):
            kw = kw.lower()
            if len(kw) > 10 or (len(kw) > 5 and ' ' in kw):
                long_kw.append(kw)
            else:
                short_kw.append(kw)
        self.long_kw = long_kw
        self.short_kw = short_kw

    def match(self, text: str) -> bool:
        t = text.lower()
        unique_hits = 0
        char_hits = 0
        # 匹配长关键词
        for kw in self.long_kw:
            if kw in t:
                cnt = t.count(kw)
                unique_hits += 1
                char_hits += cnt * len(kw)
        # 如果还未达标，再匹配短关键词
        if unique_hits < self.hit_times or char_hits / max(1, len(t)) < self.hit_ratio:
            words = t.split()
            for kw in self.short_kw:
                cnt = words.count(kw)
                if cnt:
                    unique_hits += 1
                    char_hits += cnt * len(kw)
        return unique_hits >= self.hit_times and (char_hits / max(1, len(t))) >= self.hit_ratio


def main():
    # 1. 定义你的英文关键词列表
    en_crypto_keywords = [
    "Cryptography", "Symmetric Encryption", "Asymmetric Encryption", "Public Key", 
    "Private Key", "Key Exchange", "Key Generation", "Key Management", "RSA Algorithm", 
    "ECC (Elliptic Curve Crypto)", "AES Algorithm", "DES Algorithm", "3DES Algorithm", 
    "Blowfish Algorithm", "Twofish Algorithm", "RC4 Algorithm", "RC5 Algorithm", 
    "RC6 Algorithm", "SM2 Algorithm", "SM3 Algorithm", "SM4 Algorithm", 
    "Chinese National Algorithm", "Hash Function", "MD5 Algorithm", "SHA-1 Algorithm", 
    "SHA-2 Algorithm", "SHA-256", "SHA-3 Algorithm", "Hash Collision", "Message Digest", 
    "Digital Signature", "Authentication Mechanism", "Identity Authentication", 
    "Message Authentication Code", "HMAC", "Zero Knowledge Proof", "Cryptographic Protocol", 
    "SSL/TLS Protocol", "HTTPS Secure Transmission", "VPN (Virtual Private Network)", 
    "SSH Protocol", "Blockchain Security", "Cryptographic Attack", "Brute Force Attack", 
    "Dictionary Attack", "Rainbow Table", "Side Channel Attack", "Timing Attack", 
    "Differential Cryptanalysis", "Linear Cryptanalysis", "Man-in-the-Middle Attack", 
    "Replay Attack", "Denial-of-Service Attack", "Password Leak", "Password Storage", 
    "Salt Value", "PBKDF2", "bcrypt", "scrypt", "Password Complexity", 
    "One-Time Password (OTP)", "Two-Factor Authentication", "Biometric Authentication", 
    "Data Encryption", "End-to-End Encryption", "Full Disk Encryption", "Data Masking", 
    "Data Integrity", "Data Privacy Protection", "Secure Communication", 
    "Information Security", "Network Security", "Wireless Security", "Packet Capture", 
    "Packet Analysis", "Data Leak", "Password Recovery", "Password Manager", 
    "Password Spraying", "Phishing Attack", "Social Engineering", "Web Phishing", 
    "Fake Website", "Malware", "Trojan Horse", "Ransomware", "Worm Virus", "Backdoor", 
    "Zero-Day Vulnerability", "Vulnerability Exploit", "Security Audit", "Risk Assessment", 
    "Security Compliance", "Steganography", "Secure Multi-Party Computation", 
    "Homomorphic Encryption", "Format-Preserving Encryption", "Threshold Cryptography", 
    "Quantum Cryptography", "Post-Quantum Cryptography", "Lattice-based Cryptography", 
    "Hash Lock", "Merkle Tree", "Zero Knowledge Circuit", "Secure Boot", "Cryptocurrency", 
    "Bitcoin", "Ethereum", "Blockchain Smart Contract", "Crypto Wallet", "Decentralization", 
    "Multi-Signature", "Key Recovery", "Key Escrow", "Key Rotation", "Key Lifecycle", 
    "Data Traceability", "Audit Log", "Security Token", "Hardware Security Module (HSM)", 
    "Secure Chip", "Identity Management", "Access Control", "Role-Based Access Control", 
    "Attribute-Based Access Control", "Security Policy", "Multi-Factor Authentication", 
    "Single Sign-On (SSO)", "Digital Certificate", "Certificate Authority (CA)", 
    "Certificate Revocation", "Public Key Infrastructure (PKI)", "Trust Anchor", 
    "Root Certificate", "Intermediate Certificate", "OCSP Protocol", 
    "Certificate Revocation List (CRL)", "Certificate Transparency", "Mutual Authentication", 
    "Hardware Encryption", "Software Encryption", "Web Encryption", "Email Encryption", 
    "Information Hiding", "Password Guessing", "Sensitive Information Protection", 
    "Firewall", "Intrusion Detection", "Intrusion Prevention", "Vulnerability Scan", 
    "Penetration Testing", "Security Protection", "Security Operation Center (SOC)", 
    "Security Incident Response", "Recovery Mechanism", "Anomaly Detection", "Behavior Analysis", 
    "Network Traffic Analysis", "Packet Sniffing", "Certificate Hijacking", "Security Update", 
    "Vulnerability Patch", "Zero Trust Security", "Cloud Security", "Virtualization Security", 
    "IoT Security", "Mobile Security", "Application Security", "Code Audit", 
    "Software Supply Chain Security", "Trusted Computing", "Trusted Platform Module (TPM)", 
    "Virtual Private Network (VPN)", "Antivirus Software", "Malicious Traffic Detection", 
    "Evidence Preservation", "Network Forensics", "Forensic Analysis", "Data Recovery", 
    "Network Tracking", "DNS Security", "Domain Hijacking", "Network Segmentation", 
    "Cross-Site Scripting (XSS)", "SQL Injection", "Command Injection", "CSRF Attack", 
    "Session Hijacking", "Cookie Security"
        # …在这里补全你的200个关键词…
    ]

    # 2. 初始化过滤器
    filterer = CryptoTextFilter(
        keywords=en_crypto_keywords,
        hit_times=5,
        hit_ratio=0.04
    )

    # 3. 流式加载 Hugging Face 数据集（无需预先下载 parquet）
    ds = load_dataset(
        "uonlp/CulturaX",
        "en",
        split="train",
        streaming=True
    )

    # 4. 逐条过滤，并写入本地 JSONL 文件
    output_path = "filtered_en.jsonl"
    with open(output_path, "w", encoding="utf-8") as fout:
        for example in tqdm(ds, desc="Streaming & Filtering"):
            text = example.get("text", "")
            if text and filterer.match(text):
                # 你也可以写入更多字段，这里只写 text
                fout.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")

    print(f"Done! Filtered data saved to {output_path}")

if __name__ == "__main__":
    main()

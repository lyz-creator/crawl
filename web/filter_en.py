# filter.py

import os
import json
import tqdm
import pandas as pd
import multiprocessing
import pyarrow.parquet as pq
from tqdm import tqdm
from keywords import en_crypto_words  # 或者你的英文关键词列表变量名

# 配置区
PARQUET_FOLDER = r'C:\Users\DGT_X\Desktop\crypto\en_downloads'
SAVE_ROOT      = r'C:\Users\DGT_X\Desktop\crypto\en_crypto'
LANG           = 'en'

THRESHOLD = {
    'en': {'HIT_TIMES_THRESHOLD': 5, 'HIT_RATIO_THRESHOLD': 0.04},
    'zh': {'HIT_TIMES_THRESHOLD': 5, 'HIT_RATIO_THRESHOLD': 0.05},
    'jp': {'HIT_TIMES_THRESHOLD': 5, 'HIT_RATIO_THRESHOLD': 0.05},
    'ru': {'HIT_TIMES_THRESHOLD': 4, 'HIT_RATIO_THRESHOLD': 0.02},
    'es': {'HIT_TIMES_THRESHOLD': 4, 'HIT_RATIO_THRESHOLD': 0.04},
    'fr': {'HIT_TIMES_THRESHOLD': 4, 'HIT_RATIO_THRESHOLD': 0.04},
}
HIT_TIMES_THRESHOLD = THRESHOLD[LANG]['HIT_TIMES_THRESHOLD']
HIT_RATIO_THRESHOLD = THRESHOLD[LANG]['HIT_RATIO_THRESHOLD']


class CryptoTextFilter:
    """并行过滤大规模 Parquet 文本，按关键词抽取 Crypto 相关样本。"""
    def __init__(self):
        # 绑定配置
        self.PARQUET_FOLDER = PARQUET_FOLDER
        self.SAVE_ROOT      = SAVE_ROOT
        os.makedirs(self.SAVE_ROOT, exist_ok=True)

        # 加载关键词
        self.keywords = self.load_keywords()

    @staticmethod
    def load_keywords():
        """加载并划分长短关键词两类，加速匹配。"""
        kws = list(set(en_crypto_words))
        kws = [w.lower() for w in kws]
        long_kw, short_kw = [], []
        for kw in kws:
            if len(kw) > 10 or (len(kw) > 5 and ' ' in kw):
                long_kw.append(kw)
            else:
                short_kw.append(kw)
        return long_kw, short_kw

    def match_keywords(self, text, en_like=True):
        """
        统计文本中命中关键词的种类数 & 总字符数，判断是否达到阈值
        en_like: True → 按英文空格分词；False → 直接 substring
        """
        text = text.lower()
        unique_hits = 0
        char_hits   = 0
        long_kw, short_kw = self.keywords

        if en_like:
            # 先匹配长关键词
            for kw in long_kw:
                if kw in text:
                    unique_hits += 1
                    char_hits   += text.count(kw) * len(kw)
            # 达到长关键词门槛可直接返回
            if (unique_hits >= HIT_TIMES_THRESHOLD and 
                char_hits / max(1, len(text)) >= HIT_RATIO_THRESHOLD):
                return True
            # 否则再分词匹配短关键词
            words = text.split()
            for kw in short_kw:
                cnt = words.count(kw)
                if cnt:
                    unique_hits += 1
                    char_hits   += cnt * len(kw)
        else:
            # 中文或无空格语言，直接遍历所有关键词
            for kw in long_kw + short_kw:
                cnt = text.count(kw)
                if cnt:
                    unique_hits += 1
                    char_hits   += cnt * len(kw)

        return (unique_hits >= HIT_TIMES_THRESHOLD and
                char_hits / max(1, len(text)) >= HIT_RATIO_THRESHOLD)

    def filter_file(self, filename):
        """
        分 Row-Group 读 Parquet，逐段匹配并收集命中文本，
        最后一次性写入 JSON。
        """
        pf = pq.ParquetFile(filename)
        total = pf.metadata.num_rows  # 整个文件的行数
        hits = 0

        # 用 tqdm 建一个总进度条
        pbar = tqdm(total=total,
                    desc=os.path.basename(filename),
                    unit='row',
                    leave=False)

        crypto_texts = []
        for rg in range(pf.num_row_groups):
            tbl = pf.read_row_group(rg, columns=['text'])
            df  = tbl.to_pandas()
            for text in df['text'].astype(str):
                pbar.update(1)
                if self.match_keywords(text):
                    hits += 1
                    crypto_texts.append(text)

        pbar.close()

        # 打印进度
        print(f'{filename} done. Hits: {hits}/{total}  Ratio: {hits/total*100:.2f}%')

        # 保存结果
        base = os.path.basename(filename).rsplit('.', 1)[0]
        out  = {
            'text_cnt': total,
            'crypto_text_cnt': hits,
            'crypto_text_ratio': hits/total,
            'HIT_TIMES_THRESHOLD': HIT_TIMES_THRESHOLD,
            'HIT_RATIO_THRESHOLD': HIT_RATIO_THRESHOLD,
            'crypto_texts': crypto_texts
        }
        save_path = os.path.join(self.SAVE_ROOT, f'{base}.json')
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=4)

    def filter_data(self):
        """文件级并行：对每个 Parquet 文件调用 filter_file。"""
        files = [
            os.path.join(self.PARQUET_FOLDER, fn)
            for fn in os.listdir(self.PARQUET_FOLDER)
            if fn.endswith('.parquet')
               and os.path.getsize(os.path.join(self.PARQUET_FOLDER, fn)) > 1<<30
               and not os.path.exists(os.path.join(self.SAVE_ROOT, fn.rsplit('.',1)[0] + '.json'))
        ]
        print(f'Total {len(files)} files to process.')

        pool = multiprocessing.Pool(processes=min(10, len(files)))
        pool.map(self.filter_file, files)
        pool.close()
        pool.join()


if __name__ == "__main__":
    CryptoTextFilter().filter_data()

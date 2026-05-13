"""
/d/newwork/storylens/shakespeare_rag/pipeline/fetcher.py
구텐베르크에서 셰익스피어 전집 다운로드 후 작품별로 분리
"""
import requests
import os
import re
import json
import time

# 작품 목록 [ 제목 : 장르 ]
SHAKESPEARE_PLAYS = {
    # 비극 (Tragedy)
    "Hamlet":                    "tragedy",
    "Macbeth":                   "tragedy",
    "Othello":                   "tragedy",
    "King Lear":                 "tragedy",
    "Romeo and Juliet":          "tragedy",
    "Julius Caesar":             "tragedy",
    "Antony and Cleopatra":      "tragedy",
    "Coriolanus":                "tragedy",
    "Titus Andronicus":          "tragedy",
    "Timon of Athens":           "tragedy",
    "Troilus and Cressida":      "tragedy",
    "Cymbeline":                 "tragedy",

    # 희극 (Comedy)
    "A Midsummer Night's Dream": "comedy",
    "Much Ado About Nothing":    "comedy",
    "The Merchant of Venice":    "comedy",
    "As You Like It":            "comedy",
    "Twelfth Night":             "comedy",
    "The Taming of the Shrew":   "comedy",
    "The Comedy of Errors":      "comedy",
    "The Two Gentlemen of Verona": "comedy",
    "The Merry Wives of Windsor": "comedy",
    "All's Well That Ends Well": "comedy",
    "Measure for Measure":       "comedy",
    "Love's Labour's Lost":      "comedy",
    "The Tempest":               "comedy",
    "The Winter's Tale":         "comedy",
    "Pericles":                  "comedy",
    "The Two Noble Kinsmen":     "comedy",

    # 사극 (History)
    "Richard II":                "history",
    "Henry IV Part 1":           "history",
    "Henry IV Part 2":           "history",
    "Henry V":                   "history",
    "Henry VI Part 1":           "history",
    "Henry VI Part 2":           "history",
    "Henry VI Part 3":           "history",
    "Richard III":               "history",
    "King John":                 "history",
    "Henry VIII":                "history",
}

# 구텐베르크 다운로드 횟수 (대중 선호도 데이터)
GUTENBERG_DOWNLOADS = {
    "Romeo and Juliet":          74574,
    "Hamlet":                    13874,
    "A Midsummer Night's Dream": 7797,
    "The Tempest":               6630,
    "Macbeth":                   6232,
    "As You Like It":            4769,
    "Othello":                   3800,
    "King Lear":                 3500,
    "Julius Caesar":             3200,
    "The Merchant of Venice":    2900,
    "Much Ado About Nothing":    2700,
    "Twelfth Night":             2500,
}


# 다운로드 함수

def download_complete_works(save_dir="data/raw"):
    """구텐베르크 셰익스피어 전집( ID : 100 ) 다운로드"""
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "shakespeare_complete.txt")

    if os.path.exists(save_path):
        print(f"이미 다운로드됨 : {save_path}")
        return save_path
    
    urls = [
        "https://www.gutenberg.org/files/100/100-0.txt",
        "https://gutenberg.org/cache/epub/100/pg100.txt",
    ]
    headers = {"User-Agent": "Mozilla/5.0 (compatible; story-lens research project)"}

    for url in urls:
        try:
            print(f"다운로드 시도 중: {url}")
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"다운로드 완료: {save_path}")
            return save_path
        except requests.RequestException as e:
            print(f"실패 ({url}): {e}")
            time.sleep(2)

    print("모든 URL에서 다운로드 실패")
    return None


def main():
    print("=" * 50)
    print("🎭 셰익스피어 데이터 파이프라인 시작!")
    print("=" * 50)

    # 1. 다운로드
    raw_path = download_complete_works()
    if not raw_path:
        return

if __name__ == "__main__":
    main()
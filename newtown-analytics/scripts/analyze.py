"""
NEWTOWN Tweet Analytics - データ処理スクリプト

usage:
    python analyze.py
    python analyze.py --csv-dir ../data/tweet_analytics --out ../knowledge/analysis_output.json

出力: analysis_output.json (newtown-tweet-analytics スキルの各サブエージェントが参照する中間ファイル)
"""

import argparse
import json
import re
from pathlib import Path
from collections import defaultdict


# ---------------------------------------------------------------------------
# CSV パーサー（標準ライブラリのみ使用）
# ---------------------------------------------------------------------------

def parse_csv(path: Path) -> list[dict]:
    import csv
    rows = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            post_id = row.get("Post id", "").strip()
            if not post_id:
                continue
            try:
                rows.append({
                    "post_id":        post_id,
                    "date":           row["Date"].strip(),
                    "text":           row["Post text"].strip(),
                    "link":           row["Post Link"].strip(),
                    "impressions":    int(row["Impressions"] or 0),
                    "likes":          int(row["Likes"] or 0),
                    "engagements":    int(row["Engagements"] or 0),
                    "bookmarks":      int(row["Bookmarks"] or 0),
                    "shares":         int(row["Shares"] or 0),
                    "new_follows":    int(row["New follows"] or 0),
                    "replies":        int(row["Replies"] or 0),
                    "reposts":        int(row["Reposts"] or 0),
                    "profile_visits": int(row["Profile visits"] or 0),
                    "detail_expands": int(row["Detail Expands"] or 0),
                    "url_clicks":     int(row["URL Clicks"] or 0),
                    "hashtag_clicks": int(row["Hashtag Clicks"] or 0),
                    "permalink_clicks": int(row["Permalink Clicks"] or 0),
                })
            except (ValueError, KeyError):
                continue
    return rows


def load_all_csvs(csv_dir: Path) -> tuple[list[dict], int]:
    posts = []
    seen_ids = set()
    csv_files = sorted(csv_dir.glob("*.csv"))
    csv_count = len(csv_files)
    for csv_file in csv_files:
        for row in parse_csv(csv_file):
            if row["post_id"] not in seen_ids:
                seen_ids.add(row["post_id"])
                posts.append(row)
    return posts, csv_count


# ---------------------------------------------------------------------------
# 派生指標の計算
# ---------------------------------------------------------------------------

def add_derived_metrics(posts: list[dict]) -> list[dict]:
    for p in posts:
        imp = p["impressions"]
        p["ctr"]             = round(p["url_clicks"] / imp, 4) if imp > 0 else 0.0
        p["engagement_rate"] = round(p["engagements"] / imp, 4) if imp > 0 else 0.0
        p["viral_score"]     = round((p["reposts"] + p["replies"]) / imp, 4) if imp > 0 else 0.0
    return posts


# ---------------------------------------------------------------------------
# フック分類
# ---------------------------------------------------------------------------

HOOK_PATTERNS = [
    ("事件名+実行中", r"強盗実行中|犯罪実行中|出陣中"),
    ("が始まる/始まった", r"が始まる|始まった"),
    ("時刻告知",     r"^\d{1,2}時"),
    ("修正・報告",   r"^\[修正|^\[バグ|^\[報告"),
    ("感情先行",     r"^傑作|^今めちゃ|^熱い"),
    ("サービス紹介", r"StreamerHub|MultiView|マルチビュー"),
    ("質問形",       r"[？?]"),
]

def classify_hook(text: str) -> str:
    first_line = text.split("\n")[0][:20]
    for label, pattern in HOOK_PATTERNS:
        if re.search(pattern, first_line):
            return label
    return "その他"

def analyze_hooks(posts: list[dict]) -> list[dict]:
    bucket: dict[str, list] = defaultdict(list)
    for p in posts:
        if p["impressions"] == 0:
            continue
        label = classify_hook(p["text"])
        bucket[label].append(p)

    result = []
    for label, items in sorted(bucket.items(), key=lambda x: -sum(i["impressions"] for i in x[1])):
        avg_imp  = round(sum(i["impressions"] for i in items) / len(items))
        avg_ctr  = round(sum(i["ctr"]         for i in items) / len(items), 4)
        avg_url  = round(sum(i["url_clicks"]  for i in items) / len(items), 1)
        examples = sorted(items, key=lambda x: -x["impressions"])[:2]
        result.append({
            "hook_type":    label,
            "count":        len(items),
            "avg_imp":      avg_imp,
            "avg_ctr":      avg_ctr,
            "avg_url_clicks": avg_url,
            "examples":     [{"text": e["text"][:50], "impressions": e["impressions"], "url_clicks": e["url_clicks"]} for e in examples],
        })
    return result


# ---------------------------------------------------------------------------
# ハッシュタグ分析
# ---------------------------------------------------------------------------

def extract_hashtags(text: str) -> frozenset[str]:
    return frozenset(re.findall(r"#\S+", text))

def analyze_hashtags(posts: list[dict]) -> list[dict]:
    bucket: dict[frozenset, list] = defaultdict(list)
    for p in posts:
        if p["impressions"] == 0:
            continue
        tags = extract_hashtags(p["text"])
        if not tags:
            tags = frozenset(["(タグなし)"])
        bucket[tags].append(p)

    result = []
    for tags, items in sorted(bucket.items(), key=lambda x: -sum(i["url_clicks"] for i in x[1])):
        total_url  = sum(i["url_clicks"]  for i in items)
        max_url    = max(i["url_clicks"]  for i in items)
        avg_url    = round(total_url / len(items), 1)
        avg_imp    = round(sum(i["impressions"] for i in items) / len(items))
        best_post  = max(items, key=lambda x: x["url_clicks"])
        result.append({
            "tags":           sorted(tags),
            "count":          len(items),
            "total_url_clicks": total_url,
            "max_url_clicks": max_url,
            "avg_url_clicks": avg_url,
            "avg_imp":        avg_imp,
            "best_example":   {"text": best_post["text"][:60], "url_clicks": best_post["url_clicks"], "impressions": best_post["impressions"]},
        })
    return result[:15]  # 上位15パターン


# ---------------------------------------------------------------------------
# 投稿フェーズ分類
# ---------------------------------------------------------------------------

PHASE_PATTERNS = [
    ("実行中・進行中", r"実行中|出陣中|犯罪実行"),
    ("開始前告知",    r"から！！|から！|^\d{1,2}時\d{2}分|始まる前"),
    ("開始直後",      r"が始まる|始まった|きた！|スタート"),
    ("結果・余韻",    r"成功|失敗|終わった|お疲れ"),
    ("イベント紹介",  r"登録しました|MultiViewに|マルチビューで"),
    ("サービス告知",  r"StreamerHub|個人開発|バグ|修正"),
]

def classify_phase(text: str) -> str:
    for label, pattern in PHASE_PATTERNS:
        if re.search(pattern, text):
            return label
    return "その他"

def analyze_phases(posts: list[dict]) -> list[dict]:
    bucket: dict[str, list] = defaultdict(list)
    for p in posts:
        if p["impressions"] == 0:
            continue
        label = classify_phase(p["text"])
        bucket[label].append(p)

    result = []
    for label, items in sorted(bucket.items(), key=lambda x: -sum(i["url_clicks"] for i in x[1])):
        avg_imp  = round(sum(i["impressions"] for i in items) / len(items))
        avg_url  = round(sum(i["url_clicks"]  for i in items) / len(items), 1)
        avg_ctr  = round(sum(i["ctr"]         for i in items) / len(items), 4)
        result.append({
            "phase":          label,
            "count":          len(items),
            "avg_imp":        avg_imp,
            "avg_url_clicks": avg_url,
            "avg_ctr":        avg_ctr,
        })
    return result


# ---------------------------------------------------------------------------
# エンゲージメント構造分類（クリック特化 vs 拡散特化）
# ---------------------------------------------------------------------------

def analyze_engagement_types(posts: list[dict]) -> dict:
    click_focused  = []
    viral_focused  = []
    balanced       = []
    low_performer  = []

    for p in posts:
        if p["impressions"] < 100:
            continue
        ctr   = p["ctr"]
        viral = p["viral_score"]
        if ctr >= 0.02 and viral < 0.005:
            click_focused.append(p)
        elif viral >= 0.005 and ctr < 0.02:
            viral_focused.append(p)
        elif ctr >= 0.02 and viral >= 0.005:
            balanced.append(p)
        else:
            low_performer.append(p)

    def summarize(items):
        if not items:
            return {"count": 0, "examples": []}
        top = sorted(items, key=lambda x: -x["url_clicks"])[:3]
        return {
            "count":    len(items),
            "avg_ctr":  round(sum(i["ctr"] for i in items) / len(items), 4),
            "avg_url_clicks": round(sum(i["url_clicks"] for i in items) / len(items), 1),
            "examples": [{"text": e["text"][:60], "url_clicks": e["url_clicks"], "ctr": e["ctr"]} for e in top],
        }

    return {
        "click_focused":  summarize(click_focused),
        "viral_focused":  summarize(viral_focused),
        "balanced":       summarize(balanced),
        "low_performer":  summarize(low_performer),
    }


# ---------------------------------------------------------------------------
# サマリー統計
# ---------------------------------------------------------------------------

def compute_summary(posts: list[dict], csv_count: int) -> dict:
    valid = [p for p in posts if p["impressions"] > 0]
    if not valid:
        return {}

    dates = sorted(p["date"] for p in valid)

    return {
        "csv_file_count":  csv_count,
        "total_posts":     len(valid),
        "date_oldest":     dates[0],
        "date_newest":     dates[-1],
        "total_impressions": sum(p["impressions"] for p in valid),
        "total_url_clicks": sum(p["url_clicks"] for p in valid),
        "avg_impressions": round(sum(p["impressions"] for p in valid) / len(valid)),
        "avg_url_clicks":  round(sum(p["url_clicks"] for p in valid) / len(valid), 1),
        "avg_ctr":         round(sum(p["ctr"] for p in valid) / len(valid), 4),
        "top_posts_by_imp": [
            {"text": p["text"][:60], "impressions": p["impressions"], "url_clicks": p["url_clicks"]}
            for p in sorted(valid, key=lambda x: -x["impressions"])[:5]
        ],
        "top_posts_by_url_clicks": [
            {"text": p["text"][:60], "impressions": p["impressions"], "url_clicks": p["url_clicks"], "ctr": p["ctr"]}
            for p in sorted(valid, key=lambda x: -x["url_clicks"])[:5]
        ],
    }


# ---------------------------------------------------------------------------
# URL Clicks 上位投稿リスト（top_posts セクション）
# ---------------------------------------------------------------------------

def build_top_posts(posts: list[dict], n: int = 10) -> list[dict]:
    valid = [p for p in posts if p["impressions"] > 0]
    top = sorted(valid, key=lambda x: -x["url_clicks"])[:n]
    return [
        {
            "rank":        i + 1,
            "date":        p["date"],
            "text":        p["text"][:80],
            "impressions": p["impressions"],
            "url_clicks":  p["url_clicks"],
            "ctr":         p["ctr"],
            "likes":       p["likes"],
            "reposts":     p["reposts"],
            "link":        p["link"],
        }
        for i, p in enumerate(top)
    ]


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="NEWTOWN Tweet Analytics")
    parser.add_argument("--csv-dir", default=None, help="CSVファイルのディレクトリ")
    parser.add_argument("--out",     default=None, help="出力JSONのパス")
    args = parser.parse_args()

    base = Path(__file__).parent.parent
    csv_dir = Path(args.csv_dir) if args.csv_dir else base / "data" / "tweet_analytics"
    out_path = Path(args.out) if args.out else base / "knowledge" / "analysis_output.json"

    print(f"[analyze.py] CSVディレクトリ: {csv_dir}")
    posts, csv_count = load_all_csvs(csv_dir)
    print(f"[analyze.py] 読み込んだCSVファイル数: {csv_count}件")
    print(f"[analyze.py] 読み込んだ投稿数: {len(posts)}")

    posts = add_derived_metrics(posts)

    summary = compute_summary(posts, csv_count)

    output = {
        "summary":          summary,
        "hooks":            analyze_hooks(posts),
        "hashtags":         analyze_hashtags(posts),
        "phases":           analyze_phases(posts),
        "engagement_types": analyze_engagement_types(posts),
        "top_posts":        build_top_posts(posts),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"[analyze.py] 出力完了: {out_path}")

    # サマリー出力
    valid_posts = [p for p in posts if p["impressions"] > 0]
    total_imp = sum(p["impressions"] for p in valid_posts)
    total_url = sum(p["url_clicks"] for p in valid_posts)
    avg_ctr_pct = round(summary.get("avg_ctr", 0) * 100, 2)

    print("")
    print("=== データ処理完了 ===")
    print(f"- 対象CSVファイル数: {csv_count}件")
    print(f"- 集計投稿数: {len(valid_posts)}件")
    print(f"- 分析対象期間: {summary.get('date_oldest', 'N/A')} 〜 {summary.get('date_newest', 'N/A')}")
    print(f"- 総インプレッション: {total_imp}")
    print(f"- 総URL Clicks: {total_url}")
    print(f"- 平均CTR: {avg_ctr_pct}%")
    print(f"- 出力ファイル: {out_path}")


if __name__ == "__main__":
    main()

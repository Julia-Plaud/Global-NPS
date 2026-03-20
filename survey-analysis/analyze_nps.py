import csv
from collections import Counter

def load_data(filepath):
    rows = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['NPS_Score'] = int(row['NPS_Score'])
            rows.append(row)
    return rows

def calculate_nps(rows):
    categories = Counter(r['Promoter_Category'] for r in rows)
    total = len(rows)
    promoters = categories.get('Promoter', 0)
    detractors = categories.get('Detractor', 0)
    nps = round((promoters / total - detractors / total) * 100, 1)
    return nps, categories, total

def summarize(filepath):
    rows = load_data(filepath)
    nps, categories, total = calculate_nps(rows)
    avg_score = round(sum(r['NPS_Score'] for r in rows) / total, 2)

    print(f"=== NPS Analysis: Global NPS_US ===")
    print(f"Total Responses : {total}")
    print(f"Average Score   : {avg_score}")
    print()
    print(f"Breakdown:")
    for cat in ['Promoter', 'Passive', 'Detractor']:
        count = categories.get(cat, 0)
        pct = round(count / total * 100, 1)
        print(f"  {cat:<12} {count:>3}  ({pct}%)")
    print()
    print(f"Net Promoter Score (NPS): {nps}")
    print()
    print("Comments by Category:")
    for cat in ['Promoter', 'Passive', 'Detractor']:
        print(f"\n  [{cat}]")
        for r in rows:
            if r['Promoter_Category'] == cat:
                print(f"    - Score {r['NPS_Score']}: {r['Comments']}")

if __name__ == '__main__':
    summarize('Global NPS_US.csv')

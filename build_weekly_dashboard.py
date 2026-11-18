# -*- coding: utf-8 -*-
import csv
import json
import urllib.request
import urllib.parse
from datetime import datetime
from collections import defaultdict

print("=== CALCULATING FULL WEEKLY SALES DATA (CỘT H: NGÀY CT) ===")

CSV_PATH = "/Users/ted/.gemini/antigravity/brain/e06597ef-f9a6-44b5-9b0d-ed1d09053a79/scratch/don_hang_t11_latest.csv"

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    rows = list(csv.reader(f))[6:]

def parse_money(s):
    if not s: return 0.0
    s = s.replace('.', '').replace(',', '.')
    try: return float(s)
    except: return 0.0

def parse_date(s):
    if not s: return None
    s = s.strip()
    for fmt in ('%d/%m/%Y', '%Y-%m-%d'):
        try: return datetime.strptime(s, fmt).date()
        except: pass
    return None

def get_week_key(d):
    if not d: return 'other'
    day = d.day
    if 1 <= day <= 8: return 'w1'
    elif 9 <= day <= 15: return 'w2'
    elif 16 <= day <= 22: return 'w3'
    elif 23 <= day <= 31: return 'w4'
    return 'other'

periods = ['all', 'w1', 'w2', 'w3', 'w4']

sales_periods = {p: {
    'total_rev': 0.0,
    'sos': set(),
    'rows': 0,
    'brands': {
        'THE CITY': 0.0,
        'THE MIA': 0.0,
        'RPB EDU & PUBLIC': 0.0,
        'Phí vận chuyển / Khác': 0.0
    },
    'regions': {'HCM': 0.0, 'HN': 0.0},
    'reps': {
        'HCMKDANH.05': {'rev': 0.0, 'sos': set(), 'name': 'Nguyễn Quỳnh Anh', 'reg': 'HCM'},
        'HCMKDKHOA.02': {'rev': 0.0, 'sos': set(), 'name': 'Lê Minh Khoa', 'reg': 'HCM'},
        'HNIKDDAO.01': {'rev': 0.0, 'sos': set(), 'name': 'Vũ Thị Đào', 'reg': 'HN'},
        'HNIKDMINH.02': {'rev': 0.0, 'sos': set(), 'name': 'Nguyễn Đức Minh', 'reg': 'HN'},
        'HNIKDYEN.01': {'rev': 0.0, 'sos': set(), 'name': 'Vũ Hoàng Yến', 'reg': 'HN'}
    },
    'rep_brand': defaultdict(lambda: defaultdict(float))
} for p in periods}

for r in rows:
    if len(r) <= 24: continue
    rep = r[17].strip()
    brand_raw = r[20].strip()
    source = r[21].strip()
    so = r[1]
    ngay_ct_str = r[7]
    tien = parse_money(r[16])
    
    is_mkt = False
    if rep in ['HCMKDANH.05', 'HCMKDKHOA.02']:
        is_mkt = True
    elif rep in ['HNIKDDAO.01', 'HNIKDMINH.02', 'HNIKDYEN.01']:
        if any(k in source.upper() for k in ['MKT', 'ONLINE']):
            is_mkt = True
        elif rep == 'HNIKDYEN.01' and 'EDU' in brand_raw.upper():
            is_mkt = True
            
    if not is_mkt:
        continue
        
    d = parse_date(ngay_ct_str)
    w_key = get_week_key(d)
    
    if 'CITY' in brand_raw.upper():
        brand = 'THE CITY'
    elif 'MIA' in brand_raw.upper():
        brand = 'THE MIA'
    elif 'EDU' in brand_raw.upper():
        brand = 'RPB EDU & PUBLIC'
    else:
        brand = 'Phí vận chuyển / Khác'
        
    region = 'HCM' if rep in ['HCMKDANH.05', 'HCMKDKHOA.02'] else 'HN'
    
    targets = ['all']
    if w_key in periods:
        targets.append(w_key)
        
    for k in targets:
        sp = sales_periods[k]
        sp['total_rev'] += tien
        sp['sos'].add(so)
        sp['rows'] += 1
        sp['brands'][brand] += tien
        sp['regions'][region] += tien
        if rep in sp['reps']:
            sp['reps'][rep]['rev'] += tien
            sp['reps'][rep]['sos'].add(so)
        sp['rep_brand'][rep][brand] += tien

# Clean sets for JSON serialization
clean_sales = {}
for p, val in sales_periods.items():
    clean_sales[p] = {
        'total_rev': val['total_rev'],
        'so_count': len(val['sos']),
        'rows_count': val['rows'],
        'brands': val['brands'],
        'regions': val['regions'],
        'reps': {r: {'rev': d['rev'], 'sos': len(d['sos']), 'name': d['name'], 'reg': d['reg']} for r, d in val['reps'].items()},
        'rep_brand': {r: dict(b) for r, b in val['rep_brand'].items()}
    }

print("Sales data computed successfully for all periods.")
for p in periods:
    print(f"{p}: Rev = {clean_sales[p]['total_rev']:,.0f} đ ({clean_sales[p]['so_count']} SOs)")

# Facebook Ads by period
fb_data = {
    "all": {
        "spend": 30142107.0,
        "conv": 644,
        "brands": {"THE CITY": 5861932.0, "THE MIA": 9133852.0, "RPB EDU & PUBLIC": 15049054.0, "Khác": 97269.0},
        "conv_brand": {"THE CITY": 103, "THE MIA": 104, "RPB EDU & PUBLIC": 436, "Khác": 1}
    },
    "w1": {
        "spend": 15137880.0,
        "conv": 355,
        "brands": {"THE CITY": 3114778.0, "THE MIA": 4576789.0, "RPB EDU & PUBLIC": 7446313.0, "Khác": 0.0},
        "conv_brand": {"THE CITY": 65, "THE MIA": 52, "RPB EDU & PUBLIC": 238, "Khác": 0}
    },
    "w2": {
        "spend": 10677849.0,
        "conv": 210,
        "brands": {"THE CITY": 1991355.0, "THE MIA": 3245942.0, "RPB EDU & PUBLIC": 5440552.0, "Khác": 0.0},
        "conv_brand": {"THE CITY": 31, "THE MIA": 33, "RPB EDU & PUBLIC": 146, "Khác": 0}
    },
    "w3": {
        "spend": 4326378.0,
        "conv": 79,
        "brands": {"THE CITY": 755799.0, "THE MIA": 1311121.0, "RPB EDU & PUBLIC": 2162189.0, "Khác": 97269.0},
        "conv_brand": {"THE CITY": 7, "THE MIA": 19, "RPB EDU & PUBLIC": 52, "Khác": 1}
    },
    "w4": {
        "spend": 0.0,
        "conv": 0,
        "brands": {"THE CITY": 0.0, "THE MIA": 0.0, "RPB EDU & PUBLIC": 0.0, "Khác": 0.0},
        "conv_brand": {"THE CITY": 0, "THE MIA": 0, "RPB EDU & PUBLIC": 0, "Khác": 0}
    }
}

# Google Ads by period (Total 18 days: 59,207,862 đ, 1,787.29 conv)
gg_data = {
    "all": {
        "spend": 59207862.0,
        "conv": 1787,
        "brands": {"THE CITY": 47659730.0, "THE MIA": 11548132.0, "RPB EDU & PUBLIC": 0.0}
    },
    "w1": { # 8 days (01-08) -> 8/18
        "spend": 26314605.0,
        "conv": 794,
        "brands": {"THE CITY": 21182102.0, "THE MIA": 5132503.0, "RPB EDU & PUBLIC": 0.0}
    },
    "w2": { # 7 days (09-15) -> 7/18
        "spend": 23025280.0,
        "conv": 695,
        "brands": {"THE CITY": 18534340.0, "THE MIA": 4490940.0, "RPB EDU & PUBLIC": 0.0}
    },
    "w3": { # 3 days (16-18) -> 3/18
        "spend": 9867977.0,
        "conv": 298,
        "brands": {"THE CITY": 7943288.0, "THE MIA": 1924689.0, "RPB EDU & PUBLIC": 0.0}
    },
    "w4": {
        "spend": 0.0,
        "conv": 0,
        "brands": {"THE CITY": 0.0, "THE MIA": 0.0, "RPB EDU & PUBLIC": 0.0}
    }
}

# Combine all into weekly data dictionary
combined_weekly = {}
for p in periods:
    s_rev = clean_sales[p]['total_rev']
    fb_sp = fb_data[p]['spend']
    gg_sp = gg_data[p]['spend']
    tot_ads = fb_sp + gg_sp
    cir = (tot_ads / s_rev * 100) if s_rev > 0 else 0.0
    roas = (s_rev / tot_ads) if tot_ads > 0 else 0.0
    tot_leads = fb_data[p]['conv'] + gg_data[p]['conv']
    
    # KPI Target based on period
    if p == 'all':
        kpi_target = 3250000000.0 # 1 tháng
        kpi_days = 18
    elif p == 'w1':
        kpi_target = (3250000000.0 / 30) * 8 # 866.67M
        kpi_days = 8
    elif p == 'w2':
        kpi_target = (3250000000.0 / 30) * 7 # 758.33M
        kpi_days = 7
    elif p == 'w3':
        kpi_target = (3250000000.0 / 30) * 7 # 758.33M
        kpi_days = 3 # 16-18
    elif p == 'w4':
        kpi_target = (3250000000.0 / 30) * 8 # 866.67M
        kpi_days = 0

    progress = (s_rev / kpi_target * 100) if kpi_target > 0 else 0.0

    combined_weekly[p] = {
        'revenue': s_rev,
        'kpi_target': kpi_target,
        'progress': progress,
        'ads_spend': tot_ads,
        'fb_spend': fb_sp,
        'gg_spend': gg_sp,
        'cir': cir,
        'roas': roas,
        'leads': tot_leads,
        'fb_leads': fb_data[p]['conv'],
        'gg_leads': gg_data[p]['conv'],
        'sales_detail': clean_sales[p],
        'fb_detail': fb_data[p],
        'gg_detail': gg_data[p]
    }

with open('/Users/ted/Desktop/Code/RPB/weekly_data.json', 'w', encoding='utf-8') as f:
    json.dump(combined_weekly, f, ensure_ascii=False, indent=2)

print("Weekly bundle written to /Users/ted/Desktop/Code/RPB/weekly_data.json")

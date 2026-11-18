import json

# 1. Load current dashboard_data.json
with open("/Users/ted/Desktop/Code/RPB/dashboard_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Add Google Ads Data
google_the_city = {
    "account_name": "Nguyễn Thành Long",
    "account_id": "563-582-4813",
    "brand": "THE CITY",
    "total_spend": 47659730,
    "total_clicks": 55990,
    "total_impressions": 464459,
    "total_conversions": 1604.29,
    "avg_ctr": 12.05,
    "avg_cpa": 29708,
    "campaigns": [
        {"name": "The City-Ghế VP-Search-Miền Nam-10122025", "type": "Tìm kiếm", "spend": 11426246, "clicks": 830, "impressions": 57906, "conversions": 14.21, "ctr": 1.43, "cpa": 804051},
        {"name": "The City -Bàn VP-Search-Miền Bắc-10122025", "type": "Tìm kiếm", "spend": 9235920, "clicks": 197, "impressions": 1019, "conversions": 15.00, "ctr": 19.33, "cpa": 615728},
        {"name": "The CiTy_Remarketing_90D_9/2026", "type": "Hiển thị", "spend": 9003450, "clicks": 24330, "impressions": 158598, "conversions": 740.78, "ctr": 15.34, "cpa": 12154},
        {"name": "The City-Ghế VP-Search-Miền Bắc-10122025", "type": "Tìm kiếm", "spend": 7452985, "clicks": 232, "impressions": 2826, "conversions": 12.50, "ctr": 8.21, "cpa": 596239},
        {"name": "TheCity-hiển thị miền bắc -26/08/26 #2", "type": "Performance Max", "spend": 4959114, "clicks": 28547, "impressions": 226706, "conversions": 722.01, "ctr": 12.59, "cpa": 6869},
        {"name": "The City-Search-Brand City-Miền Nam-10122025", "type": "Tìm kiếm", "spend": 2419345, "clicks": 475, "impressions": 6336, "conversions": 15.00, "ctr": 7.50, "cpa": 161275},
        {"name": "The City -Search-Nội thất phòng giám đốc-phòng họp", "type": "Tìm kiếm", "spend": 2317137, "clicks": 1162, "impressions": 10279, "conversions": 80.79, "ctr": 11.30, "cpa": 28682},
        {"name": "The City - Search-Brand City-Miền Bắc-10122025", "type": "Tìm kiếm", "spend": 845533, "clicks": 217, "impressions": 2289, "conversions": 4.00, "ctr": 9.48, "cpa": 211383}
    ]
}

google_the_mia = {
    "account_name": "The Mia",
    "account_id": "958-066-7486",
    "brand": "THE MIA",
    "total_spend": 11548132,
    "total_clicks": 785,
    "total_impressions": 10918,
    "total_conversions": 183.00,
    "avg_ctr": 7.19,
    "avg_cpa": 63105,
    "campaigns": [
        {"name": "The Mia - Ghế Văn Phòng - Tìm kiếm - 2.11", "type": "Tìm kiếm", "spend": 5943669, "clicks": 391, "impressions": 6585, "conversions": 91.50, "ctr": 5.94, "cpa": 64958},
        {"name": "Search - Brand Mia - Miền Nam-10122025", "type": "Tìm kiếm", "spend": 2918440, "clicks": 273, "impressions": 2433, "conversions": 6.50, "ctr": 11.22, "cpa": 448991},
        {"name": "The Mia -Bàn VP-Search-Miền Bắc-10122025", "type": "Tìm kiếm", "spend": 1477020, "clicks": 34, "impressions": 884, "conversions": 45.00, "ctr": 3.85, "cpa": 32823},
        {"name": "The Mia-Ghế VP-Search-Miền Bắc-10122025", "type": "Tìm kiếm", "spend": 873048, "clicks": 22, "impressions": 710, "conversions": 29.00, "ctr": 3.10, "cpa": 30105},
        {"name": "Search - Brand Mia - Miền Bắc-10122025", "type": "Tìm kiếm", "spend": 335955, "clicks": 65, "impressions": 306, "conversions": 11.00, "ctr": 21.24, "cpa": 30541}
    ]
}

data["google_ads"] = {
    "total_spend": google_the_city["total_spend"] + google_the_mia["total_spend"],
    "total_clicks": google_the_city["total_clicks"] + google_the_mia["total_clicks"],
    "total_impressions": google_the_city["total_impressions"] + google_the_mia["total_impressions"],
    "total_conversions": google_the_city["total_conversions"] + google_the_mia["total_conversions"],
    "the_city": google_the_city,
    "the_mia": google_the_mia
}

# 3. Combined Total Spend (FB + GG)
total_ads_spend = data["fb_ads"]["total_spend"] + data["google_ads"]["total_spend"]
data["combined_ads"] = {
    "total_spend": total_ads_spend,
    "fb_spend": data["fb_ads"]["total_spend"],
    "gg_spend": data["google_ads"]["total_spend"],
    "cir_standard": (total_ads_spend / data["sales"]["total_mkt_standard"]) * 100,
    "cir_expanded": (total_ads_spend / data["sales"]["total_mkt_expanded"]) * 100,
    "roas_standard": data["sales"]["total_mkt_standard"] / total_ads_spend,
    "roas_expanded": data["sales"]["total_mkt_expanded"] / total_ads_spend,
    "by_brand": {
        "THE CITY": {
            "fb": 5840661,
            "gg": 47659730,
            "total_spend": 5840661 + 47659730,
            "revenue": 1019997830,
            "cir": ((5840661 + 47659730) / 1019997830) * 100
        },
        "THE MIA": {
            "fb": 9088260,
            "gg": 11548132,
            "total_spend": 9088260 + 11548132,
            "revenue": 333227800,
            "cir": ((9088260 + 11548132) / 333227800) * 100
        },
        "RPB EDU & PUBLIC": {
            "fb": 14962619,
            "gg": 0,
            "total_spend": 14962619,
            "revenue": 9796055,
            "revenue_expanded": 97344955,
            "cir": (14962619 / 9796055) * 100
        }
    }
}

# Save updated data.json
with open("/Users/ted/Desktop/Code/RPB/dashboard_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated dashboard_data.json with Google Ads successfully!")
print(f"Total Combined Spend: {total_ads_spend:,.0f} VND (FB: {data['fb_ads']['total_spend']:,.0f} | GG: {data['google_ads']['total_spend']:,.0f})")
print(f"Combined CIR: {data['combined_ads']['cir_standard']:.2f}% (expanded: {data['combined_ads']['cir_expanded']:.2f}%)")

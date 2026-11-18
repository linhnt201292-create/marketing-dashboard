import urllib.request
import urllib.parse
import json
import csv
import os
from datetime import datetime
from collections import defaultdict, Counter

print("Starting dashboard data generation...")

# 1. Fetch Facebook Ads
FB_ACCESS_TOKEN = "EAAQSjFaeEA0BTKGgaEfyacviQYCglXjpKKRG1Wk0zBVdnKwXiPNQszpDkrHic1Tls6tCVZA2u4eeNvxI0DsUTpZAFM5I3OAeJ8hrTvp6CJs9quxKTZCUyvqByYXjk7dfWGhah5XG3FVnmJmptZAemObcAtZCShTAzBOqJMhgh7CZBNmM1oQj1IVAvoHqlpnybLpAZDZD"
AD_ACCOUNT_ID = "act_1113055687224460"
time_range = json.dumps({"since": "2026-11-01", "until": "2026-11-18"})

fb_campaigns = []
fb_total_spend = 0
fb_total_msgs = 0
fb_total_leads = 0
fb_total_impressions = 0
fb_total_clicks = 0

try:
    url = (
        f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/insights"
        f"?level=campaign"
        f"&time_range={urllib.parse.quote(time_range)}"
        f"&fields=campaign_id,campaign_name,spend,impressions,clicks,cpc,cpm,ctr,actions"
        f"&limit=100"
        f"&access_token={FB_ACCESS_TOKEN}"
    )
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
    data = res.get("data", [])
    for item in data:
        spend = float(item.get("spend", 0))
        impressions = int(item.get("impressions", 0))
        clicks = int(item.get("clicks", 0))
        ctr = float(item.get("ctr", 0))
        actions = {a.get("action_type"): int(a.get("value", 0)) for a in item.get("actions", [])}
        msgs = actions.get("onsite_conversion.messaging_conversation_started_7d", 0)
        leads = actions.get("lead", 0)
        cname = item.get("campaign_name")
        
        # Determine brand
        cname_upper = cname.upper()
        if any(k in cname_upper for k in ["EDU", "ROOKY", "MOTO", "SMART ZICO", "TITAN"]):
            brand = "RPB EDU & PUBLIC"
        elif any(k in cname_upper for k in ["THE MIA", "THEMIA"]):
            brand = "THE MIA"
        elif any(k in cname_upper for k in ["THECITY", "THE CITY"]):
            brand = "THE CITY"
        else:
            brand = "KHÁC / CHUNG"
            
        total_conv = msgs + leads
        cost_per_conv = (spend / total_conv) if total_conv > 0 else spend
        
        fb_campaigns.append({
            "name": cname,
            "brand": brand,
            "spend": spend,
            "impressions": impressions,
            "clicks": clicks,
            "ctr": ctr,
            "msgs": msgs,
            "leads": leads,
            "total_conv": total_conv,
            "cost_per_conv": cost_per_conv
        })
        fb_total_spend += spend
        fb_total_msgs += msgs
        fb_total_leads += leads
        fb_total_impressions += impressions
        fb_total_clicks += clicks

    print(f"Loaded {len(fb_campaigns)} FB campaigns. Spend: {fb_total_spend:,.0f} VND")
except Exception as e:
    print("Error fetching FB Ads:", e)

# 2. Fetch AI Seller Chatbot
AISELLER_URL = "https://chatbot.sales.ai.vn/api/mcp"
AISELLER_TOKEN = "aat_110b15afb5a529f2bcc148bc1215994e7b4170da45e496f1e3ba0e6db7efb68a"

chatbot_stats = {
    "total_convs": 0,
    "phone_count": 0,
    "order_label_count": 0,
    "platforms": Counter(),
    "platform_phones": Counter()
}

try:
    def call_aiseller(name, args):
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": name, "arguments": args}
        }).encode("utf-8")
        req = urllib.request.Request(AISELLER_URL, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AISELLER_TOKEN}"
        })
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
        content = res["result"]["content"][0]["text"]
        return json.loads(content)

    all_convs = []
    offset = 0
    while True:
        res = call_aiseller("aiseller_list_conversations", {
            "chatbotId": 14,
            "from": "2026-11-01",
            "to": "2026-11-18",
            "limit": 200,
            "offset": offset
        })
        convs = res.get("conversations", [])
        if not convs:
            break
        all_convs.extend(convs)
        if len(convs) < 200:
            break
        offset += 200

    chatbot_stats["total_convs"] = len(all_convs)
    for c in all_convs:
        pname = c.get("platformName") or c.get("platformType")
        chatbot_stats["platforms"][pname] += 1
        if c.get("customerPhone"):
            chatbot_stats["phone_count"] += 1
            chatbot_stats["platform_phones"][pname] += 1
        for lb in c.get("labels", []):
            if "đơn hàng" in lb.get("name", "").lower():
                chatbot_stats["order_label_count"] += 1

    print(f"Loaded {chatbot_stats['total_convs']} chatbot conversations, {chatbot_stats['phone_count']} phones.")
except Exception as e:
    print("Error fetching AI Seller:", e)

# 3. Read Google Sheets SO Sales
csv_path = "/Users/ted/.gemini/antigravity/brain/e06597ef-f9a6-44b5-9b0d-ed1d09053a79/scratch/don_hang_t11.csv"
sales_data = {
    "hcm_anh": {"city": 817516000, "mia": 225009000, "edu": 0, "fee": 26163390, "total": 1068688390, "sos": 38, "rows": 100},
    "hcm_khoa": {"city": 164219830, "mia": 101599000, "edu": 9796055, "fee": 8051921, "total": 283666806, "sos": 30, "rows": 63},
    "hn_dao": {"city": 38262000, "mia": 0, "edu": 0, "fee": 0, "total": 38262000, "sos": 1, "rows": 6},
    "hn_minh": {"city": 0, "mia": 6619800, "edu": 0, "fee": 0, "total": 6619800, "sos": 1, "rows": 1},
    "hn_yen": {"city": 0, "mia": 0, "edu": 87548900, "fee": 0, "total": 87548900, "sos": 5, "rows": 10}
}

sales_summary = {
    "total_mkt_standard": 1397236996,
    "total_mkt_expanded": 1484785896,
    "by_brand_standard": {
        "THE CITY": 1019997830,
        "THE MIA": 333227800,
        "RPB EDU & PUBLIC": 9796055,
        "Phí vận chuyển / Khác": 34215311
    },
    "by_brand_expanded": {
        "THE CITY": 1019997830,
        "THE MIA": 333227800,
        "RPB EDU & PUBLIC": 97344955,
        "Phí vận chuyển / Khác": 34215311
    },
    "by_region": {
        "HCM": 1352355196,
        "HN_standard": 44881800,
        "HN_expanded": 132430700
    }
}

# 4. Generate JSON bundle
export_data = {
    "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    "date_range": "01/11/2026 - 18/11/2026",
    "kpi_year": {
        "revenue_target": 39000000000,
        "ads_budget_5pct": 1950000000,
        "quote_target": 117000000000,
        "brands": {
            "THE CITY": {"share": 0.61, "rev": 23790000000, "budget": 1189500000},
            "THE MIA": {"share": 0.25, "rev": 9750000000, "budget": 487500000},
            "RPB EDU & PUBLIC": {"share": 0.14, "rev": 5460000000, "budget": 273000000}
        }
    },
    "fb_ads": {
        "total_spend": fb_total_spend,
        "total_msgs": fb_total_msgs,
        "total_leads": fb_total_leads,
        "total_conv": fb_total_msgs + fb_total_leads,
        "avg_cpa": fb_total_spend / (fb_total_msgs + fb_total_leads) if (fb_total_msgs + fb_total_leads) > 0 else 0,
        "campaigns": fb_campaigns
    },
    "chatbot": {
        "total_convs": chatbot_stats["total_convs"],
        "phones": chatbot_stats["phone_count"],
        "orders_tagged": chatbot_stats["order_label_count"],
        "platforms": dict(chatbot_stats["platforms"]),
        "platform_phones": dict(chatbot_stats["platform_phones"])
    },
    "sales": sales_summary,
    "sales_reps": sales_data
}

# Save data.json
with open("/Users/ted/Desktop/Code/RPB/dashboard_data.json", "w", encoding="utf-8") as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print("Data exported to /Users/ted/Desktop/Code/RPB/dashboard_data.json")

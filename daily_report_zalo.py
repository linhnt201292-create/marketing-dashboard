#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daily_report_zalo.py
Tự động lấy báo cáo Facebook Ads ngày hôm qua và gửi thông báo vào nhóm Zalo mỗi sáng.
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime

# ==============================================================================
# CẤU HÌNH THÔNG TIN KẾT NỐI
# ==============================================================================

# 1. Thông tin Facebook Ads (Đã cấu hình sẵn tài khoản RPB HCM của bạn)
FB_ACCESS_TOKEN = "EAAQSjFaeEA0BTKGgaEfyacviQYCglXjpKKRG1Wk0zBVdnKwXiPNQszpDkrHic1Tls6tCVZA2u4eeNvxI0DsUTpZAFM5I3OAeJ8hrTvp6CJs9quxKTZCUyvqByYXjk7dfWGhah5XG3FVnmJmptZAemObcAtZCShTAzBOqJMhgh7CZBNmM1oQj1IVAvoHqlpnybLpAZDZD"
AD_ACCOUNT_ID = "act_1113055687224460"  # RPB ADs account HCM

# 2. Cấu hình gửi Zalo
# Cách phổ biến nhất: Dùng Webhook URL của Zalo Bot trong nhóm
# (Nếu nhóm Zalo của bạn có webhook bot, dán URL webhook vào đây)
ZALO_WEBHOOK_URL = "YOUR_ZALO_WEBHOOK_URL_HERE"


# ==============================================================================
# HÀM LẤY SỐ LIỆU TỪ FACEBOOK ADS
# ==============================================================================
def get_fb_yesterday_insights():
    url = (
        f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/insights"
        f"?level=campaign"
        f"&date_preset=yesterday"
        f"&fields=campaign_id,campaign_name,spend,impressions,clicks,cpc,cpm,ctr,actions,cost_per_action_type"
        f"&limit=100"
        f"&access_token={FB_ACCESS_TOKEN}"
    )

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
    
    data = res.get("data", [])
    
    total_spend = 0
    total_msgs = 0
    total_clicks = 0
    total_impressions = 0
    campaign_list = []

    for item in data:
        spend = float(item.get("spend", 0))
        impressions = int(item.get("impressions", 0))
        clicks = int(item.get("clicks", 0))
        ctr = float(item.get("ctr", 0))
        
        actions = {a.get("action_type"): int(a.get("value", 0)) for a in item.get("actions", [])}
        cost_per_action = {c.get("action_type"): float(c.get("value", 0)) for c in item.get("cost_per_action_type", [])}
        
        msgs = actions.get("onsite_conversion.messaging_conversation_started_7d", 0)
        cost_per_msg = cost_per_action.get("onsite_conversion.messaging_conversation_started_7d", 0)

        total_spend += spend
        total_msgs += msgs
        total_clicks += clicks
        total_impressions += impressions

        campaign_list.append({
            "name": item.get("campaign_name"),
            "spend": spend,
            "msgs": msgs,
            "cost_per_msg": cost_per_msg,
            "ctr": ctr
        })

    avg_cost_per_msg = (total_spend / total_msgs) if total_msgs > 0 else 0
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0

    return {
        "total_spend": total_spend,
        "total_msgs": total_msgs,
        "avg_cost_per_msg": avg_cost_per_msg,
        "total_clicks": total_clicks,
        "avg_ctr": avg_ctr,
        "campaigns": campaign_list
    }


# ==============================================================================
# HÀM SOẠN NỘI DUNG BÁO CÁO
# ==============================================================================
def build_report_message(stats):
    today_str = datetime.now().strftime("%d/%m/%Y")
    
    # Lọc top camp hiệu quả (có mess, giá mess tốt nhất)
    good_camps = [c for c in stats["campaigns"] if c["msgs"] > 0]
    good_camps.sort(key=lambda x: x["cost_per_msg"])
    
    # Lọc camp cần lưu ý (tiêu trên 50k mà chưa có mess, hoặc giá mess > 100k)
    warning_camps = [c for c in stats["campaigns"] if (c["spend"] > 50000 and c["msgs"] == 0) or c["cost_per_msg"] > 100000]
    warning_camps.sort(key=lambda x: x["spend"], reverse=True)

    msg = f"📊 BÁO CÁO FACEBOOK ADS HÔM QUA (Ngày {today_str})\n"
    msg += f"🏢 Tài khoản: RPB ADs account HCM\n"
    msg += f"------------------------------------\n"
    msg += f"💰 Tổng chi tiêu: {stats['total_spend']:,.0f} đ\n"
    msg += f"💬 Tổng tin nhắn: {stats['total_msgs']} mess\n"
    msg += f"🎯 Giá TB / Mess: {stats['avg_cost_per_msg']:,.0f} đ/mess\n"
    msg += f"🖱 Lượt Click: {stats['total_clicks']} (CTR: {stats['avg_ctr']:.2f}%)\n"
    msg += f"------------------------------------\n"
    
    msg += "🌟 TOP CHIẾN DỊCH HIỆU QUẢ:\n"
    if good_camps:
        for c in good_camps[:3]:
            msg += f"  • {c['name'][:30]}...\n    👉 {c['msgs']} mess | {c['cost_per_msg']:,.0f} đ/mess (Chi: {c['spend']:,.0f} đ)\n"
    else:
        msg += "  (Hôm qua chưa có tin nhắn phát sinh)\n"

    if warning_camps:
        msg += "\n⚠️ CẦN CHÚ Ý (ĐẮT / CHƯA RA MESS):\n"
        for c in warning_camps[:3]:
            if c["msgs"] == 0:
                msg += f"  • {c['name'][:30]}...\n    👉 Tiêu {c['spend']:,.0f} đ (0 mess)\n"
            else:
                msg += f"  • {c['name'][:30]}...\n    👉 Giá cao: {c['cost_per_msg']:,.0f} đ/mess (Tiêu {c['spend']:,.0f} đ)\n"
    
    return msg


# ==============================================================================
# HÀM GỬI TIN NHẮN ĐẾN ZALO
# ==============================================================================
def send_to_zalo(message_text):
    if not ZALO_WEBHOOK_URL or "YOUR_ZALO_WEBHOOK_URL" in ZALO_WEBHOOK_URL:
        print("[!] Chưa cấu hình ZALO_WEBHOOK_URL. Nội dung tin nhắn mẫu:")
        print("="*50)
        print(message_text)
        print("="*50)
        return False

    payload = json.dumps({"text": message_text}).encode("utf-8")
    req = urllib.request.Request(
        ZALO_WEBHOOK_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print("[+] Đã gửi báo cáo thành công vào Zalo! Status:", resp.status)
            return True
    except Exception as e:
        print("[-] Lỗi khi gửi đến Zalo Webhook:", e)
        return False


if __name__ == "__main__":
    print("[*] Đang lấy dữ liệu hôm qua từ Facebook Ads...")
    stats = get_fb_yesterday_insights()
    report = build_report_message(stats)
    send_to_zalo(report)

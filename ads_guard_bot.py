#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ads_guard_bot.py
Trợ lý giám sát, cảnh báo & báo cáo Facebook Ads qua Telegram:
1. Tự động gửi báo cáo ngày hôm qua vào 08:00 sáng mỗi ngày (chạy ngầm độc lập, không phụ thuộc cron của macOS)
2. Nhận lệnh tương tác 24/7:
   - /today hoặc /bc: Số liệu hôm nay
   - /7day hoặc /tuan: Báo cáo tổng kết 7 ngày qua & Top camp tốt nhất
   - /30day hoặc /thang: Báo cáo tổng kết 30 ngày qua & Top camp tốt nhất
3. Cảnh báo khẩn cấp mỗi 1 tiếng: Lỗi thẻ, khóa tài khoản, camp cắn tiền lố >150k chưa có mess
4. Bắn data khách hàng mới (Họ tên, SĐT, Nhu cầu) từ Lead Form vào Telegram ngay lập tức
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime

# ==============================================================================
# CẤU HÌNH THÔNG TIN
# ==============================================================================
FB_ACCESS_TOKEN = "EAAQSjFaeEA0BTKGgaEfyacviQYCglXjpKKRG1Wk0zBVdnKwXiPNQszpDkrHic1Tls6tCVZA2u4eeNvxI0DsUTpZAFM5I3OAeJ8hrTvp6CJs9quxKTZCUyvqByYXjk7dfWGhah5XG3FVnmJmptZAemObcAtZCShTAzBOqJMhgh7CZBNmM1oQj1IVAvoHqlpnybLpAZDZD"
AD_ACCOUNT_ID = "act_1113055687224460"

TELEGRAM_BOT_TOKEN = "9247946542:AAH9C_6bRd-48PQzy2YX1Xs1a3gRRZirTjI"
TELEGRAM_CHAT_ID = "-5547572529"  # Nhóm "Báo cáo Ads RPB"

SEEN_LEADS_FILE = "/Users/ted/Desktop/Code/RPB/seen_leads.json"

ACCOUNT_STATUS_MAP = {
    1: "HOẠT ĐỘNG BÌNH THƯỜNG",
    2: "BỊ VÔ HIỆU HÓA / KHÓA",
    3: "LỖI THANH TOÁN (HẾT TIỀN / LỖI THẺ VISA)",
    7: "ĐANG XÉT DUYỆT RỦI RO",
    8: "CHỜ THANH TOÁN QUYẾT TOÁN",
    9: "TRONG GIAI ĐOẠN ÂN HẠN",
    100: "CHỜ ĐÓNG TÀI KHOẢN",
    101: "ĐÃ ĐÓNG TÀI KHOẢN"
}

alerted_campaigns_today = set()
last_hourly_check = 0
last_lead_check = 0
last_daily_report_date = None


# ==============================================================================
# QUẢN LÝ DANH SÁCH LEAD ĐÃ XỬ LÝ
# ==============================================================================
def load_seen_leads():
    if os.path.exists(SEEN_LEADS_FILE):
        try:
            with open(SEEN_LEADS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_seen_leads(seen_set):
    try:
        with open(SEEN_LEADS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(seen_set), f, ensure_ascii=False)
    except Exception as e:
        print("[-] Lỗi lưu file seen_leads:", e)

seen_leads = load_seen_leads()


# ==============================================================================
# TELEGRAM API HELPERS
# ==============================================================================
def telegram_send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    req = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(payload).encode("utf-8")
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print("[-] Lỗi gửi tin nhắn Telegram:", e, flush=True)
        return None


# ==============================================================================
# BÁO CÁO NGÀY HÔM QUA (CHẠY LÚC 08:00 SÁNG)
# ==============================================================================
def send_yesterday_daily_report():
    try:
        url = (
            f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/insights"
            f"?level=campaign"
            f"&date_preset=yesterday"
            f"&fields=campaign_id,campaign_name,spend,impressions,clicks,ctr,actions"
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
            msgs = actions.get("onsite_conversion.messaging_conversation_started_7d", 0)
            cost_per_msg = (spend / msgs) if msgs > 0 else 0

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

        today_str = datetime.now().strftime("%d/%m/%Y")
        
        good_camps = [c for c in campaign_list if c["msgs"] > 0]
        good_camps.sort(key=lambda x: x["cost_per_msg"])
        
        warning_camps = [c for c in campaign_list if (c["spend"] > 50000 and c["msgs"] == 0) or c["cost_per_msg"] > 100000]
        warning_camps.sort(key=lambda x: x["spend"], reverse=True)

        msg = f"📊 <b>BÁO CÁO FACEBOOK ADS HÔM QUA ({today_str})</b>\n"
        msg += f"🏢 Tài khoản: <b>RPB ADs account HCM</b>\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"💰 Tổng chi tiêu: <b>{total_spend:,.0f} đ</b>\n"
        msg += f"💬 Tổng tin nhắn: <b>{total_msgs} mess</b>\n"
        msg += f"🎯 Giá TB / Mess: <b>{avg_cost_per_msg:,.0f} đ/mess</b>\n"
        msg += f"🖱 Lượt Click: <b>{total_clicks:,}</b> (CTR: <b>{avg_ctr:.2f}%</b>)\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        
        msg += "🌟 <b>TOP CHIẾN DỊCH HIỆU QUẢ:</b>\n"
        if good_camps:
            for c in good_camps[:3]:
                msg += f"  • {c['name'][:35]}...\n    👉 <b>{c['msgs']} mess</b> | Giá: <b>{c['cost_per_msg']:,.0f} đ/mess</b> (Chi: {c['spend']:,.0f} đ)\n"
        else:
            msg += "  (Hôm qua chưa có tin nhắn phát sinh)\n"

        if warning_camps:
            msg += "\n⚠️ <b>CẦN CHÚ Ý (ĐẮT / CHƯA RA MESS):</b>\n"
            for c in warning_camps[:3]:
                if c["msgs"] == 0:
                    msg += f"  • {c['name'][:35]}...\n    👉 Tiêu {c['spend']:,.0f} đ (0 mess)\n"
                else:
                    msg += f"  • {c['name'][:35]}...\n    👉 Giá cao: {c['cost_per_msg']:,.0f} đ/mess (Tiêu {c['spend']:,.0f} đ)\n"

        telegram_send_message(msg)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đã gửi báo cáo ngày hôm qua thành công!", flush=True)
    except Exception as e:
        print(f"[-] Lỗi gửi báo cáo ngày hôm qua: {e}", flush=True)


# ==============================================================================
# KIỂM TRA LEAD FORM MỚI
# ==============================================================================
def check_new_leads():
    """Quét tất cả Form Lead trên các Fanpage và gửi thông báo nếu có khách mới"""
    global seen_leads
    try:
        accounts_url = f"https://graph.facebook.com/v21.0/me/accounts?fields=id,name,access_token&access_token={FB_ACCESS_TOKEN}"
        with urllib.request.urlopen(accounts_url) as resp:
            pages = json.loads(resp.read().decode()).get("data", [])
        
        for p in pages:
            pid = p.get("id")
            pname = p.get("name")
            ptoken = p.get("access_token")

            forms_url = f"https://graph.facebook.com/v21.0/{pid}/leadgen_forms?fields=id,name,status&limit=50&access_token={ptoken}"
            with urllib.request.urlopen(forms_url) as fresp:
                forms = json.loads(fresp.read().decode()).get("data", [])

            for f in forms:
                fid = f.get("id")
                fname = f.get("name")

                leads_url = f"https://graph.facebook.com/v21.0/{fid}/leads?fields=id,created_time,field_data&limit=5&access_token={ptoken}"
                try:
                    with urllib.request.urlopen(leads_url) as lresp:
                        leads = json.loads(lresp.read().decode()).get("data", [])
                    
                    for lead in leads:
                        lid = lead.get("id")
                        if lid not in seen_leads:
                            seen_leads.add(lid)
                            save_seen_leads(seen_leads)

                            c_time = lead.get("created_time", "")
                            try:
                                dt = datetime.fromisoformat(c_time.replace("Z", "+00:00"))
                                time_str = dt.strftime("%H:%M:%S - %d/%m/%Y")
                            except Exception:
                                time_str = c_time

                            field_data = lead.get("field_data", [])
                            info = {}
                            extra_fields = []
                            for fd in field_data:
                                name_key = fd.get("name", "").lower()
                                vals = fd.get("values", [])
                                val_str = vals[0] if vals else ""
                                
                                if any(k in name_key for k in ["full_name", "first_name", "name", "họ_tên", "tên"]):
                                    info["name"] = val_str
                                elif any(k in name_key for k in ["phone", "sdt", "điện_thoại", "số_điện_thoại"]):
                                    info["phone"] = val_str
                                elif any(k in name_key for k in ["email"]):
                                    info["email"] = val_str
                                else:
                                    extra_fields.append((fd.get("name", ""), val_str))

                            lead_msg = (
                                f"🔔 <b>CÓ KHÁCH HÀNG MỚI ĐĂNG KÝ (LEAD FORM)!</b>\n"
                                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                                f"🏢 Trang: <b>{pname}</b>\n"
                                f"📋 Biểu mẫu: <b>{fname}</b>\n"
                                f"⏰ Thời gian: <b>{time_str}</b>\n"
                                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                                f"👤 Khách hàng: <b>{info.get('name', 'Chưa có')}</b>\n"
                                f"📞 Số điện thoại: <b><code>{info.get('phone', 'Chưa có')}</code></b>\n"
                            )
                            if info.get("email"):
                                lead_msg += f"✉️ Email: {info.get('email')}\n"
                            
                            for k, v in extra_fields:
                                if v:
                                    lead_msg += f"💬 {k}: <b>{v}</b>\n"

                            lead_msg += (
                                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                                f"👉 <i>Đội ngũ tư vấn bấm vào SĐT để liên hệ ngay!</i>"
                            )
                            telegram_send_message(lead_msg)

                except Exception:
                    pass

    except Exception as e:
        print("[-] Lỗi khi quét Lead Form:", e, flush=True)


# ==============================================================================
# FACEBOOK ADS HEALTH & INSIGHTS CHECK
# ==============================================================================
def check_account_health():
    """Kiểm tra sức khỏe tài khoản và các camp cắn tiền hoang mỗi tiếng"""
    global alerted_campaigns_today
    
    url = (
        f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}"
        f"?fields=id,name,account_status,disable_reason,currency,amount_spent"
        f"&access_token={FB_ACCESS_TOKEN}"
    )
    try:
        with urllib.request.urlopen(url) as resp:
            acc_info = json.loads(resp.read().decode())
    except Exception as e:
        print("[-] Lỗi kiểm tra account:", e, flush=True)
        return

    status = acc_info.get("account_status", 1)
    if status != 1:
        status_desc = ACCOUNT_STATUS_MAP.get(status, f"Mã trạng thái {status}")
        alert_msg = (
            f"🚨 <b>CẢNH BÁO KHẨN CẤP TÀI KHOẢN ADS!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏢 Tài khoản: <b>{acc_info.get('name')}</b>\n"
            f"⚠️ Tình trạng: <b>{status_desc}</b>\n"
            f"👉 Vui lòng kiểm tra thẻ Visa hoặc số dư thanh toán ngay!"
        )
        telegram_send_message(alert_msg)

    today_insights_url = (
        f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/insights"
        f"?level=campaign"
        f"&date_preset=today"
        f"&fields=campaign_id,campaign_name,spend,actions"
        f"&limit=100"
        f"&access_token={FB_ACCESS_TOKEN}"
    )
    try:
        with urllib.request.urlopen(today_insights_url) as resp:
            today_data = json.loads(resp.read().decode()).get("data", [])
    except Exception as e:
        print("[-] Lỗi lấy insights today:", e, flush=True)
        return

    for item in today_data:
        cid = item.get("campaign_id")
        cname = item.get("campaign_name")
        spend = float(item.get("spend", 0))
        
        actions = {a.get("action_type"): int(a.get("value", 0)) for a in item.get("actions", [])}
        msgs = actions.get("onsite_conversion.messaging_conversation_started_7d", 0)

        if spend >= 150000 and msgs == 0 and cid not in alerted_campaigns_today:
            alerted_campaigns_today.add(cid)
            msg = (
                f"⚠️ <b>NHẮC NHỞ: CHIẾN DỊCH CẮN TIỀN CHƯA RA MESS!</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📌 Chiến dịch: <b>{cname}</b>\n"
                f"💸 Hôm nay đã tiêu: <b>{spend:,.0f} đ</b>\n"
                f"💬 Số tin nhắn: <b>0 mess</b>\n"
                f"👉 Đội ngũ nên vào kiểm tra lại bài viết/target của chiến dịch này."
            )
            telegram_send_message(msg)

def get_today_report():
    url = (
        f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/insights"
        f"?level=account"
        f"&date_preset=today"
        f"&fields=spend,impressions,clicks,ctr,actions"
        f"&access_token={FB_ACCESS_TOKEN}"
    )
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read().decode()).get("data", [])
        if not data:
            return "📊 <b>Hôm nay chưa có chi tiêu phát sinh trên tài khoản!</b>"
        
        row = data[0]
        spend = float(row.get("spend", 0))
        clicks = int(row.get("clicks", 0))
        ctr = float(row.get("ctr", 0))
        actions = {a.get("action_type"): int(a.get("value", 0)) for a in row.get("actions", [])}
        msgs = actions.get("onsite_conversion.messaging_conversation_started_7d", 0)
        cost_msg = (spend / msgs) if msgs > 0 else 0

        now_str = datetime.now().strftime("%H:%M - %d/%m/%Y")
        return (
            f"⚡ <b>SỐ LIỆU HÔM NAY (Cập nhật lúc {now_str})</b>\n"
            f"🏢 Tài khoản: <b>RPB ADs account HCM</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Đã tiêu: <b>{spend:,.0f} đ</b>\n"
            f"💬 Tin nhắn hôm nay: <b>{msgs} mess</b>\n"
            f"🎯 Giá / Mess: <b>{cost_msg:,.0f} đ/mess</b>\n"
            f"🖱 Clicks: <b>{clicks}</b> (CTR: {ctr:.2f}%)\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )
    except Exception as e:
        return f"[-] Lỗi khi tải số liệu: {e}"

def get_period_report(preset, label):
    """Lấy báo cáo chu kỳ 7 ngày hoặc 30 ngày kèm Top chiến dịch tốt nhất"""
    try:
        url_acc = (
            f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/insights"
            f"?level=account"
            f"&date_preset={preset}"
            f"&fields=spend,impressions,clicks,ctr,actions"
            f"&access_token={FB_ACCESS_TOKEN}"
        )
        with urllib.request.urlopen(url_acc) as resp:
            data = json.loads(resp.read().decode()).get("data", [])
        if not data:
            return f"📊 Không có số liệu trong {label}."

        row = data[0]
        spend = float(row.get("spend", 0))
        clicks = int(row.get("clicks", 0))
        ctr = float(row.get("ctr", 0))
        actions = {a.get("action_type"): int(a.get("value", 0)) for a in row.get("actions", [])}
        msgs = actions.get("onsite_conversion.messaging_conversation_started_7d", 0)
        cost_msg = (spend / msgs) if msgs > 0 else 0

        url_camps = (
            f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/insights"
            f"?level=campaign"
            f"&date_preset={preset}"
            f"&fields=campaign_name,spend,actions"
            f"&limit=50"
            f"&access_token={FB_ACCESS_TOKEN}"
        )
        with urllib.request.urlopen(url_camps) as resp:
            camps = json.loads(resp.read().decode()).get("data", [])

        parsed_camps = []
        for c in camps:
            c_spend = float(c.get("spend", 0))
            c_actions = {a.get("action_type"): int(a.get("value", 0)) for a in c.get("actions", [])}
            c_msgs = c_actions.get("onsite_conversion.messaging_conversation_started_7d", 0)
            c_cost_msg = (c_spend / c_msgs) if c_msgs > 0 else 0
            if c_msgs > 0:
                parsed_camps.append({
                    "name": c.get("campaign_name"),
                    "msgs": c_msgs,
                    "spend": c_spend,
                    "cost_msg": c_cost_msg
                })

        parsed_camps.sort(key=lambda x: x["cost_msg"])

        msg = f"📈 <b>BÁO CÁO ADS {label.upper()}</b>\n"
        msg += f"🏢 Tài khoản: <b>RPB ADs account HCM</b>\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"💰 Tổng chi tiêu: <b>{spend:,.0f} đ</b>\n"
        msg += f"💬 Tổng tin nhắn: <b>{msgs} mess</b>\n"
        msg += f"🎯 Giá TB / Mess: <b>{cost_msg:,.0f} đ/mess</b>\n"
        msg += f"🖱 Lượt Click: <b>{clicks:,}</b> (CTR: <b>{ctr:.2f}%</b>)\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"🌟 <b>TOP CHIẾN DỊCH HIỆU QUẢ NHẤT:</b>\n"
        if parsed_camps:
            for c in parsed_camps[:3]:
                msg += f"  • {c['name'][:35]}...\n    👉 <b>{c['msgs']} mess</b> | Giá: <b>{c['cost_msg']:,.0f} đ/mess</b> (Chi: {c['spend']:,.0f} đ)\n"
        else:
            msg += "  (Không có chiến dịch nào phát sinh tin nhắn)\n"

        return msg
    except Exception as e:
        return f"[-] Lỗi khi tải số liệu {label}: {e}"


# ==============================================================================
# TELEGRAM LONG POLLING BOT LOOP
# ==============================================================================
def run_bot():
    global last_hourly_check, last_lead_check, last_daily_report_date
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Bot RPB Ads Guard đang hoạt động...", flush=True)
    offset = 0
    
    check_account_health()
    check_new_leads()
    last_hourly_check = time.time()
    last_lead_check = time.time()

    while True:
        try:
            now_dt = datetime.now()
            now_ts = time.time()

            # 1. TỰ ĐỘNG GỬI BÁO CÁO NGÀY HÔM QUA LÚC 08:00 SÁNG
            today_date_str = now_dt.strftime("%Y-%m-%d")
            if now_dt.hour == 8 and last_daily_report_date != today_date_str:
                last_daily_report_date = today_date_str
                send_yesterday_daily_report()

            # 2. Quét Lead Form mới mỗi 3 phút
            if now_ts - last_lead_check >= 180:
                check_new_leads()
                last_lead_check = now_ts

            # 3. Quét sức khỏe tài khoản & cảnh báo camp mỗi 1 tiếng
            if now_ts - last_hourly_check >= 3600:
                check_account_health()
                last_hourly_check = now_ts

            # 4. Lắng nghe lệnh từ Telegram
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset}&timeout=10"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as resp:
                updates = json.loads(resp.read().decode()).get("result", [])

            for u in updates:
                offset = u.get("update_id") + 1

                if "message" in u and "text" in u["message"]:
                    raw_text = u["message"]["text"].strip()
                    # Loại bỏ @rpb_ads_report_bot nếu người dùng gõ /today@rpb_ads_report_bot
                    msg_text = raw_text.split("@")[0].lower()
                    
                    # A. Báo cáo hôm nay
                    if msg_text in ["/today", "/bc", "today", "báo cáo"]:
                        report = get_today_report()
                        telegram_send_message(report)

                    # B. Báo cáo 7 ngày
                    elif msg_text in ["/7day", "/7ngay", "/tuan", "7day", "tuần", "/week"]:
                        report = get_period_report("last_7d", "7 ngày gần nhất")
                        telegram_send_message(report)

                    # C. Báo cáo 30 ngày (1 tháng)
                    elif msg_text in ["/30day", "/30ngay", "/thang", "30day", "tháng", "/month", "/1thang"]:
                        report = get_period_report("last_30d", "30 ngày (1 tháng)")
                        telegram_send_message(report)

                    # D. Hướng dẫn lệnh
                    elif msg_text in ["/help", "help", "/start"]:
                        help_text = (
                            f"🤖 <b>DANH SÁCH LỆNH XEM BÁO CÁO ADS:</b>\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"• Gõ <code>/today</code> hoặc <code>/bc</code>: Xem chi tiêu & tin nhắn <b>Hôm nay</b>\n"
                            f"• Gõ <code>/7day</code> hoặc <code>/tuan</code>: Xem báo cáo <b>7 ngày qua</b> + Top camp rẻ nhất\n"
                            f"• Gõ <code>/30day</code> hoặc <code>/thang</code>: Xem báo cáo <b>30 ngày qua</b> + Top camp rẻ nhất\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"• <b>Tự động 8h sáng:</b> Báo cáo tổng kết ngày hôm qua\n"
                            f"• <b>Tự động mỗi 1 tiếng:</b> Cảnh báo lỗi thẻ/khóa tài khoản hoặc camp cắn tiền lố\n"
                            f"• <b>Tự động mỗi 3 phút:</b> Bắn SĐT khách mới từ Lead Form vào nhóm."
                        )
                        telegram_send_message(help_text)

        except Exception as e:
            time.sleep(3)

        time.sleep(1)

if __name__ == "__main__":
    run_bot()

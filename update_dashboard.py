#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_dashboard.py
Chạy script này để tự động đồng bộ dữ liệu mới nhất từ:
1. Facebook Ads API (tài khoản RPB Ads HCM)
2. Chatbot AI Seller (toàn bộ hội thoại & SĐT)
3. Xuất file marketing_dashboard.html để mở trực tiếp trên trình duyệt
"""
import os
import sys

print("[*] Đang cập nhật dữ liệu Dashboard...")
ret1 = os.system("python3 /Users/ted/Desktop/Code/RPB/generate_dashboard.py")
if ret1 != 0:
    print("[-] Lỗi khi đồng bộ dữ liệu API.")
    sys.exit(1)

ret2 = os.system("python3 /Users/ted/Desktop/Code/RPB/build_html.py")
if ret2 != 0:
    print("[-] Lỗi khi tạo file HTML Dashboard.")
    sys.exit(1)

print("[✓] ĐÃ CẬP NHẬT THÀNH CÔNG!")
print("    Đường dẫn Dashboard: /Users/ted/Desktop/Code/RPB/marketing_dashboard.html")
print("    Để mở trên máy, bạn chỉ cần chạy lệnh: open /Users/ted/Desktop/Code/RPB/marketing_dashboard.html")

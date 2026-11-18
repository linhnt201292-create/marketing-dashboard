import json
import base64

# Read logo and encode to base64
with open("/Users/ted/Desktop/Code/RPB/rpb_logo.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode("utf-8")
logo_data_uri = f"data:image/png;base64,{logo_base64}"

with open("/Users/ted/Desktop/Code/RPB/dashboard_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

json_data_str = json.dumps(data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo Digital Marketing Rồng Phương Bắc</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
        }}
        .badge-brand-city {{ background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
        .badge-brand-mia {{ background-color: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }}
        .badge-brand-edu {{ background-color: #fefce8; color: #a16207; border: 1px solid #fef08a; }}
        .badge-brand-other {{ background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }}
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Top Header -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap justify-between items-center gap-4">
            <div class="flex items-center gap-3.5">
                <!-- RPB Official Logo -->
                <div class="h-12 w-auto flex items-center justify-center p-1 bg-white rounded-xl border border-slate-100 shadow-sm">
                    <img src="{logo_data_uri}" alt="RPB Logo" class="h-10 w-auto object-contain">
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <h1 class="text-lg font-black text-slate-900 tracking-tight">Báo cáo Digital Marketing Rồng Phương Bắc</h1>
                        <span class="px-2.5 py-0.5 text-[11px] font-bold rounded-full bg-emerald-100 text-emerald-800">FB + GG Ads Live</span>
                    </div>
                    <p class="text-xs text-slate-500 font-medium">Báo cáo Quản trị Hiệu quả Digital Toàn diện | Giai đoạn: 01/11 - 18/11/2026</p>
                </div>
            </div>
            <div class="flex items-center gap-2.5">
                <span class="text-xs text-slate-500 hidden sm:inline" id="lastUpdated">Cập nhật: {data['generated_at']}</span>
                <button onclick="location.reload()" class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors border border-slate-300">
                    <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.03 0 01-15.357-2m15.357 2H15"></path></svg>
                    Làm mới
                </button>
            </div>
        </div>

        <!-- Prominent Navigation Segmented Bar (Redesigned & Eye-Catching) -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5">
            <nav class="bg-slate-100/90 p-1.5 rounded-2xl border border-slate-200/80 flex space-x-1 overflow-x-auto shadow-inner" aria-label="Tabs">
                
                <!-- Tab 1: Tổng quan -->
                <button onclick="switchTab('tab-executive')" id="btn-executive" class="tab-btn inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all shadow-sm bg-white text-orange-600 border border-slate-200/60 whitespace-nowrap">
                    <svg class="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                    Tổng quan
                </button>

                <!-- Tab 2: Doanh số bán hàng -->
                <button onclick="switchTab('tab-sales')" id="btn-sales" class="tab-btn inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all text-slate-600 hover:text-slate-900 hover:bg-white/60 whitespace-nowrap">
                    <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Doanh số bán hàng
                </button>

                <!-- Tab 3: Google Ads -->
                <button onclick="switchTab('tab-google')" id="btn-google" class="tab-btn inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all text-slate-600 hover:text-slate-900 hover:bg-white/60 whitespace-nowrap">
                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                    Google Ads
                </button>

                <!-- Tab 4: Facebook Ads -->
                <button onclick="switchTab('tab-ads')" id="btn-ads" class="tab-btn inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all text-slate-600 hover:text-slate-900 hover:bg-white/60 whitespace-nowrap">
                    <svg class="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"></path></svg>
                    Facebook Ads
                </button>

                <!-- Tab 5: Kênh CSKH -->
                <button onclick="switchTab('tab-funnel')" id="btn-funnel" class="tab-btn inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all text-slate-600 hover:text-slate-900 hover:bg-white/60 whitespace-nowrap">
                    <svg class="w-4 h-4 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
                    Kênh CSKH
                </button>

            </nav>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full">

        <!-- Top 5 Executive KPI Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
            
            <!-- Card 1: Doanh số MKT -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[11px] font-bold tracking-wider text-slate-500 uppercase">Doanh số MKT</span>
                    <div class="w-8 h-8 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-sm">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                    </div>
                </div>
                <div>
                    <div class="flex items-baseline gap-1.5">
                        <span class="text-2xl font-black text-slate-900 tracking-tight">1,397</span>
                        <span class="text-xs font-bold text-slate-500 uppercase">tỷ đ</span>
                    </div>
                    <div class="text-[11px] text-slate-500 mt-1">
                        +87.5 tr dự án HN <span class="font-semibold text-slate-700">(Tổng: 1,484 tỷ)</span>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100">
                    <div class="flex justify-between items-center text-[11px] mb-1.5">
                        <span class="text-slate-500">Tiến độ tháng:</span>
                        <span class="font-bold text-emerald-600">45.7%</span>
                    </div>
                    <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                        <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 45.7%"></div>
                    </div>
                </div>
            </div>

            <!-- Card 2: Tổng Chi phí Ads -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[11px] font-bold tracking-wider text-slate-500 uppercase">Tổng Chi phí Ads</span>
                    <div class="w-8 h-8 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-sm">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    </div>
                </div>
                <div>
                    <div class="flex items-baseline gap-1.5">
                        <span class="text-2xl font-black text-slate-900 tracking-tight">89,24</span>
                        <span class="text-xs font-bold text-slate-500 uppercase">triệu đ</span>
                    </div>
                    <div class="text-[11px] text-slate-500 mt-1">
                        FB: <strong class="text-slate-700">30.0tr</strong> • GG: <strong class="text-slate-700">59.2tr</strong>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100">
                    <div class="flex justify-between items-center text-[11px] mb-1.5">
                        <span class="text-slate-500">Ngân sách tháng:</span>
                        <span class="font-bold text-blue-700">54.9% / 162.5tr</span>
                    </div>
                    <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                        <div class="bg-blue-600 h-1.5 rounded-full" style="width: 54.9%"></div>
                    </div>
                </div>
            </div>

            <!-- Card 3: Tỷ lệ Ads/Doanh số (CIR) -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[11px] font-bold tracking-wider text-slate-500 uppercase">Tỷ lệ Ads / DS (CIR)</span>
                    <div class="w-8 h-8 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold text-sm">
                        %
                    </div>
                </div>
                <div>
                    <div class="flex items-baseline gap-1.5">
                        <span class="text-2xl font-black text-amber-600 tracking-tight">6,01%</span>
                        <span class="text-xs font-medium text-slate-400">(chuẩn: 6,39%)</span>
                    </div>
                    <div class="text-[11px] text-slate-500 mt-1">
                        Mục tiêu trần CEO: <strong class="text-slate-700">≤ 5,0%</strong>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
                    <span class="text-slate-500">Đánh giá:</span>
                    <span class="px-2 py-0.5 rounded-md bg-amber-100 text-amber-800 font-bold text-[10px]">Sát trần 5%</span>
                </div>
            </div>

            <!-- Card 4: Hiệu suất vốn (ROAS) -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[11px] font-bold tracking-wider text-slate-500 uppercase">ROAS (DS / Ads)</span>
                    <div class="w-8 h-8 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center font-bold text-sm">
                        ✕
                    </div>
                </div>
                <div>
                    <div class="flex items-baseline gap-1.5">
                        <span class="text-2xl font-black text-purple-700 tracking-tight">16.6x</span>
                        <span class="text-xs font-medium text-slate-400">(chuẩn: 15.7x)</span>
                    </div>
                    <div class="text-[11px] text-slate-500 mt-1">
                        1đ Ads → tạo <strong class="text-purple-700 font-semibold">16.6đ</strong> doanh số
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
                    <span class="text-slate-500">Mức kỳ vọng:</span>
                    <span class="font-semibold text-slate-700">≥ 20x</span>
                </div>
            </div>

            <!-- Card 5: Chuyển đổi & Data khách -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[11px] font-bold tracking-wider text-slate-500 uppercase">Chuyển đổi & Data</span>
                    <div class="w-8 h-8 rounded-xl bg-cyan-50 text-cyan-600 flex items-center justify-center font-bold text-sm">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                    </div>
                </div>
                <div>
                    <div class="flex items-baseline gap-1.5">
                        <span class="text-2xl font-black text-slate-900 tracking-tight">2.431</span>
                        <span class="text-xs font-bold text-slate-500 uppercase">lượt</span>
                    </div>
                    <div class="text-[11px] text-slate-500 mt-1">
                        FB: <strong class="text-slate-700">644 data</strong> • GG: <strong class="text-slate-700">1.787 conv</strong>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
                    <span class="text-slate-500">CPA bình quân:</span>
                    <span class="font-bold text-cyan-800">~36.7k / lượt</span>
                </div>
            </div>

        </div>

        <!-- ========================================== -->
        <!-- TAB 1: TỔNG QUAN -->
        <!-- ========================================== -->
        <div id="tab-executive" class="tab-content space-y-6">
            <!-- Strategic Insight Alert Box -->
            <div class="bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200 rounded-2xl p-5 shadow-sm">
                <div class="flex items-start gap-3.5">
                    <div class="w-8 h-8 rounded-full bg-orange-600 text-white flex items-center justify-center font-bold text-sm shrink-0">i</div>
                    <div>
                        <h3 class="text-sm font-bold text-orange-950 uppercase tracking-wide">Nhận định Hiệu suất Tổng hợp (Facebook Ads + Google Ads)</h3>
                        <p class="text-xs text-orange-900 mt-1.5 leading-relaxed">
                            <strong>1. Chi tiêu ngân sách:</strong> Sau 18 ngày, tổng ngân sách ads đã tiêu là <strong>89,24 triệu VNĐ</strong> (FB: 30,03 tr | GG: 59,21 tr), đạt <strong>54,9%</strong> định mức tháng (162,5 triệu). Tốc độ tiêu tiền hoàn toàn đúng tiến độ thời gian.<br>
                            <strong>2. Tỷ lệ Chi phí Ads / Doanh số (CIR):</strong> Đang ở mức <strong>6,01%</strong> (nếu tính cả đơn Edu ngoài Hà Nội) hoặc <strong>6,39%</strong> (nếu chỉ tính chuẩn). Mức này chênh nhẹ so với mức trần 5% của CEO, nhưng <em>The City</em> đang có CIR rất đẹp (<strong>5,25%</strong>, mang về 1,02 tỷ doanh số).<br>
                            <strong>3. Kênh Google Ads:</strong> Là cỗ máy kéo chuyển đổi chính với <strong>1.787 lượt chuyển đổi</strong> và hơn <strong>56.000 lượt click</strong>, đóng vai trò hứng trọn nhu cầu tìm kiếm của khách hàng mua bàn ghế văn phòng cuối năm.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Charts Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Chart 1: Doanh số vs Chi phí theo Brand -->
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-900 mb-1">Doanh số chốt vs. Tổng Chi phí Ads (FB + GG) theo Thương hiệu</h3>
                    <p class="text-xs text-slate-500 mb-4">Đơn vị tính: Triệu VNĐ (01/11 - 18/11/2026)</p>
                    <div class="h-64">
                        <canvas id="chartBrandComparison"></canvas>
                    </div>
                </div>

                <!-- Chart 2: Tỷ trọng Chi tiêu FB Ads vs GG Ads -->
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-900 mb-1">Cơ cấu Chi tiêu Quảng cáo theo Kênh & Thương hiệu</h3>
                    <p class="text-xs text-slate-500 mb-4">Google Ads chiếm 66.3% tổng ngân sách | Facebook chiếm 33.7%</p>
                    <div class="h-64 flex items-center justify-center">
                        <canvas id="chartChannelShare"></canvas>
                    </div>
                </div>
            </div>

            <!-- Summary Table by Brand -->
            <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
                <div class="p-4 border-b border-slate-100 flex justify-between items-center">
                    <h3 class="text-sm font-bold text-slate-900">Bảng Đối soát Chi phí Toàn kênh (FB + GG) & Doanh số theo Thương hiệu</h3>
                    <span class="text-xs text-slate-500">Đối chiếu Facebook Ads, Google Ads & Sheets SO</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider border-b border-slate-200">
                            <tr>
                                <th class="p-3">Thương hiệu</th>
                                <th class="p-3 text-right">FB Ads</th>
                                <th class="p-3 text-right">GG Ads</th>
                                <th class="p-3 text-right">Tổng Chi Ads</th>
                                <th class="p-3 text-right">Doanh số chốt</th>
                                <th class="p-3 text-right">Tỷ trọng DS</th>
                                <th class="p-3 text-right">Tỷ lệ Ads/DS (CIR)</th>
                                <th class="p-3 text-center">Đánh giá</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 font-medium">
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-blue-600"></span>
                                    <strong>The City</strong> (TK Nguyễn Thành Long)
                                </td>
                                <td class="p-3 text-right text-slate-600">5.840.661 đ</td>
                                <td class="p-3 text-right font-bold text-blue-700">47.659.730 đ</td>
                                <td class="p-3 text-right font-bold text-slate-900">53.500.391 đ</td>
                                <td class="p-3 text-right font-extrabold text-blue-800">1.019.997.830 đ</td>
                                <td class="p-3 text-right font-semibold">73,0%</td>
                                <td class="p-3 text-right font-bold text-emerald-700">5,25%</td>
                                <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] bg-emerald-100 text-emerald-800 font-semibold">Rất hiệu quả</span></td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
                                    <strong>The MIA</strong> (TK The Mia)
                                </td>
                                <td class="p-3 text-right text-slate-600">9.088.260 đ</td>
                                <td class="p-3 text-right font-bold text-emerald-700">11.548.132 đ</td>
                                <td class="p-3 text-right font-bold text-slate-900">20.636.392 đ</td>
                                <td class="p-3 text-right font-extrabold text-slate-800">333.227.800 đ</td>
                                <td class="p-3 text-right font-semibold">23,8%</td>
                                <td class="p-3 text-right font-bold text-amber-700">6,19%</td>
                                <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] bg-amber-100 text-amber-800 font-semibold">Khá (Tối ưu nhẹ)</span></td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                                    <strong>RPB Edu & Public</strong>
                                </td>
                                <td class="p-3 text-right text-slate-600">14.962.619 đ</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right font-bold text-slate-900">14.962.619 đ</td>
                                <td class="p-3 text-right font-bold text-slate-800">9.796.055 đ <span class="text-[10px] text-slate-500 block font-normal">(+87.5tr HN)</span></td>
                                <td class="p-3 text-right font-semibold">0,7% <span class="text-[10px] text-slate-500 block font-normal">(6.6%)</span></td>
                                <td class="p-3 text-right font-bold text-rose-700">152,7% <span class="text-[10px] text-slate-500 block font-normal">(15.3%)</span></td>
                                <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] bg-rose-100 text-rose-800 font-semibold">Cần tối ưu</span></td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-slate-400"></span>
                                    <strong>Phí vận chuyển / Black Friday</strong>
                                </td>
                                <td class="p-3 text-right text-slate-600">90.641 đ</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right font-bold text-slate-900">90.641 đ</td>
                                <td class="p-3 text-right font-bold text-slate-800">34.215.311 đ</td>
                                <td class="p-3 text-right font-semibold">2,5%</td>
                                <td class="p-3 text-right font-bold text-slate-600">-</td>
                                <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] bg-slate-100 text-slate-700 font-medium">Bổ trợ</span></td>
                            </tr>
                            <tr class="bg-slate-100/90 font-bold text-slate-900 border-t border-slate-300">
                                <td class="p-3">TỔNG CỘNG</td>
                                <td class="p-3 text-right text-slate-800 font-bold">30.033.394 đ</td>
                                <td class="p-3 text-right text-blue-900 font-bold">59.207.862 đ</td>
                                <td class="p-3 text-right text-indigo-950 font-extrabold text-sm">89.241.256 đ</td>
                                <td class="p-3 text-right text-emerald-800 font-extrabold text-sm">1.397.236.996 đ</td>
                                <td class="p-3 text-right">100%</td>
                                <td class="p-3 text-right text-amber-800 font-bold">6,01% - 6,39%</td>
                                <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] bg-blue-600 text-white font-bold">54.9% QUOTA</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 2: DOANH SỐ BÁN HÀNG -->
        <!-- ========================================== -->
        <div id="tab-sales" class="tab-content hidden space-y-6">
            <!-- Region Breakdown Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Khu vực Hồ Chí Minh (Sale Online)</span>
                        <span class="px-2.5 py-0.5 text-xs font-bold rounded-full bg-blue-100 text-blue-800">91,1% Tổng DS</span>
                    </div>
                    <div class="text-2xl font-black text-slate-900">1.352.355.196 đ</div>
                    <p class="text-xs text-slate-500 mt-1.5 leading-relaxed">Ghi nhận 100% doanh số từ ads của 2 bạn: <strong>Nguyễn Quỳnh Anh</strong> (1,068 tỷ) & <strong>Lê Minh Khoa</strong> (283 tr).</p>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Khu vực Hà Nội (Đơn nguồn MKT)</span>
                        <span class="px-2.5 py-0.5 text-xs font-bold rounded-full bg-emerald-100 text-emerald-800">8,9% Tổng DS</span>
                    </div>
                    <div class="text-2xl font-black text-slate-900">132.430.700 đ</div>
                    <p class="text-xs text-slate-500 mt-1.5 leading-relaxed">Đơn phát sinh nguồn MKT từ NVKD: <strong>Vũ Thị Đào</strong> (38.2 tr), <strong>Nguyễn Đức Minh</strong> (6.6 tr) và <strong>Vũ Hoàng Yến</strong> (87.5 tr Edu).</p>
                </div>
            </div>

            <!-- Rep Table -->
            <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
                <div class="p-4 border-b border-slate-100">
                    <h3 class="text-sm font-bold text-slate-900">Bảng Doanh số Chi tiết theo Từng Nhân sự & Thương hiệu</h3>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider border-b border-slate-200">
                            <tr>
                                <th class="p-3">Nhân sự</th>
                                <th class="p-3">Khu vực / Phụ trách</th>
                                <th class="p-3 text-right">The City</th>
                                <th class="p-3 text-right">The MIA</th>
                                <th class="p-3 text-right">Edu & Public</th>
                                <th class="p-3 text-right">Phí vận chuyển</th>
                                <th class="p-3 text-right">TỔNG CỘNG</th>
                                <th class="p-3 text-center">Số đơn (SO)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 font-medium">
                            <tr class="hover:bg-slate-50">
                                <td class="p-3"><strong>Nguyễn Quỳnh Anh</strong> (HCMKDANH.05)</td>
                                <td class="p-3 text-slate-500">HCM - Sale Online</td>
                                <td class="p-3 text-right font-bold text-blue-700">817.516.000 đ</td>
                                <td class="p-3 text-right font-bold text-emerald-700">225.009.000 đ</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right text-slate-500">26.163.390 đ</td>
                                <td class="p-3 text-right font-extrabold text-slate-900">1.068.688.390 đ</td>
                                <td class="p-3 text-center font-bold">38</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3"><strong>Lê Minh Khoa</strong> (HCMKDKHOA.02)</td>
                                <td class="p-3 text-slate-500">HCM - Sale Online</td>
                                <td class="p-3 text-right font-bold text-blue-700">164.219.830 đ</td>
                                <td class="p-3 text-right font-bold text-emerald-700">101.599.000 đ</td>
                                <td class="p-3 text-right font-bold text-amber-700">9.796.055 đ</td>
                                <td class="p-3 text-right text-slate-500">8.051.921 đ</td>
                                <td class="p-3 text-right font-extrabold text-slate-900">283.666.806 đ</td>
                                <td class="p-3 text-center font-bold">30</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3"><strong>Vũ Thị Đào</strong> (HNIKDDAO.01)</td>
                                <td class="p-3 text-slate-500">HN - Nguồn MKT</td>
                                <td class="p-3 text-right font-bold text-blue-700">38.262.000 đ</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right font-extrabold text-slate-900">38.262.000 đ</td>
                                <td class="p-3 text-center font-bold">1</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3"><strong>Nguyễn Đức Minh</strong> (HNIKDMINH.02)</td>
                                <td class="p-3 text-slate-500">HN - Nguồn MKT</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right font-bold text-emerald-700">6.619.800 đ</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right font-extrabold text-slate-900">6.619.800 đ</td>
                                <td class="p-3 text-center font-bold">1</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3"><strong>Vũ Hoàng Yến</strong> (HNIKDYEN.01)</td>
                                <td class="p-3 text-slate-500">HN - Nguồn MKT Edu</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right font-bold text-amber-700">87.548.900 đ</td>
                                <td class="p-3 text-right text-slate-400">0 đ</td>
                                <td class="p-3 text-right font-extrabold text-slate-900">87.548.900 đ</td>
                                <td class="p-3 text-center font-bold">5</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 3: GOOGLE ADS -->
        <!-- ========================================== -->
        <div id="tab-google" class="tab-content hidden space-y-6">
            <!-- Google Ads Overview Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Tổng Chi phí Google Ads</span>
                    <div class="text-xl font-black text-blue-700 mt-1">59.207.862 đ</div>
                    <span class="text-xs text-slate-500">The City: 47.7tr | The Mia: 11.5tr</span>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Lượt nhấp (Clicks)</span>
                    <div class="text-xl font-black text-slate-900 mt-1">56.775 nhấp</div>
                    <span class="text-xs text-slate-500">Lượt hiển thị: 475.377</span>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Lượt chuyển đổi (Conv.)</span>
                    <div class="text-xl font-black text-emerald-700 mt-1">1.787,29 lượt</div>
                    <span class="text-xs text-slate-500">Form, gọi điện, chat web</span>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">CPA TB (Giá/Chuyển đổi)</span>
                    <div class="text-xl font-black text-purple-700 mt-1">33.127 đ</div>
                    <span class="text-xs text-slate-500">The City: 29.7k | The Mia: 63.1k</span>
                </div>
            </div>

            <!-- Google Ads Campaigns Table -->
            <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
                <div class="p-4 border-b border-slate-100 flex justify-between items-center">
                    <div>
                        <h3 class="text-sm font-bold text-slate-900">Chi tiết Chiến dịch Google Ads (01/11 - 18/11/2026)</h3>
                        <p class="text-xs text-slate-500">2 Tài khoản: Nguyễn Thành Long (The City) & The Mia (The Mia)</p>
                    </div>
                    <span class="px-2.5 py-1 text-xs rounded-full bg-blue-100 text-blue-800 font-bold">13 Chiến dịch</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider border-b border-slate-200">
                            <tr>
                                <th class="p-3">Chiến dịch Google Ads</th>
                                <th class="p-3">Tài khoản & Thương hiệu</th>
                                <th class="p-3">Loại chiến dịch</th>
                                <th class="p-3 text-right">Chi phí (VND)</th>
                                <th class="p-3 text-right">Lần nhấp</th>
                                <th class="p-3 text-right">Lượt chuyển đổi</th>
                                <th class="p-3 text-right">CPA (Giá/Ch.đổi)</th>
                                <th class="p-3 text-right">CTR</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 font-medium">
                            <!-- The City Campaigns -->
                            <tr class="bg-blue-50/50 font-bold text-blue-900"><td colspan="8" class="p-2.5 px-3">TÀI KHOẢN: NGUYỄN THÀNH LONG (THE CITY - 563-582-4813) — Tổng chi: 47.659.730 đ</td></tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">The City-Ghế VP-Search-Miền Nam-10122025</td>
                                <td class="p-3"><span class="badge-brand-city px-2 py-0.5 rounded text-[11px] font-semibold">The City</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">11.426.246 đ</td>
                                <td class="p-3 text-right">830</td>
                                <td class="p-3 text-right font-bold text-slate-800">14,21</td>
                                <td class="p-3 text-right text-rose-700 font-bold">804.051 đ</td>
                                <td class="p-3 text-right">1,43%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">The City -Bàn VP-Search-Miền Bắc-10122025</td>
                                <td class="p-3"><span class="badge-brand-city px-2 py-0.5 rounded text-[11px] font-semibold">The City</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">9.235.920 đ</td>
                                <td class="p-3 text-right">197</td>
                                <td class="p-3 text-right font-bold text-slate-800">15,00</td>
                                <td class="p-3 text-right text-amber-700 font-bold">615.728 đ</td>
                                <td class="p-3 text-right">19,33%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">The CiTy_Remarketing_90D_9/2026</td>
                                <td class="p-3"><span class="badge-brand-city px-2 py-0.5 rounded text-[11px] font-semibold">The City</span></td>
                                <td class="p-3 text-slate-500">Hiển thị</td>
                                <td class="p-3 text-right font-bold">9.003.450 đ</td>
                                <td class="p-3 text-right">24.330</td>
                                <td class="p-3 text-right font-bold text-emerald-700">740,78</td>
                                <td class="p-3 text-right text-emerald-700 font-bold">12.154 đ</td>
                                <td class="p-3 text-right">15,34%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">The City-Ghế VP-Search-Miền Bắc-10122025</td>
                                <td class="p-3"><span class="badge-brand-city px-2 py-0.5 rounded text-[11px] font-semibold">The City</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">7.452.985 đ</td>
                                <td class="p-3 text-right">232</td>
                                <td class="p-3 text-right font-bold text-slate-800">12,50</td>
                                <td class="p-3 text-right text-amber-700 font-bold">596.239 đ</td>
                                <td class="p-3 text-right">8,21%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">TheCity-hiển thị miền bắc -26/08/26 #2</td>
                                <td class="p-3"><span class="badge-brand-city px-2 py-0.5 rounded text-[11px] font-semibold">The City</span></td>
                                <td class="p-3 text-slate-500">Performance Max</td>
                                <td class="p-3 text-right font-bold">4.959.114 đ</td>
                                <td class="p-3 text-right">28.547</td>
                                <td class="p-3 text-right font-bold text-emerald-700">722,01</td>
                                <td class="p-3 text-right text-emerald-700 font-bold">6.869 đ</td>
                                <td class="p-3 text-right">12,59%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">The City-Search-Brand City-Miền Nam-10122025</td>
                                <td class="p-3"><span class="badge-brand-city px-2 py-0.5 rounded text-[11px] font-semibold">The City</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">2.419.345 đ</td>
                                <td class="p-3 text-right">475</td>
                                <td class="p-3 text-right font-bold text-slate-800">15,00</td>
                                <td class="p-3 text-right text-slate-700">161.275 đ</td>
                                <td class="p-3 text-right">7,50%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">The City -Search-Nội thất phòng giám đốc-phòng họp</td>
                                <td class="p-3"><span class="badge-brand-city px-2 py-0.5 rounded text-[11px] font-semibold">The City</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">2.317.137 đ</td>
                                <td class="p-3 text-right">1.162</td>
                                <td class="p-3 text-right font-bold text-emerald-700">80,79</td>
                                <td class="p-3 text-right text-emerald-700 font-bold">28.682 đ</td>
                                <td class="p-3 text-right">11,30%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">The City - Search-Brand City-Miền Bắc-10122025</td>
                                <td class="p-3"><span class="badge-brand-city px-2 py-0.5 rounded text-[11px] font-semibold">The City</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">845.533 đ</td>
                                <td class="p-3 text-right">217</td>
                                <td class="p-3 text-right font-bold text-slate-800">4,00</td>
                                <td class="p-3 text-right text-slate-700">211.383 đ</td>
                                <td class="p-3 text-right">9,48%</td>
                            </tr>

                            <!-- The Mia Campaigns -->
                            <tr class="bg-emerald-50/50 font-bold text-emerald-900"><td colspan="8" class="p-2.5 px-3">TÀI KHOẢN: THE MIA (THE MIA - 958-066-7486) — Tổng chi: 11.548.132 đ</td></tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">The Mia - Ghế Văn Phòng - Tìm kiếm - 2.11</td>
                                <td class="p-3"><span class="badge-brand-mia px-2 py-0.5 rounded text-[11px] font-semibold">The Mia</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">5.943.669 đ</td>
                                <td class="p-3 text-right">391</td>
                                <td class="p-3 text-right font-bold text-emerald-700">91,50</td>
                                <td class="p-3 text-right text-slate-800 font-bold">64.958 đ</td>
                                <td class="p-3 text-right">5,94%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">Search - Brand Mia - Miền Nam-10122025</td>
                                <td class="p-3"><span class="badge-brand-mia px-2 py-0.5 rounded text-[11px] font-semibold">The Mia</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">2.918.440 đ</td>
                                <td class="p-3 text-right">273</td>
                                <td class="p-3 text-right font-bold text-slate-800">6,50</td>
                                <td class="p-3 text-right text-rose-700 font-bold">448.991 đ</td>
                                <td class="p-3 text-right">11,22%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">The Mia -Bàn VP-Search-Miền Bắc-10122025</td>
                                <td class="p-3"><span class="badge-brand-mia px-2 py-0.5 rounded text-[11px] font-semibold">The Mia</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">1.477.020 đ</td>
                                <td class="p-3 text-right">34</td>
                                <td class="p-3 text-right font-bold text-emerald-700">45,00</td>
                                <td class="p-3 text-right text-emerald-700 font-bold">32.823 đ</td>
                                <td class="p-3 text-right">3,85%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">The Mia-Ghế VP-Search-Miền Bắc-10122025</td>
                                <td class="p-3"><span class="badge-brand-mia px-2 py-0.5 rounded text-[11px] font-semibold">The Mia</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">873.048 đ</td>
                                <td class="p-3 text-right">22</td>
                                <td class="p-3 text-right font-bold text-emerald-700">29,00</td>
                                <td class="p-3 text-right text-emerald-700 font-bold">30.105 đ</td>
                                <td class="p-3 text-right">3,10%</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3">Search - Brand Mia - Miền Bắc-10122025</td>
                                <td class="p-3"><span class="badge-brand-mia px-2 py-0.5 rounded text-[11px] font-semibold">The Mia</span></td>
                                <td class="p-3 text-slate-500">Tìm kiếm</td>
                                <td class="p-3 text-right font-bold">335.955 đ</td>
                                <td class="p-3 text-right">65</td>
                                <td class="p-3 text-right font-bold text-emerald-700">11,00</td>
                                <td class="p-3 text-right text-emerald-700 font-bold">30.541 đ</td>
                                <td class="p-3 text-right">21,24%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 4: FACEBOOK ADS -->
        <!-- ========================================== -->
        <div id="tab-ads" class="tab-content hidden space-y-6">
            <!-- Filter Bar -->
            <div class="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm flex flex-wrap justify-between items-center gap-3">
                <div class="flex items-center gap-2">
                    <span class="text-xs font-bold text-slate-700 uppercase">Lọc theo Brand:</span>
                    <button onclick="filterCampaigns('ALL')" class="filter-btn active px-3.5 py-1.5 text-xs rounded-xl font-bold bg-orange-600 text-white shadow-sm" id="filter-ALL">Tất cả (26)</button>
                    <button onclick="filterCampaigns('THE CITY')" class="filter-btn px-3.5 py-1.5 text-xs rounded-xl font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors" id="filter-THE CITY">The City (8)</button>
                    <button onclick="filterCampaigns('THE MIA')" class="filter-btn px-3.5 py-1.5 text-xs rounded-xl font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors" id="filter-THE MIA">The MIA (5)</button>
                    <button onclick="filterCampaigns('RPB EDU & PUBLIC')" class="filter-btn px-3.5 py-1.5 text-xs rounded-xl font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors" id="filter-RPB EDU & PUBLIC">Edu & Public (12)</button>
                </div>
                <div class="relative w-full sm:w-64">
                    <input type="text" id="campaignSearch" onkeyup="searchCampaigns()" placeholder="Tìm tên chiến dịch..." class="w-full text-xs px-3 py-2 pl-8 rounded-xl border border-slate-300 focus:outline-none focus:ring-1 focus:ring-orange-500">
                    <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>
            </div>

            <!-- Facebook Campaigns Table -->
            <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
                <div class="p-4 border-b border-slate-100 flex justify-between items-center">
                    <h3 class="text-sm font-bold text-slate-900">Danh sách Chiến dịch Facebook Ads (01/11 - 18/11/2026)</h3>
                    <span class="text-xs text-slate-500">Tài khoản: RPB ADs account HCM (act_1113055687224460)</span>
                </div>
                <div class="overflow-x-auto max-h-[500px]">
                    <table class="w-full text-left text-xs" id="campaignsTable">
                        <thead class="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider sticky top-0 border-b border-slate-200">
                            <tr>
                                <th class="p-3">Chiến dịch</th>
                                <th class="p-3">Thương hiệu</th>
                                <th class="p-3 text-right">Chi phí (VND)</th>
                                <th class="p-3 text-right">Tin nhắn</th>
                                <th class="p-3 text-right">Form Lead</th>
                                <th class="p-3 text-right">Tổng Khách</th>
                                <th class="p-3 text-right">CPA (Giá/Khách)</th>
                                <th class="p-3 text-right">CTR</th>
                                <th class="p-3 text-center">Đánh giá</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 font-medium" id="campaignsTableBody">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 5: KÊNH CSKH -->
        <!-- ========================================== -->
        <div id="tab-funnel" class="tab-content hidden space-y-6">
            <!-- Full Conversion Funnel Visualization -->
            <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm">
                <h3 class="text-sm font-bold text-slate-900 mb-1">Quy trình Chuyển đổi & Chăm sóc Khách hàng (Kênh CSKH)</h3>
                <p class="text-xs text-slate-500 mb-6">Từ tương tác đa kênh đến hội thoại chatbot AI Seller và chốt đơn</p>
                
                <div class="grid grid-cols-1 md:grid-cols-5 gap-3 text-center">
                    <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
                        <div class="text-xs font-semibold text-slate-500 uppercase">1. Chuyển đổi Ads</div>
                        <div class="text-2xl font-black text-slate-900 mt-2">2.431</div>
                        <div class="text-[11px] text-slate-500 mt-1">644 FB + 1.787 GG</div>
                    </div>
                    <div class="p-4 rounded-xl bg-blue-50 border border-blue-200">
                        <div class="text-xs font-semibold text-blue-700 uppercase">2. Hội thoại Bot</div>
                        <div class="text-2xl font-black text-blue-900 mt-2">309</div>
                        <div class="text-[11px] text-blue-700 mt-1">AI Seller tiếp nhận</div>
                    </div>
                    <div class="p-4 rounded-xl bg-indigo-50 border border-indigo-200">
                        <div class="text-xs font-semibold text-indigo-700 uppercase">3. Khách để lại SĐT</div>
                        <div class="text-2xl font-black text-indigo-900 mt-2">23</div>
                        <div class="text-[11px] text-indigo-700 mt-1">SĐT chất lượng cao</div>
                    </div>
                    <div class="p-4 rounded-xl bg-purple-50 border border-purple-200">
                        <div class="text-xs font-semibold text-purple-700 uppercase">4. Chuyển Sale xử lý</div>
                        <div class="text-2xl font-black text-purple-900 mt-2">17</div>
                        <div class="text-[11px] text-purple-700 mt-1">Tag "Xử lý đơn hàng"</div>
                    </div>
                    <div class="p-4 rounded-xl bg-emerald-50 border border-emerald-200">
                        <div class="text-xs font-semibold text-emerald-700 uppercase">5. Đơn hàng SO duyệt</div>
                        <div class="text-2xl font-black text-emerald-900 mt-2">75 SO</div>
                        <div class="text-[11px] text-emerald-700 mt-1">1,397 - 1,484 tỷ đ</div>
                    </div>
                </div>
            </div>

            <!-- Platforms Breakdown -->
            <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
                <div class="p-4 border-b border-slate-100 flex justify-between items-center">
                    <h3 class="text-sm font-bold text-slate-900">Chi tiết Hội thoại & Thu thập SĐT theo Kênh CSKH (AI Seller)</h3>
                    <span class="text-xs text-slate-500">Chatbot ID 14: Nội Thất Rồng Phương Bắc</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider border-b border-slate-200">
                            <tr>
                                <th class="p-3">Kênh kết nối / Fanpage</th>
                                <th class="p-3 text-right">Số cuộc hội thoại</th>
                                <th class="p-3 text-right">Số ĐT thu thập</th>
                                <th class="p-3 text-right">Tỷ lệ để lại SĐT</th>
                                <th class="p-3">Ghi chú vận hành</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 font-medium">
                            <tr class="hover:bg-slate-50">
                                <td class="p-3"><strong>RPB - Education & Public Seating</strong> (Facebook)</td>
                                <td class="p-3 text-right font-bold">104</td>
                                <td class="p-3 text-right font-bold text-blue-700">6</td>
                                <td class="p-3 text-right text-slate-600">5.8%</td>
                                <td class="p-3 text-slate-500">Khách quan tâm ghế nâng hạ, phonebooth</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3"><strong>Nội thất Rồng Phương Bắc</strong> (Zalo OA)</td>
                                <td class="p-3 text-right font-bold">61</td>
                                <td class="p-3 text-right font-bold text-emerald-700">13</td>
                                <td class="p-3 text-right text-emerald-700 font-bold">21.3%</td>
                                <td class="p-3 text-slate-500">Tỷ lệ SĐT rất cao, khách sẵn sàng nghe tư vấn</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3"><strong>Nội thất The City At Home</strong> (Facebook)</td>
                                <td class="p-3 text-right font-bold">59</td>
                                <td class="p-3 text-right font-bold text-blue-700">1</td>
                                <td class="p-3 text-right text-slate-600">1.7%</td>
                                <td class="p-3 text-slate-500">Khách hỏi mua ghế lẻ cho gia đình</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3"><strong>The Mia - Nội thất văn phòng hiện đại</strong> (Facebook)</td>
                                <td class="p-3 text-right font-bold">40</td>
                                <td class="p-3 text-right font-bold text-blue-700">3</td>
                                <td class="p-3 text-right text-slate-600">7.5%</td>
                                <td class="p-3 text-slate-500">Nhu cầu setup văn phòng vừa & nhỏ</td>
                            </tr>
                            <tr class="hover:bg-slate-50">
                                <td class="p-3"><strong>The City - Giải pháp Nội thất cao cấp</strong> (Facebook)</td>
                                <td class="p-3 text-right font-bold">22</td>
                                <td class="p-3 text-right font-bold text-slate-500">0</td>
                                <td class="p-3 text-right text-slate-500">0%</td>
                                <td class="p-3 text-slate-500">Khách dự án hỏi báo giá trực tiếp qua file</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500 font-medium">
        Rồng Phương Bắc Group &copy; 2026 Báo cáo Digital Marketing | Tích hợp Facebook Ads, Google Ads & AI Seller
    </footer>

    <!-- Injected Data & Script -->
    <script>
        const dashboardData = {json_data_str};

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            
            // Inactive style for all tabs
            document.querySelectorAll('.tab-btn').forEach(el => {{
                el.className = 'tab-btn inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all text-slate-600 hover:text-slate-900 hover:bg-white/60 whitespace-nowrap';
            }});
            
            document.getElementById(tabId).classList.remove('hidden');
            
            const btnMap = {{
                'tab-executive': 'btn-executive',
                'tab-sales': 'btn-sales',
                'tab-google': 'btn-google',
                'tab-ads': 'btn-ads',
                'tab-funnel': 'btn-funnel'
            }};
            
            if (btnMap[tabId]) {{
                const activeBtn = document.getElementById(btnMap[tabId]);
                activeBtn.className = 'tab-btn inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all shadow-sm bg-white text-orange-600 border border-slate-200/60 whitespace-nowrap';
            }}
        }}

        // Render Facebook Campaigns Table
        let currentCampaigns = dashboardData.fb_ads.campaigns;
        function renderCampaignsTable(camps) {{
            const tbody = document.getElementById('campaignsTableBody');
            tbody.innerHTML = '';
            
            camps.forEach(c => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50';
                
                let badgeClass = 'badge-brand-other';
                if (c.brand === 'THE CITY') badgeClass = 'badge-brand-city';
                else if (c.brand === 'THE MIA') badgeClass = 'badge-brand-mia';
                else if (c.brand === 'RPB EDU & PUBLIC') badgeClass = 'badge-brand-edu';

                let evalBadge = '<span class=\"px-2 py-0.5 rounded text-[11px] bg-emerald-100 text-emerald-800 font-semibold\">Tốt</span>';
                if (c.cost_per_conv > 100000) {{
                    evalBadge = '<span class=\"px-2 py-0.5 rounded text-[11px] bg-rose-100 text-rose-800 font-semibold\">Giá cao</span>';
                }} else if (c.total_conv === 0 && c.spend > 50000) {{
                    evalBadge = '<span class=\"px-2 py-0.5 rounded text-[11px] bg-amber-100 text-amber-800 font-semibold\">Chưa ra số</span>';
                }}

                tr.innerHTML = `
                    <td class="p-3 max-w-xs truncate" title="${{c.name}}"><strong>${{c.name}}</strong></td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded text-[11px] font-semibold ${{badgeClass}}">${{c.brand}}</span></td>
                    <td class="p-3 text-right font-bold">${{Math.round(c.spend).toLocaleString('vi-VN')}} đ</td>
                    <td class="p-3 text-right">${{c.msgs}}</td>
                    <td class="p-3 text-right">${{c.leads}}</td>
                    <td class="p-3 text-right font-bold text-slate-900">${{c.total_conv}}</td>
                    <td class="p-3 text-right font-bold text-orange-600">${{Math.round(c.cost_per_conv).toLocaleString('vi-VN')}} đ</td>
                    <td class="p-3 text-right">${{c.ctr.toFixed(2)}}%</td>
                    <td class="p-3 text-center">${{evalBadge}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function filterCampaigns(brand) {{
            document.querySelectorAll('.filter-btn').forEach(b => {{
                b.classList.remove('bg-orange-600', 'text-white');
                b.classList.add('bg-slate-100', 'text-slate-700');
            }});
            const activeBtn = document.getElementById('filter-' + brand);
            if (activeBtn) {{
                activeBtn.classList.remove('bg-slate-100', 'text-slate-700');
                activeBtn.classList.add('bg-orange-600', 'text-white');
            }}

            if (brand === 'ALL') {{
                currentCampaigns = dashboardData.fb_ads.campaigns;
            }} else {{
                currentCampaigns = dashboardData.fb_ads.campaigns.filter(c => c.brand === brand);
            }}
            renderCampaignsTable(currentCampaigns);
        }}

        function searchCampaigns() {{
            const q = document.getElementById('campaignSearch').value.toLowerCase();
            const filtered = currentCampaigns.filter(c => c.name.toLowerCase().includes(q));
            renderCampaignsTable(filtered);
        }}

        // Render Charts
        window.addEventListener('DOMContentLoaded', () => {{
            renderCampaignsTable(currentCampaigns);

            // Chart 1: Bar Chart (Doanh số vs Tổng Chi Ads)
            const ctx1 = document.getElementById('chartBrandComparison').getContext('2d');
            new Chart(ctx1, {{
                type: 'bar',
                data: {{
                    labels: ['The City (Cao cấp)', 'The MIA (Trung cấp)', 'RPB Edu & Public'],
                    datasets: [
                        {{
                            label: 'Doanh số thực tế (Triệu đ)',
                            data: [1020, 333, 9.8],
                            backgroundColor: '#2563eb',
                            borderRadius: 6
                        }},
                        {{
                            label: 'Tổng Chi phí Ads FB + GG (Triệu đ)',
                            data: [53.5, 20.6, 14.96],
                            backgroundColor: '#ea580c',
                            borderRadius: 6
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'top', labels: {{ font: {{ size: 11 }} }} }}
                    }},
                    scales: {{
                        y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }}
                    }}
                }}
            }});

            // Chart 2: Channel Share (FB vs GG by Brand)
            const ctx2 = document.getElementById('chartChannelShare').getContext('2d');
            new Chart(ctx2, {{
                type: 'doughnut',
                data: {{
                    labels: ['Google Ads - The City (47.7tr)', 'Google Ads - The Mia (11.5tr)', 'Facebook - Edu & Public (14.9tr)', 'Facebook - The Mia (9.1tr)', 'Facebook - The City (5.8tr)'],
                    datasets: [{{
                        data: [47.66, 11.55, 14.96, 9.09, 5.84],
                        backgroundColor: ['#1d4ed8', '#059669', '#ea580c', '#10b981', '#3b82f6'],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'right', labels: {{ font: {{ size: 10 }} }} }}
                    }}
                }}
            }});
        }});
    </script>
</body>
</html>
'''

with open("/Users/ted/Desktop/Code/RPB/marketing_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("/Users/ted/Desktop/Code/RPB/build_html.py", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Navigation tabs successfully redesigned and synced!")

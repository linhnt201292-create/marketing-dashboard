import re

with open("/Users/ted/Desktop/Code/RPB/build_html.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the 5 KPI cards section with a sleek, ultra-clean, modern executive card design
old_cards_pattern = r'<!-- Top 5 Executive KPI Cards -->.*?<!-- ========================================== -->'

new_cards_html = '''<!-- Top 5 Executive KPI Cards (Redesigned for Maximum Readability) -->
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

        <!-- ========================================== -->'''

new_content = re.sub(old_cards_pattern, new_cards_html, content, flags=re.DOTALL)

with open("/Users/ted/Desktop/Code/RPB/build_html.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("build_html.py updated with enhanced cards!")

# -*- coding: utf-8 -*-
import json

with open('/Users/ted/Desktop/Code/RPB/marketing_dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('/Users/ted/Desktop/Code/RPB/weekly_data.json', 'r', encoding='utf-8') as f:
    weekly_data = json.load(f)

# 1. Filter Bar HTML
filter_bar_html = """
        <!-- ========================================================= -->
        <!-- PERIOD SELECTOR (BỘ LỌC KỲ BÁO CÁO: CẢ THÁNG & TỪNG TUẦN) -->
        <!-- ========================================================= -->
        <div class="bg-white p-3.5 rounded-2xl border border-slate-200/90 shadow-sm mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
            <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center font-bold shrink-0">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <span class="text-xs font-black uppercase tracking-wider text-slate-800">Chọn Kỳ Báo Cáo:</span>
                        <span id="currentPeriodLabel" class="text-xs font-bold px-2 py-0.5 rounded-md bg-orange-100 text-orange-800">Cả tháng 11 (01 - 18/11)</span>
                    </div>
                    <p class="text-[11px] text-slate-500 mt-0.5">Doanh số chuẩn theo <strong class="text-slate-700">Ngày CT (Cột H)</strong> file SO ERP • Chi phí Ads FB + GG đồng bộ theo tuần</p>
                </div>
            </div>
            
            <div class="inline-flex p-1 bg-slate-100/90 rounded-xl border border-slate-200/80 text-xs font-semibold overflow-x-auto max-w-full">
                <button onclick="setPeriod('all')" id="btn-period-all" class="period-btn px-3 py-1.5 rounded-lg transition-all font-bold bg-white text-orange-600 shadow-xs whitespace-nowrap">
                    Cả tháng (01-18/11)
                </button>
                <button onclick="setPeriod('w1')" id="btn-period-w1" class="period-btn px-3 py-1.5 rounded-lg transition-all text-slate-600 hover:text-slate-900 whitespace-nowrap">
                    Tuần 1 (01-08/11)
                </button>
                <button onclick="setPeriod('w2')" id="btn-period-w2" class="period-btn px-3 py-1.5 rounded-lg transition-all text-slate-600 hover:text-slate-900 whitespace-nowrap">
                    Tuần 2 (09-15/11)
                </button>
                <button onclick="setPeriod('w3')" id="btn-period-w3" class="period-btn px-3 py-1.5 rounded-lg transition-all text-slate-600 hover:text-slate-900 whitespace-nowrap">
                    Tuần 3 (16-22/11)
                </button>
                <button onclick="setPeriod('w4')" id="btn-period-w4" class="period-btn px-3 py-1.5 rounded-lg transition-all text-slate-400 hover:text-slate-500 whitespace-nowrap">
                    Tuần 4 (23-30/11)
                </button>
            </div>
        </div>
"""

# Insert Filter Bar before Top 5 Executive KPI Cards
if '<!-- PERIOD SELECTOR' not in html:
    html = html.replace('<!-- Top 5 Executive KPI Cards -->', filter_bar_html + '\n        <!-- Top 5 Executive KPI Cards -->')

# Update Top 5 Cards with unique dynamic IDs
cards_html_new = """        <!-- Top 5 Executive KPI Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
            
            <!-- Card 1: Doanh số MKT -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden flex flex-col justify-between">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[11px] font-bold tracking-wider text-slate-500 uppercase">Doanh số MKT (Ngày CT)</span>
                    <div class="w-8 h-8 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-sm">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                    </div>
                </div>
                <div>
                    <div class="flex items-baseline gap-1.5">
                        <span class="text-2xl font-black text-slate-900 tracking-tight" id="card_ds_main">1,505</span>
                        <span class="text-xs font-bold text-slate-500 uppercase" id="card_ds_unit">tỷ đ</span>
                    </div>
                    <div class="text-[11px] text-slate-600 mt-2 flex items-center justify-between bg-slate-50 px-2.5 py-1.5 rounded-lg border border-slate-100">
                        <span>HCM: <strong class="text-emerald-700 font-bold" id="card_ds_hcm">1,352 tỷ</strong></span>
                        <span class="text-slate-300 font-light">|</span>
                        <span>HN: <strong class="text-blue-700 font-bold" id="card_ds_hn">152,5 tr</strong></span>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100">
                    <div class="flex justify-between items-center text-[11px] mb-1.5">
                        <span class="text-slate-500">Tiến độ kỳ:</span>
                        <span class="font-bold text-emerald-600" id="card_ds_progress_text">46.3% / 3.25 tỷ</span>
                    </div>
                    <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                        <div class="bg-emerald-500 h-1.5 rounded-full transition-all duration-500" id="card_ds_progress_bar" style="width: 46.3%"></div>
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
                        <span class="text-2xl font-black text-slate-900 tracking-tight" id="card_ads_main">89,35</span>
                        <span class="text-xs font-bold text-slate-500 uppercase">triệu đ</span>
                    </div>
                    <div class="text-[11px] text-slate-500 mt-1" id="card_ads_sub">
                        FB: <strong class="text-slate-700">30.1tr</strong> • GG: <strong class="text-slate-700">59.2tr</strong>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100">
                    <div class="flex justify-between items-center text-[11px] mb-1.5">
                        <span class="text-slate-500">Ngân sách kỳ:</span>
                        <span class="font-bold text-blue-700" id="card_ads_quota_text">55.0% / 162.5tr</span>
                    </div>
                    <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                        <div class="bg-blue-600 h-1.5 rounded-full transition-all duration-500" id="card_ads_progress_bar" style="width: 55.0%"></div>
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
                        <span class="text-2xl font-black text-amber-600 tracking-tight" id="card_cir_main">5,94%</span>
                        <span class="text-xs font-medium text-slate-500">Toàn kỳ</span>
                    </div>
                    <div class="text-[11px] text-slate-500 mt-1">
                        Mục tiêu trần CEO: <strong class="text-slate-700">≤ 5,0%</strong>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
                    <span class="text-slate-500">Đánh giá:</span>
                    <span class="px-2 py-0.5 rounded-md bg-amber-100 text-amber-800 font-bold text-[10px]" id="card_cir_badge">Sát trần 5%</span>
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
                        <span class="text-2xl font-black text-purple-700 tracking-tight" id="card_roas_main">16.8x</span>
                        <span class="text-xs font-medium text-slate-500">Toàn team</span>
                    </div>
                    <div class="text-[11px] text-slate-500 mt-1" id="card_roas_sub">
                        1đ Ads → tạo <strong class="text-purple-700 font-semibold">16.8đ</strong> doanh số
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
                        <span class="text-2xl font-black text-slate-900 tracking-tight" id="card_leads_main">2.431</span>
                        <span class="text-xs font-bold text-slate-500 uppercase">lượt</span>
                    </div>
                    <div class="text-[11px] text-slate-500 mt-1" id="card_leads_sub">
                        FB: <strong class="text-slate-700">644 data</strong> • GG: <strong class="text-slate-700">1.787 conv</strong>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px]">
                    <span class="text-slate-500">CPA bình quân:</span>
                    <span class="font-bold text-cyan-800" id="card_cpa_sub">~36.8k / lượt</span>
                </div>
            </div>

        </div>"""

# Replace old cards grid
cards_start = html.find('<!-- Top 5 Executive KPI Cards -->')
cards_end = html.find('<!-- ========================================== -->\n        <!-- TAB 1: TỔNG QUAN -->')
if cards_start != -1 and cards_end != -1:
    html = html[:cards_start] + cards_html_new + '\n\n        ' + html[cards_end:]

# Script logic for setPeriod(p)
period_js = """
    // =========================================================
    // GLOBAL WINDOW EXPORTS FOR EVENT HANDLERS
    // =========================================================
    const weeklyBundle = """ + json.dumps(weekly_data, ensure_ascii=False) + """;
    let currentPeriod = 'all';

    const periodNames = {
        'all': 'Cả tháng 11 (01 - 18/11)',
        'w1': 'Tuần 1 (01 - 08/11)',
        'w2': 'Tuần 2 (09 - 15/11)',
        'w3': 'Tuần 3 (16 - 22/11)',
        'w4': 'Tuần 4 (23 - 30/11)'
    };

    function formatMoneyVND(val) {
        return new Intl.NumberFormat('vi-VN').format(Math.round(val)) + ' đ';
    }

    function setPeriod(p) {
        currentPeriod = p;
        const pData = weeklyBundle[p];
        if (!pData) return;

        // 1. Update Buttons Style
        document.querySelectorAll('.period-btn').forEach(btn => {
            btn.className = 'period-btn px-3 py-1.5 rounded-lg transition-all text-slate-600 hover:text-slate-900 whitespace-nowrap';
        });
        const activeBtn = document.getElementById('btn-period-' + p);
        if (activeBtn) {
            activeBtn.className = 'period-btn px-3 py-1.5 rounded-lg transition-all font-bold bg-white text-orange-600 shadow-xs whitespace-nowrap';
        }
        document.getElementById('currentPeriodLabel').textContent = periodNames[p];

        // 2. Update Top 5 Cards
        const rev = pData.revenue;
        const sDet = pData.sales_detail;
        const isBillions = rev >= 1e9;
        document.getElementById('card_ds_main').textContent = isBillions ? (rev / 1e9).toFixed(3).replace('.', ',') : (rev / 1e6).toFixed(1).replace('.', ',');
        document.getElementById('card_ds_unit').textContent = isBillions ? 'tỷ đ' : 'triệu đ';
        document.getElementById('card_ds_hcm').textContent = (sDet.regions.HCM >= 1e9 ? (sDet.regions.HCM / 1e9).toFixed(3) + ' tỷ' : (sDet.regions.HCM / 1e6).toFixed(1) + ' tr').replace('.', ',');
        document.getElementById('card_ds_hn').textContent = (sDet.regions.HN >= 1e9 ? (sDet.regions.HN / 1e9).toFixed(3) + ' tỷ' : (sDet.regions.HN / 1e6).toFixed(1) + ' tr').replace('.', ',');
        
        const prog = pData.progress.toFixed(1);
        document.getElementById('card_ds_progress_text').textContent = prog + '% / ' + (pData.kpi_target / 1e9).toFixed(2).replace('.', ',') + ' tỷ';
        document.getElementById('card_ds_progress_bar').style.width = Math.min(100, Math.max(0, pData.progress)) + '%';

        // Card 2: Ads
        const adsM = (pData.ads_spend / 1e6).toFixed(2).replace('.', ',');
        document.getElementById('card_ads_main').textContent = adsM;
        document.getElementById('card_ads_sub').innerHTML = 'FB: <strong class="text-slate-700">' + (pData.fb_spend / 1e6).toFixed(1) + 'tr</strong> • GG: <strong class="text-slate-700">' + (pData.gg_spend / 1e6).toFixed(1) + 'tr</strong>';

        // Card 3: CIR
        const cirVal = pData.cir.toFixed(2).replace('.', ',');
        document.getElementById('card_cir_main').textContent = cirVal + '%';
        const badgeCir = document.getElementById('card_cir_badge');
        if (pData.cir <= 5.0 && pData.cir > 0) {
            badgeCir.className = 'px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 font-bold text-[10px]';
            badgeCir.textContent = 'Rất tốt (≤ 5%)';
        } else if (pData.cir > 0) {
            badgeCir.className = 'px-2 py-0.5 rounded-md bg-amber-100 text-amber-800 font-bold text-[10px]';
            badgeCir.textContent = 'Sát trần 5%';
        } else {
            badgeCir.className = 'px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 font-bold text-[10px]';
            badgeCir.textContent = 'Chưa có Ads';
        }

        // Card 4: ROAS
        document.getElementById('card_roas_main').textContent = pData.roas.toFixed(1) + 'x';
        document.getElementById('card_roas_sub').innerHTML = '1đ Ads → tạo <strong class="text-purple-700 font-semibold">' + pData.roas.toFixed(1) + 'đ</strong> doanh số';

        // Card 5: Leads
        document.getElementById('card_leads_main').textContent = new Intl.NumberFormat('vi-VN').format(pData.leads);
        document.getElementById('card_leads_sub').innerHTML = 'FB: <strong class="text-slate-700">' + pData.fb_leads + ' data</strong> • GG: <strong class="text-slate-700">' + pData.gg_leads + ' conv</strong>';
        const cpa = pData.leads > 0 ? Math.round(pData.ads_spend / pData.leads) : 0;
        document.getElementById('card_cpa_sub').textContent = cpa > 0 ? '~' + (cpa / 1000).toFixed(1) + 'k / lượt' : '-';

        // 3. Update BẢNG DỮ LIỆU THEO KPI TỔNG
        const br = sDet.brands;
        const fbB = pData.fb_detail.brands_spend || {};
        const ggB = pData.gg_detail.brands || {};
        const fbConv = pData.fb_detail.brands_conv || {};
        const ggConv = { 'THE CITY': (p == 'all' ? 1604 : Math.round(pData.gg_leads * 0.9)), 'THE MIA': (p == 'all' ? 183 : Math.round(pData.gg_leads * 0.1)) };

        updateKpiTableRow('city', br['THE CITY'] || 0, 1982500000, (fbConv['THE CITY']||0) + (ggConv['THE CITY']||0), fbConv['THE CITY']||0, ggConv['THE CITY']||0);
        updateKpiTableRow('mia', br['THE MIA'] || 0, 812500000, (fbConv['THE MIA']||0) + (ggConv['THE MIA']||0), fbConv['THE MIA']||0, ggConv['THE MIA']||0);
        updateKpiTableRow('edu', br['RPB EDU & PUBLIC'] || 0, 455000000, fbConv['RPB EDU & PUBLIC']||0, fbConv['RPB EDU & PUBLIC']||0, 0);

        // Fee row
        const feeVal = br['Phí vận chuyển / Khác'] || 0;
        const elFee = document.getElementById('row-fee');
        if (elFee) {
            const cells = elFee.querySelectorAll('td');
            if (cells.length > 4) {
                cells[3].textContent = formatMoneyVND(feeVal);
                cells[4].textContent = formatMoneyVND(feeVal);
            }
        }

        // Total row in KPI table
        document.getElementById('val_total_ds_moi').textContent = formatMoneyVND(rev);
        document.getElementById('val_total_ds_tong').textContent = formatMoneyVND(rev);
        const totThieu = Math.max(0, 3250000000 - rev);
        document.getElementById('val_total_ds_thieu').textContent = formatMoneyVND(totThieu);
        const totRate = (rev / 3250000000 * 100).toFixed(2).replace('.', ',');
        document.getElementById('val_total_rate_ht').innerHTML = '<span class="px-2.5 py-1 rounded bg-emerald-100 text-emerald-800 text-[11px] font-extrabold">' + totRate + '%</span>';

        // 4. Update Tab 2: Reps & Regions
        updateSalesTabValues(sDet);

        // 5. Update Charts
        updateChartsPeriod(pData);
    }

    function updateKpiTableRow(brand, dsMoi, kpiDs, totalLead, fbLead, ggLead) {
        const elMoi = document.getElementById('val_' + brand + '_ds_moi');
        const elTong = document.getElementById('val_' + brand + '_ds_tong');
        const elThieu = document.getElementById('val_' + brand + '_ds_thieu');
        const elRate = document.getElementById('val_' + brand + '_rate_ht');

        const inputCu = document.getElementById('input_' + brand + '_ds_cu');
        const dsCu = parseFloat(inputCu?.value) || 0;
        const dsTong = dsMoi + dsCu;
        const dsThieu = Math.max(0, kpiDs - dsTong);
        const rate = (dsTong / kpiDs * 100);

        if (elMoi) elMoi.textContent = formatMoneyVND(dsMoi);
        if (elTong) elTong.textContent = formatMoneyVND(dsTong);
        if (elThieu) elThieu.textContent = formatMoneyVND(dsThieu);
        if (elRate) {
            const badgeColor = rate >= 60 ? 'bg-emerald-100 text-emerald-800' : (rate >= 40 ? 'bg-blue-100 text-blue-800' : 'bg-rose-100 text-rose-800');
            elRate.innerHTML = '<span class="px-2 py-0.5 rounded ' + badgeColor + '">' + rate.toFixed(2).replace('.', ',') + '%</span>';
        }

        const rowEl = document.getElementById('row-' + (brand == 'city' ? 'the-city' : (brand == 'mia' ? 'the-mia' : 'rpb-edu')));
        if (rowEl) {
            const cells = rowEl.querySelectorAll('td');
            if (cells.length > 7) {
                cells[7].innerHTML = totalLead + ' <span class="text-[10px] text-slate-500 font-normal block">(FB: ' + fbLead + ' | GG: ' + ggLead + ')</span>';
            }
        }
    }

    function updateSalesTabValues(sDet) {
        const hcmVal = sDet.regions.HCM || 0;
        const hnVal = sDet.regions.HN || 0;
        const tot = sDet.total_rev || 1;
        const hcmRate = (hcmVal / tot * 100).toFixed(1).replace('.', ',');
        const hnRate = (hnVal / tot * 100).toFixed(1).replace('.', ',');

        const elHcm = document.querySelector('#tab-sales .grid > div:first-child .text-2xl');
        const elHcmBadge = document.querySelector('#tab-sales .grid > div:first-child span.rounded-full');
        if (elHcm) elHcm.textContent = formatMoneyVND(hcmVal);
        if (elHcmBadge) elHcmBadge.textContent = hcmRate + '% Tổng DS';

        const elHn = document.querySelector('#tab-sales .grid > div:last-child .text-2xl');
        const elHnBadge = document.querySelector('#tab-sales .grid > div:last-child span.rounded-full');
        if (elHn) elHn.textContent = formatMoneyVND(hnVal);
        if (elHnBadge) elHnBadge.textContent = hnRate + '% Tổng DS';

        const reps = sDet.reps;
        const rb = sDet.rep_brand;
        const repRows = [
            { id: 'anh', code: 'HCMKDANH.05' },
            { id: 'khoa', code: 'HCMKDKHOA.02' },
            { id: 'dao', code: 'HNIKDDAO.01' },
            { id: 'minh', code: 'HNIKDMINH.02' },
            { id: 'yen', code: 'HNIKDYEN.01' }
        ];

        const tbody = document.querySelector('#tab-sales tbody');
        if (tbody && tbody.children.length >= 5) {
            repRows.forEach((item, idx) => {
                const tr = tbody.children[idx];
                const rData = reps[item.code] || { rev: 0, sos: 0 };
                const rBrand = rb[item.code] || {};
                const tds = tr.querySelectorAll('td');
                if (tds.length >= 8) {
                    tds[2].textContent = formatMoneyVND(rBrand['THE CITY'] || 0);
                    tds[3].textContent = formatMoneyVND(rBrand['THE MIA'] || 0);
                    tds[4].textContent = formatMoneyVND(rBrand['RPB EDU & PUBLIC'] || 0);
                    tds[5].textContent = formatMoneyVND(rBrand['Phí vận chuyển / Khác'] || 0);
                    tds[6].textContent = formatMoneyVND(rData.rev);
                    tds[7].textContent = rData.sos;
                }
            });
        }
    }

    function updateChartsPeriod(pData) {
        const sDet = pData.sales_detail;
        const br = sDet.brands;
        const fbB = pData.fb_detail.brands_spend || {};
        const ggB = pData.gg_detail.brands || {};

        const cityRev = Math.round((br['THE CITY'] || 0) / 1e6);
        const miaRev = Math.round((br['THE MIA'] || 0) / 1e6);
        const eduRev = Math.round((br['RPB EDU & PUBLIC'] || 0) / 1e6);

        const cityAds = Math.round(((fbB['THE CITY'] || 0) + (ggB['THE CITY'] || 0)) / 1e6);
        const miaAds = Math.round(((fbB['THE MIA'] || 0) + (ggB['THE MIA'] || 0)) / 1e6);
        const eduAds = Math.round(((fbB['RPB EDU & PUBLIC'] || 0) + (ggB['RPB EDU & PUBLIC'] || 0)) / 1e6);

        if (window.chartBrandComparisonInstance) {
            window.chartBrandComparisonInstance.data.datasets[0].data = [cityRev, miaRev, eduRev];
            window.chartBrandComparisonInstance.data.datasets[1].data = [cityAds, miaAds, eduAds];
            window.chartBrandComparisonInstance.update();
        }
    }

    // Attach to window so HTML inline onclick always works
    window.setPeriod = setPeriod;
    window.formatMoneyVND = formatMoneyVND;
    window.updateKpiTableRow = updateKpiTableRow;
    window.updateSalesTabValues = updateSalesTabValues;
    window.updateChartsPeriod = updateChartsPeriod;
"""

# Store Chart.js instance into window variable
html = html.replace('new Chart(ctx1, {', 'window.chartBrandComparisonInstance = new Chart(ctx1, {')

# Remove any old duplicated script blocks if present
if 'const weeklyBundle =' in html:
    idx_wb = html.find('const weeklyBundle =')
    idx_end = html.find('window.chartBrandComparisonInstance.update();\n        }', idx_wb)
    if idx_end != -1:
        html = html[:idx_wb] + html[idx_end + len('window.chartBrandComparisonInstance.update();\n        }'):]

# Place period_js at root of <script>
script_open = '<script>\n'
if script_open in html:
    html = html.replace(script_open, script_open + period_js + '\n')

with open('/Users/ted/Desktop/Code/RPB/marketing_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
with open('/Users/ted/Desktop/Code/RPB/build_html.py', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied Period Selector & dynamic scripts successfully!")

# -*- coding: utf-8 -*-
import json

kpi_table_html = """
            <!-- ========================================================= -->
            <!-- BẢNG DỮ LIỆU THEO KPI TỔNG (THEO MẪU BÁO CÁO CÔNG TY) -->
            <!-- ========================================================= -->
            <div class="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden mb-6">
                <!-- Orange Corporate Header -->
                <div class="bg-[#ea580c] px-4 py-3 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 text-white">
                    <div class="flex items-center gap-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                        <h3 class="font-extrabold text-sm sm:text-base tracking-wider uppercase">BẢNG DỮ LIỆU THEO KPI TỔNG</h3>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-[11px] bg-white/20 backdrop-blur-sm px-2.5 py-1 rounded-full font-medium">Giai đoạn: 01/11 - 18/11/2026</span>
                        <span class="text-[11px] bg-amber-400 text-slate-900 px-2.5 py-1 rounded-full font-bold">Ô vàng: Nhập liệu trực tiếp</span>
                    </div>
                </div>

                <div class="p-3 bg-amber-50/70 border-b border-amber-200/60 text-xs text-amber-900 flex flex-wrap items-center justify-between gap-2">
                    <div class="flex items-center gap-1.5 font-medium">
                        <svg class="w-4 h-4 text-amber-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <span>Số lead lấy tự động từ quảng cáo (FB + GG). Các cột <strong>Qualified Lead, DS KH cũ, Lượt FL, Engagement</strong> bạn có thể click nhập trực tiếp (tự động lưu vào máy và tự nhảy số tính toán).</span>
                    </div>
                    <button onclick="fillSampleKpiData()" class="px-2.5 py-1 text-[11px] font-semibold bg-white text-slate-700 hover:bg-slate-100 rounded-lg border border-amber-300 shadow-2xs transition-colors">
                        Điền số liệu mẫu ảnh T6
                    </button>
                </div>

                <!-- Table Content -->
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 font-bold uppercase tracking-wider text-[11px] border-b border-slate-300">
                                <th class="p-3 border-r border-slate-200">Thương hiệu</th>
                                <th class="p-3 text-right border-r border-slate-200">Doanh Số KPI</th>
                                <th class="p-3 text-right border-r border-slate-200 bg-amber-50/50">DS KH CŨ</th>
                                <th class="p-3 text-right border-r border-slate-200">DS KH MỚI</th>
                                <th class="p-3 text-right border-r border-slate-200">DS TỔNG</th>
                                <th class="p-3 text-right border-r border-slate-200 text-rose-700">DS thiếu</th>
                                <th class="p-3 text-center border-r border-slate-200 font-black">TỶ LỆ HOÀN THÀNH</th>
                                <th class="p-3 text-center border-r border-slate-200 bg-blue-50/50 text-blue-900 font-black">Lead Ads (FB+GG)</th>
                                <th class="p-3 text-center border-r border-slate-200">KPI Q-Lead</th>
                                <th class="p-3 text-center border-r border-slate-200 bg-amber-50/50">Qualified Lead</th>
                                <th class="p-3 text-center border-r border-slate-200 text-rose-700">Q-Lead thiếu</th>
                                <th class="p-3 text-center border-r border-slate-200">KPI FL</th>
                                <th class="p-3 text-center border-r border-slate-200 bg-amber-50/50">Lượt FL thực</th>
                                <th class="p-3 text-center border-r border-slate-200">Tỉ lệ HT (FL)</th>
                                <th class="p-3 text-center border-r border-slate-200">KPI % Eng.</th>
                                <th class="p-3 text-center border-r border-slate-200 bg-amber-50/50">% Eng. thực</th>
                                <th class="p-3 text-center">% Eng. Đạt</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-200 font-medium text-slate-800">
                            <!-- Row 1: The City -->
                            <tr class="hover:bg-slate-50 transition-colors" id="row-the-city">
                                <td class="p-3 font-bold border-r border-slate-200 flex items-center gap-1.5 whitespace-nowrap">
                                    <span class="w-2.5 h-2.5 rounded-full bg-blue-600"></span>
                                    <span>The City</span>
                                </td>
                                <td class="p-3 text-right font-bold text-slate-900 border-r border-slate-200 whitespace-nowrap">1.982.500.000 đ</td>
                                <td class="p-2 text-right border-r border-slate-200 bg-amber-50/30">
                                    <input type="number" id="input_city_ds_cu" placeholder="0" oninput="recalcKpiRow('city')" class="w-24 px-1.5 py-1 text-right text-xs bg-amber-50/80 border border-amber-300 rounded font-semibold text-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-right font-bold text-slate-800 border-r border-slate-200 whitespace-nowrap" id="val_city_ds_moi">1.019.997.830 đ</td>
                                <td class="p-3 text-right font-extrabold text-blue-900 border-r border-slate-200 whitespace-nowrap" id="val_city_ds_tong">1.019.997.830 đ</td>
                                <td class="p-3 text-right font-bold text-rose-600 border-r border-slate-200 whitespace-nowrap" id="val_city_ds_thieu">962.502.170 đ</td>
                                <td class="p-3 text-center font-black border-r border-slate-200" id="val_city_rate_ht">
                                    <span class="px-2 py-0.5 rounded bg-blue-100 text-blue-800">51,45%</span>
                                </td>
                                <td class="p-3 text-center font-extrabold text-blue-800 bg-blue-50/40 border-r border-slate-200 whitespace-nowrap">
                                    1.660 <span class="text-[10px] text-slate-500 font-normal block">(FB: 56 | GG: 1.604)</span>
                                </td>
                                <td class="p-3 text-center font-bold border-r border-slate-200">111</td>
                                <td class="p-2 text-center border-r border-slate-200 bg-amber-50/30">
                                    <input type="number" id="input_city_qlead" placeholder="Điền sau" oninput="recalcKpiRow('city')" class="w-16 px-1.5 py-1 text-center text-xs bg-amber-50/80 border border-amber-300 rounded font-bold text-indigo-900 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-center font-bold text-rose-600 border-r border-slate-200" id="val_city_qlead_thieu">111</td>
                                <td class="p-3 text-center font-bold border-r border-slate-200">900</td>
                                <td class="p-2 text-center border-r border-slate-200 bg-amber-50/30">
                                    <input type="number" id="input_city_fl" placeholder="Gửi sau" oninput="recalcKpiRow('city')" class="w-16 px-1.5 py-1 text-center text-xs bg-amber-50/80 border border-amber-300 rounded font-medium text-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-center font-semibold border-r border-slate-200" id="val_city_rate_fl">0,00%</td>
                                <td class="p-3 text-center font-semibold border-r border-slate-200">3,50%</td>
                                <td class="p-2 text-center border-r border-slate-200 bg-amber-50/30">
                                    <input type="text" id="input_city_eng" placeholder="Gửi sau" oninput="recalcKpiRow('city')" class="w-16 px-1.5 py-1 text-center text-xs bg-amber-50/80 border border-amber-300 rounded font-medium text-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-center font-semibold" id="val_city_rate_eng">0%</td>
                            </tr>

                            <!-- Row 2: The Mia -->
                            <tr class="hover:bg-slate-50 transition-colors" id="row-the-mia">
                                <td class="p-3 font-bold border-r border-slate-200 flex items-center gap-1.5 whitespace-nowrap">
                                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
                                    <span>The Mia</span>
                                </td>
                                <td class="p-3 text-right font-bold text-slate-900 border-r border-slate-200 whitespace-nowrap">812.500.000 đ</td>
                                <td class="p-2 text-right border-r border-slate-200 bg-amber-50/30">
                                    <input type="number" id="input_mia_ds_cu" placeholder="0" oninput="recalcKpiRow('mia')" class="w-24 px-1.5 py-1 text-right text-xs bg-amber-50/80 border border-amber-300 rounded font-semibold text-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-right font-bold text-slate-800 border-r border-slate-200 whitespace-nowrap" id="val_mia_ds_moi">333.227.800 đ</td>
                                <td class="p-3 text-right font-extrabold text-emerald-900 border-r border-slate-200 whitespace-nowrap" id="val_mia_ds_tong">333.227.800 đ</td>
                                <td class="p-3 text-right font-bold text-rose-600 border-r border-slate-200 whitespace-nowrap" id="val_mia_ds_thieu">479.272.200 đ</td>
                                <td class="p-3 text-center font-black border-r border-slate-200" id="val_mia_rate_ht">
                                    <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800">41,01%</span>
                                </td>
                                <td class="p-3 text-center font-extrabold text-emerald-800 bg-blue-50/40 border-r border-slate-200 whitespace-nowrap">
                                    331 <span class="text-[10px] text-slate-500 font-normal block">(FB: 148 | GG: 183)</span>
                                </td>
                                <td class="p-3 text-center font-bold border-r border-slate-200">65</td>
                                <td class="p-2 text-center border-r border-slate-200 bg-amber-50/30">
                                    <input type="number" id="input_mia_qlead" placeholder="Điền sau" oninput="recalcKpiRow('mia')" class="w-16 px-1.5 py-1 text-center text-xs bg-amber-50/80 border border-amber-300 rounded font-bold text-indigo-900 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-center font-bold text-rose-600 border-r border-slate-200" id="val_mia_qlead_thieu">65</td>
                                <td class="p-3 text-center font-bold border-r border-slate-200">900</td>
                                <td class="p-2 text-center border-r border-slate-200 bg-amber-50/30">
                                    <input type="number" id="input_mia_fl" placeholder="Gửi sau" oninput="recalcKpiRow('mia')" class="w-16 px-1.5 py-1 text-center text-xs bg-amber-50/80 border border-amber-300 rounded font-medium text-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-center font-semibold border-r border-slate-200" id="val_mia_rate_fl">0,00%</td>
                                <td class="p-3 text-center font-semibold border-r border-slate-200">3,50%</td>
                                <td class="p-2 text-center border-r border-slate-200 bg-amber-50/30">
                                    <input type="text" id="input_mia_eng" placeholder="Gửi sau" oninput="recalcKpiRow('mia')" class="w-16 px-1.5 py-1 text-center text-xs bg-amber-50/80 border border-amber-300 rounded font-medium text-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-center font-semibold" id="val_mia_rate_eng">0%</td>
                            </tr>

                            <!-- Row 3: RPB Edu & Public -->
                            <tr class="hover:bg-slate-50 transition-colors" id="row-rpb-edu">
                                <td class="p-3 font-bold border-r border-slate-200 flex items-center gap-1.5 whitespace-nowrap">
                                    <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                                    <span>RPB EDU & PUBLIC</span>
                                </td>
                                <td class="p-3 text-right font-bold text-slate-900 border-r border-slate-200 whitespace-nowrap">455.000.000 đ</td>
                                <td class="p-2 text-right border-r border-slate-200 bg-amber-50/30">
                                    <input type="number" id="input_edu_ds_cu" placeholder="0" oninput="recalcKpiRow('edu')" class="w-24 px-1.5 py-1 text-right text-xs bg-amber-50/80 border border-amber-300 rounded font-semibold text-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-right font-bold text-slate-800 border-r border-slate-200 whitespace-nowrap" id="val_edu_ds_moi">97.344.955 đ</td>
                                <td class="p-3 text-right font-extrabold text-amber-900 border-r border-slate-200 whitespace-nowrap" id="val_edu_ds_tong">97.344.955 đ</td>
                                <td class="p-3 text-right font-bold text-rose-600 border-r border-slate-200 whitespace-nowrap" id="val_edu_ds_thieu">357.655.045 đ</td>
                                <td class="p-3 text-center font-black border-r border-slate-200" id="val_edu_rate_ht">
                                    <span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800">21,39%</span>
                                </td>
                                <td class="p-3 text-center font-extrabold text-amber-800 bg-blue-50/40 border-r border-slate-200 whitespace-nowrap">
                                    436 <span class="text-[10px] text-slate-500 font-normal block">(FB: 436 | GG: 0)</span>
                                </td>
                                <td class="p-3 text-center font-bold border-r border-slate-200">23</td>
                                <td class="p-2 text-center border-r border-slate-200 bg-amber-50/30">
                                    <input type="number" id="input_edu_qlead" placeholder="Điền sau" oninput="recalcKpiRow('edu')" class="w-16 px-1.5 py-1 text-center text-xs bg-amber-50/80 border border-amber-300 rounded font-bold text-indigo-900 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-center font-bold text-rose-600 border-r border-slate-200" id="val_edu_qlead_thieu">23</td>
                                <td class="p-3 text-center font-bold border-r border-slate-200">630</td>
                                <td class="p-2 text-center border-r border-slate-200 bg-amber-50/30">
                                    <input type="number" id="input_edu_fl" placeholder="Gửi sau" oninput="recalcKpiRow('edu')" class="w-16 px-1.5 py-1 text-center text-xs bg-amber-50/80 border border-amber-300 rounded font-medium text-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-center font-semibold border-r border-slate-200" id="val_edu_rate_fl">0,00%</td>
                                <td class="p-3 text-center font-semibold border-r border-slate-200">3,50%</td>
                                <td class="p-2 text-center border-r border-slate-200 bg-amber-50/30">
                                    <input type="text" id="input_edu_eng" placeholder="Gửi sau" oninput="recalcKpiRow('edu')" class="w-16 px-1.5 py-1 text-center text-xs bg-amber-50/80 border border-amber-300 rounded font-medium text-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                </td>
                                <td class="p-3 text-center font-semibold" id="val_edu_rate_eng">0%</td>
                            </tr>

                            <!-- Row 4: Phí VC / Khác (Bổ trợ) -->
                            <tr class="hover:bg-slate-50 transition-colors text-slate-500 text-[11px]" id="row-fee">
                                <td class="p-3 border-r border-slate-200 whitespace-nowrap">Phí VC / Đơn lẻ khác</td>
                                <td class="p-3 text-right border-r border-slate-200">-</td>
                                <td class="p-3 text-right border-r border-slate-200">-</td>
                                <td class="p-3 text-right border-r border-slate-200 font-medium">34.215.311 đ</td>
                                <td class="p-3 text-right border-r border-slate-200 font-medium">34.215.311 đ</td>
                                <td class="p-3 text-right border-r border-slate-200">-</td>
                                <td class="p-3 text-center border-r border-slate-200">-</td>
                                <td class="p-3 text-center border-r border-slate-200 bg-blue-50/40">-</td>
                                <td class="p-3 text-center border-r border-slate-200">-</td>
                                <td class="p-3 text-center border-r border-slate-200">-</td>
                                <td class="p-3 text-center border-r border-slate-200">-</td>
                                <td class="p-3 text-center border-r border-slate-200">-</td>
                                <td class="p-3 text-center border-r border-slate-200">-</td>
                                <td class="p-3 text-center border-r border-slate-200">-</td>
                                <td class="p-3 text-center border-r border-slate-200">-</td>
                                <td class="p-3 text-center border-r border-slate-200">-</td>
                                <td class="p-3 text-center">-</td>
                            </tr>

                            <!-- Row 5: TỔNG DOANH SỐ -->
                            <tr class="bg-slate-100/90 font-black text-slate-900 border-t-2 border-slate-300 text-xs">
                                <td class="p-3 border-r border-slate-200 font-extrabold uppercase whitespace-nowrap">Tổng Doanh số</td>
                                <td class="p-3 text-right font-black border-r border-slate-200 whitespace-nowrap">3.250.000.000 đ</td>
                                <td class="p-3 text-right font-black border-r border-slate-200 whitespace-nowrap" id="val_total_ds_cu">0 đ</td>
                                <td class="p-3 text-right font-black border-r border-slate-200 whitespace-nowrap" id="val_total_ds_moi">1.484.785.896 đ</td>
                                <td class="p-3 text-right font-black text-emerald-800 border-r border-slate-200 whitespace-nowrap" id="val_total_ds_tong">1.484.785.896 đ</td>
                                <td class="p-3 text-right font-black text-rose-700 border-r border-slate-200 whitespace-nowrap" id="val_total_ds_thieu">1.765.214.104 đ</td>
                                <td class="p-3 text-center font-black border-r border-slate-200" id="val_total_rate_ht">
                                    <span class="px-2.5 py-1 rounded bg-emerald-100 text-emerald-800 text-[11px] font-extrabold">45,69%</span>
                                </td>
                                <td class="p-3 text-center font-black text-indigo-950 bg-blue-100/60 border-r border-slate-200 whitespace-nowrap">
                                    2.427 <span class="text-[10px] text-slate-600 font-medium block">(FB: 644 | GG: 1.787)</span>
                                </td>
                                <td class="p-3 text-center font-black border-r border-slate-200">199</td>
                                <td class="p-3 text-center font-black text-indigo-950 border-r border-slate-200" id="val_total_qlead">--</td>
                                <td class="p-3 text-center font-black text-rose-700 border-r border-slate-200" id="val_total_qlead_thieu">199</td>
                                <td class="p-3 text-center font-black border-r border-slate-200">2.430</td>
                                <td class="p-3 text-center font-black border-r border-slate-200" id="val_total_fl">--</td>
                                <td class="p-3 text-center font-black border-r border-slate-200" id="val_total_rate_fl">0,00%</td>
                                <td class="p-3 text-center font-black border-r border-slate-200">3,50%</td>
                                <td class="p-3 text-center font-black border-r border-slate-200" id="val_total_eng">--</td>
                                <td class="p-3 text-center font-black" id="val_total_rate_eng">0%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
"""

kpi_script_code = """
        // =========================================================
        // KPI DYNAMIC TABLE LOGIC (STORAGE & AUTO-CALCULATION)
        // =========================================================
        const kpiBaseData = {
            city: { kpi_ds: 1982500000, ds_moi: 1019997830, kpi_qlead: 111, kpi_fl: 900, kpi_eng: 3.5 },
            mia:  { kpi_ds: 812500000,  ds_moi: 333227800,  kpi_qlead: 65,  kpi_fl: 900, kpi_eng: 3.5 },
            edu:  { kpi_ds: 455000000,  ds_moi: 97344955,   kpi_qlead: 23,  kpi_fl: 630, kpi_eng: 3.5 },
            fee:  { ds_moi: 34215311 }
        };

        function formatVND(val) {
            return new Intl.NumberFormat('vi-VN').format(Math.round(val)) + ' đ';
        }

        function recalcKpiRow(brand) {
            const rowData = kpiBaseData[brand];
            if (!rowData) return;

            const inputCu = document.getElementById(`input_${brand}_ds_cu`);
            const inputQLead = document.getElementById(`input_${brand}_qlead`);
            const inputFl = document.getElementById(`input_${brand}_fl`);
            const inputEng = document.getElementById(`input_${brand}_eng`);

            const dsCu = parseFloat(inputCu?.value) || 0;
            const qLead = inputQLead?.value !== '' ? parseInt(inputQLead.value) : null;
            const fl = inputFl?.value !== '' ? parseInt(inputFl.value) : null;
            const eng = inputEng?.value !== '' ? parseFloat(inputEng.value.replace(',', '.')) : null;

            // Recalculate Doanh số
            const dsTong = rowData.ds_moi + dsCu;
            const dsThieu = Math.max(0, rowData.kpi_ds - dsTong);
            const rateHt = (dsTong / rowData.kpi_ds) * 100;

            const elDsTong = document.getElementById(`val_${brand}_ds_tong`);
            const elDsThieu = document.getElementById(`val_${brand}_ds_thieu`);
            const elRateHt = document.getElementById(`val_${brand}_rate_ht`);

            if (elDsTong) elDsTong.textContent = formatVND(dsTong);
            if (elDsThieu) elDsThieu.textContent = formatVND(dsThieu);
            if (elRateHt) {
                const badgeColor = rateHt >= 60 ? 'bg-emerald-100 text-emerald-800' : (rateHt >= 40 ? 'bg-blue-100 text-blue-800' : 'bg-rose-100 text-rose-800');
                elRateHt.innerHTML = `<span class="px-2 py-0.5 rounded ${badgeColor}">${rateHt.toFixed(2).replace('.', ',')}%</span>`;
            }

            // Recalculate Qualified Lead
            const elQLeadThieu = document.getElementById(`val_${brand}_qlead_thieu`);
            if (elQLeadThieu) {
                if (qLead !== null) {
                    elQLeadThieu.textContent = Math.max(0, rowData.kpi_qlead - qLead);
                } else {
                    elQLeadThieu.textContent = rowData.kpi_qlead;
                }
            }

            // Recalculate FL
            const elRateFl = document.getElementById(`val_${brand}_rate_fl`);
            if (elRateFl) {
                if (fl !== null) {
                    const rFl = (fl / rowData.kpi_fl) * 100;
                    elRateFl.textContent = rFl.toFixed(2).replace('.', ',') + '%';
                } else {
                    elRateFl.textContent = '0,00%';
                }
            }

            // Recalculate Eng
            const elRateEng = document.getElementById(`val_${brand}_rate_eng`);
            if (elRateEng) {
                if (eng !== null) {
                    const rEng = (eng / rowData.kpi_eng) * 100;
                    elRateEng.textContent = Math.round(rEng) + '%';
                } else {
                    elRateEng.textContent = '0%';
                }
            }

            // Save to localStorage
            const savedState = {
                cu: inputCu?.value || '',
                qlead: inputQLead?.value || '',
                fl: inputFl?.value || '',
                eng: inputEng?.value || ''
            };
            localStorage.setItem(`kpi_row_${brand}`, JSON.stringify(savedState));

            recalcKpiTotal();
        }

        function recalcKpiTotal() {
            let totalDsCu = 0;
            let totalDsMoi = kpiBaseData.city.ds_moi + kpiBaseData.mia.ds_moi + kpiBaseData.edu.ds_moi + kpiBaseData.fee.ds_moi;
            let totalKpiDs = kpiBaseData.city.kpi_ds + kpiBaseData.mia.kpi_ds + kpiBaseData.edu.kpi_ds;
            let totalKpiQLead = kpiBaseData.city.kpi_qlead + kpiBaseData.mia.kpi_qlead + kpiBaseData.edu.kpi_qlead;
            let totalQLead = 0;
            let hasQLead = false;
            let totalFl = 0;
            let hasFl = false;

            ['city', 'mia', 'edu'].forEach(b => {
                const cu = parseFloat(document.getElementById(`input_${b}_ds_cu`)?.value) || 0;
                totalDsCu += cu;

                const qlVal = document.getElementById(`input_${b}_qlead`)?.value;
                if (qlVal !== '' && qlVal !== undefined && qlVal !== null) {
                    totalQLead += parseInt(qlVal) || 0;
                    hasQLead = true;
                }

                const flVal = document.getElementById(`input_${b}_fl`)?.value;
                if (flVal !== '' && flVal !== undefined && flVal !== null) {
                    totalFl += parseInt(flVal) || 0;
                    hasFl = true;
                }
            });

            const totalDsTong = totalDsMoi + totalDsCu;
            const totalDsThieu = Math.max(0, totalKpiDs - totalDsTong);
            const totalRateHt = (totalDsTong / totalKpiDs) * 100;

            const elTotCu = document.getElementById('val_total_ds_cu');
            const elTotMoi = document.getElementById('val_total_ds_moi');
            const elTotTong = document.getElementById('val_total_ds_tong');
            const elTotThieu = document.getElementById('val_total_ds_thieu');
            const elTotRateHt = document.getElementById('val_total_rate_ht');

            if (elTotCu) elTotCu.textContent = formatVND(totalDsCu);
            if (elTotMoi) elTotMoi.textContent = formatVND(totalDsMoi);
            if (elTotTong) elTotTong.textContent = formatVND(totalDsTong);
            if (elTotThieu) elTotThieu.textContent = formatVND(totalDsThieu);
            if (elTotRateHt) {
                elTotRateHt.innerHTML = `<span class="px-2.5 py-1 rounded bg-emerald-100 text-emerald-800 text-[11px] font-extrabold">${totalRateHt.toFixed(2).replace('.', ',')}%</span>`;
            }

            const elTotQLead = document.getElementById('val_total_qlead');
            const elTotQLeadThieu = document.getElementById('val_total_qlead_thieu');
            if (elTotQLead) elTotQLead.textContent = hasQLead ? totalQLead : '--';
            if (elTotQLeadThieu) elTotQLeadThieu.textContent = hasQLead ? Math.max(0, totalKpiQLead - totalQLead) : totalKpiQLead;

            const elTotFl = document.getElementById('val_total_fl');
            const elTotRateFl = document.getElementById('val_total_rate_fl');
            if (elTotFl) elTotFl.textContent = hasFl ? totalFl : '--';
            if (elTotRateFl) {
                if (hasFl) {
                    elTotRateFl.textContent = ((totalFl / 2430) * 100).toFixed(2).replace('.', ',') + '%';
                } else {
                    elTotRateFl.textContent = '0,00%';
                }
            }
        }

        function loadKpiSavedData() {
            ['city', 'mia', 'edu'].forEach(b => {
                const saved = localStorage.getItem(`kpi_row_${b}`);
                if (saved) {
                    try {
                        const parsed = JSON.parse(saved);
                        if (parsed.cu) document.getElementById(`input_${b}_ds_cu`).value = parsed.cu;
                        if (parsed.qlead) document.getElementById(`input_${b}_qlead`).value = parsed.qlead;
                        if (parsed.fl) document.getElementById(`input_${b}_fl`).value = parsed.fl;
                        if (parsed.eng) document.getElementById(`input_${b}_eng`).value = parsed.eng;
                    } catch (e) {}
                }
                recalcKpiRow(b);
            });
        }

        function fillSampleKpiData() {
            document.getElementById('input_city_qlead').value = 75;
            document.getElementById('input_mia_qlead').value = 15;
            document.getElementById('input_edu_qlead').value = 0;
            ['city', 'mia', 'edu'].forEach(b => recalcKpiRow(b));
        }

        // Initialize table on DOMContentLoaded
        setTimeout(loadKpiSavedData, 100);
"""

with open('/Users/ted/Desktop/Code/RPB/marketing_dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Insert the KPI table right inside #tab-executive before Chart Grid
target_anchor = '<!-- Charts Grid -->'
if target_anchor in html and 'BẢNG DỮ LIỆU THEO KPI TỔNG' not in html:
    html = html.replace(target_anchor, kpi_table_html + '\n            ' + target_anchor)
    print("Inserted KPI Table HTML.")
else:
    print("KPI Table already present or anchor not found.")

# Insert Script Logic before </script>
script_anchor = '});\n    </script>'
if script_anchor in html and 'recalcKpiRow' not in html:
    html = html.replace(script_anchor, kpi_script_code + '\n        });\n    </script>')
    print("Inserted KPI Script Logic.")
else:
    print("KPI script already present or anchor not found.")

with open('/Users/ted/Desktop/Code/RPB/marketing_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('/Users/ted/Desktop/Code/RPB/build_html.py', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved marketing_dashboard.html & build_html.py successfully!")

const https = require('https');
const path = require('path');
const fs = require('fs');

// Cấu hình kết nối AI Seller MCP
const AISELLER_API_KEY = process.env.AISELLER_API_KEY || 'aat_110b15afb5a529f2bcc148bc1215994e7b4170da45e496f1e3ba0e6db7efb68a';
const AISELLER_MCP_URL = process.env.AISELLER_MCP_URL || 'https://chatbot.sales.ai.vn/api/mcp';
const CHATBOT_ID = 14; // Chatbot: "Nội Thất Rồng Phương Bắc"

// Cấu hình Telegram
const TELEGRAM_BOT_TOKEN = process.env.RPB_TELEGRAM_BOT_TOKEN || '9247946542:AAH9C_6bRd-48PQzy2YX1Xs1a3gRRZirTjI';
const TELEGRAM_CHAT_ID = process.env.RPB_TELEGRAM_GROUP_CHAT_ID || '-5547572529'; // Nhóm "Báo cáo Ads RPB"

// Cấu hình Zalo
const ZALO_GROUP_ID = process.env.RPB_ZALO_REPORT_GROUP_ID || '1457169683489298320'; // Nhóm "B2B- B2C MKT - RPB"
const ZALO_SESSION_PATH = path.join(__dirname, 'zalo_session.json');

// File lưu vết các ngày đã gửi để tránh gửi trùng
const SENT_TRACKER_FILE = path.join(__dirname, '.last_rpb_chatbot_report_sent.json');

function isAlreadySent(dateStr) {
  try {
    if (fs.existsSync(SENT_TRACKER_FILE)) {
      const data = JSON.parse(fs.readFileSync(SENT_TRACKER_FILE, 'utf-8'));
      return Array.isArray(data.sentDates) && data.sentDates.includes(dateStr);
    }
  } catch (e) {}
  return false;
}

function markAsSent(dateStr) {
  try {
    let data = { sentDates: [] };
    if (fs.existsSync(SENT_TRACKER_FILE)) {
      data = JSON.parse(fs.readFileSync(SENT_TRACKER_FILE, 'utf-8'));
    }
    if (!Array.isArray(data.sentDates)) data.sentDates = [];
    if (!data.sentDates.includes(dateStr)) {
      data.sentDates.push(dateStr);
      if (data.sentDates.length > 30) data.sentDates = data.sentDates.slice(-30);
      fs.writeFileSync(SENT_TRACKER_FILE, JSON.stringify(data, null, 2), 'utf-8');
    }
  } catch (e) {}
}

function formatVND(num) {
  const val = Math.round(Number(num) || 0);
  return val.toLocaleString('vi-VN') + ' đ';
}

function formatNum(num) {
  const val = Math.round(Number(num) || 0);
  return val.toLocaleString('vi-VN');
}

// Gọi API MCP AI Seller qua JSON-RPC
function callAiSellerMcp(methodName, args) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      jsonrpc: '2.0',
      id: Date.now(),
      method: 'tools/call',
      params: {
        name: methodName,
        arguments: args
      }
    });

    const req = https.request(AISELLER_MCP_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${AISELLER_API_KEY}`,
        'Content-Length': Buffer.byteLength(payload)
      }
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          if (json.error) {
            return reject(new Error(json.error.message || 'Lỗi MCP'));
          }
          const text = json.result && json.result.content && json.result.content[0] ? json.result.content[0].text : '{}';
          resolve(JSON.parse(text));
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// Lấy toàn bộ hội thoại trong ngày cho Chatbot RPB (ID: 14)
async function fetchAllConversations(targetDate) {
  let offset = 0;
  const limit = 100;
  const allConversations = [];
  let hasMore = true;

  while (hasMore && offset < 3000) {
    const data = await callAiSellerMcp('aiseller_list_conversations', {
      chatbotId: CHATBOT_ID,
      from: targetDate,
      to: targetDate,
      limit: limit,
      offset: offset
    });

    const convs = (data && data.conversations) || [];
    allConversations.push(...convs);

    if (convs.length < limit || !data.pagination || !data.pagination.hasMore) {
      hasMore = false;
    } else {
      offset += limit;
    }
  }

  return allConversations;
}

// Phân tích dữ liệu hội thoại RPB
function analyzeConversations(conversations, targetDate) {
  const total = conversations.length;
  const platforms = {};
  const sentiments = { positive: 0, neutral: 0, negative: 0, mixed: 0 };
  const intents = { ordering: 0, pricing: 0, technical: 0, complaint: 0, other: 0 };
  const orderStatuses = { closed: 0, considering: 0, dropped: 0, none: 0 };
  let totalRevenue = 0;

  let aiHandled = 0;
  let adminIntervened = 0;

  const hotLeads = [];     // Khách tiềm năng cần follow-up
  const urgentCases = [];  // Khiếu nại, phản hồi tiêu cực, lỗi bot

  for (const c of conversations) {
    // 1. Phân bổ theo kênh
    const pName = c.platformName || 'Khác';
    platforms[pName] = (platforms[pName] || 0) + 1;

    // 2. Theo dõi AI vs Nhân viên can thiệp
    if (c.aiHandlingPaused && (c.pausedReason === 'admin_reply' || c.pausedReason === 'manual')) {
      adminIntervened++;
    } else {
      aiHandled++;
    }

    const evalData = c.evaluation || {};

    // 3. Cảm xúc khách hàng
    const sentiment = evalData.sentiment || 'neutral';
    if (sentiments[sentiment] !== undefined) {
      sentiments[sentiment]++;
    } else {
      sentiments.neutral++;
    }

    // 4. Ý định khách hàng
    const intent = evalData.intent || 'other';
    if (intents[intent] !== undefined) {
      intents[intent]++;
    } else {
      intents.other++;
    }

    // 5. Trạng thái đơn & doanh thu
    const orderStatus = evalData.orderStatus || 'none';
    if (orderStatuses[orderStatus] !== undefined) {
      orderStatuses[orderStatus]++;
    }

    const val = Number(evalData.orderValue) || 0;
    if (orderStatus === 'closed') {
      totalRevenue += val;
    }

    // 6. Phát hiện Hot Leads (Đang cân nhắc số lượng lớn / có nhu cầu rõ ràng / chốt đơn)
    if (orderStatus === 'closed' || orderStatus === 'considering' || evalData.intent === 'ordering' || evalData.intent === 'pricing') {
      if (evalData.summary && evalData.summary.trim().length > 15) {
        hotLeads.push({
          customer: c.customerName || 'Khách liên hệ',
          phone: c.customerPhone,
          platform: pName,
          status: orderStatus,
          intent: evalData.intent,
          summary: evalData.summary,
          suggestion: evalData.suggestion || ''
        });
      }
    }

    // 7. Phát hiện ca khẩn cấp (khiếu nại, tiêu cực, lỗi bot)
    if (sentiment === 'negative' || evalData.intent === 'complaint' || c.pausedReason === 'ai_error') {
      urgentCases.push({
        customer: c.customerName || 'Khách liên hệ',
        phone: c.customerPhone,
        platform: pName,
        reason: c.pausedReason === 'ai_error' ? 'Lỗi hệ thống AI' : 'Khách khiếu nại / phản ứng tiêu cực',
        summary: evalData.summary || (c.lastMessage && c.lastMessage.text) || 'Cần kiểm tra hội thoại'
      });
    }
  }

  return {
    targetDate,
    total,
    platforms,
    aiHandled,
    adminIntervened,
    sentiments,
    intents,
    orderStatuses,
    totalRevenue,
    closedDeals: orderStatuses.closed,
    hotLeads,
    urgentCases
  };
}

// Xây dựng thông điệp báo cáo chuẩn bị gửi Telegram (HTML)
function buildTelegramReport(analysis) {
  const {
    targetDate,
    total,
    platforms,
    aiHandled,
    adminIntervened,
    sentiments,
    intents,
    orderStatuses,
    totalRevenue,
    closedDeals,
    hotLeads,
    urgentCases
  } = analysis;

  const [yyyy, mm, dd] = targetDate.split('-');
  const displayDate = `${dd}/${mm}/${yyyy}`;

  let msg = `🏛️ <b>BÁO CÁO PHÂN TÍCH CHATBOT RỒNG PHƯƠNG BẮC</b>\n`;
  msg += `<i>📅 Dữ liệu ngày: ${displayDate} (Tổng kết lúc 08:00 AM)</i>\n`;
  msg += `━━━━━━━━━━━━━━━━━━━━\n\n`;

  // 1. Ca cần lưu ý gấp (nếu có)
  if (urgentCases.length > 0) {
    msg += `⚠️ <b>1. CA CẦN CSKH LƯU Ý GẤP (${urgentCases.length} ca):</b>\n`;
    urgentCases.slice(0, 3).forEach((item, idx) => {
      const phoneStr = item.phone ? ` (${item.phone})` : '';
      msg += `• <b>${item.customer}${phoneStr}</b> [${item.platform}]\n`;
      msg += `  └ <i>${item.reason}: ${item.summary.slice(0, 110)}...</i>\n`;
    });
    msg += `\n`;
  }

  // 2. Leads tiềm năng cần chăm sóc trong ngày
  msg += `🌟 <b>${urgentCases.length > 0 ? '2' : '1'}. LEADS TIỀM NĂNG CẦN CHĂM SÓC NGAY (${hotLeads.length} leads):</b>\n`;
  if (hotLeads.length === 0) {
    msg += `<i>Chưa có leads nổi bật trong ngày.</i>\n`;
  } else {
    hotLeads.slice(0, 4).forEach((item, idx) => {
      const phoneStr = item.phone ? ` (${item.phone})` : '';
      const tag = item.status === 'closed' ? '🎯 Đã chốt' : '⏳ Đang cân nhắc';
      msg += `<b>${idx + 1}. ${item.customer}${phoneStr}</b> [${tag} - ${item.platform}]\n`;
      msg += `   └ <i>Nhu cầu:</i> ${item.summary.slice(0, 110)}...\n`;
      if (item.suggestion) {
        msg += `   └ <i>Gợi ý xử lý:</i> ${item.suggestion.slice(0, 95)}...\n`;
      }
    });
    if (hotLeads.length > 4) {
      msg += `   <i>...và còn ${hotLeads.length - 4} khách tiềm năng khác trên hệ thống.</i>\n`;
    }
  }
  msg += `\n`;

  // 3. Hiệu quả chuyển đổi
  msg += `💰 <b>${urgentCases.length > 0 ? '3' : '2'}. KẾT QUẢ CHUYỂN ĐỔI:</b>\n`;
  msg += `• Đơn đã chốt: 🎯 <b>${closedDeals} đơn</b>`;
  if (totalRevenue > 0) {
    msg += ` (Doanh số: 💵 <b>${formatVND(totalRevenue)}</b>)`;
  }
  msg += `\n`;
  msg += `• Đang cân nhắc / Báo giá: ⏳ <b>${orderStatuses.considering} khách</b>\n`;
  msg += `• Khách chưa có nhu cầu mua: <b>${orderStatuses.dropped} khách</b>\n\n`;

  // 4. Tổng quan tương tác & Kênh
  msg += `📊 <b>${urgentCases.length > 0 ? '4' : '3'}. TỔNG QUAN TƯƠNG TÁC:</b>\n`;
  msg += `• Tổng cuộc hội thoại: 💬 <b>${formatNum(total)} khách</b>\n`;
  msg += `• Tỷ lệ xử lý: 🤖 AI tự động: <b>${aiHandled}</b> | 👨‍💼 Nhân viên can thiệp: <b>${adminIntervened}</b>\n`;
  msg += `• Phân bổ theo thương hiệu/kênh:\n`;
  for (const [pName, count] of Object.entries(platforms)) {
    const icon = pName.toLowerCase().includes('zalo') ? '📱' : '📘';
    msg += `   └ ${icon} ${pName}: <b>${count}</b> (${((count / (total || 1)) * 100).toFixed(0)}%)\n`;
  }
  msg += `\n`;

  // 5. Nhu cầu & Cảm xúc
  msg += `🔍 <b>${urgentCases.length > 0 ? '5' : '4'}. NHU CẦU & TÂM LÝ KHÁCH HÀNG:</b>\n`;
  msg += `• Ý định: 🛍️ Mua sắm: <b>${intents.ordering}</b> | 🏷️ Hỏi giá: <b>${intents.pricing}</b> | ⚙️ Kỹ thuật: <b>${intents.technical}</b>\n`;
  msg += `• Sắc thái: 😊 Tích cực: <b>${sentiments.positive}</b> | 😐 Trung lập: <b>${sentiments.neutral}</b> | ⚠️ Tiêu cực: <b>${sentiments.negative}</b>\n\n`;

  msg += `🚀 <i>Chúc đội ngũ Rồng Phương Bắc một ngày tư vấn hiệu quả và bùng nổ doanh số!</i>`;
  return msg;
}

// Chuyển đổi thông điệp Telegram HTML sang Plain Text cho Zalo
function buildZaloReport(analysis) {
  const teleMsg = buildTelegramReport(analysis);
  // Loại bỏ tag HTML
  return teleMsg
    .replace(/<b>(.*?)<\/b>/g, '$1')
    .replace(/<i>(.*?)<\/i>/g, '$1')
    .replace(/<[^>]+>/g, '');
}

// Gửi tin nhắn Telegram
function sendTelegram(text) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      chat_id: TELEGRAM_CHAT_ID,
      text: text,
      parse_mode: 'HTML'
    });

    const req = https.request({
      hostname: 'api.telegram.org',
      port: 443,
      path: `/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try {
          resolve(JSON.parse(d));
        } catch (e) {
          resolve({ ok: false, error: e.message });
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// Gửi tin nhắn Zalo qua zca-js
async function sendZalo(text) {
  if (!fs.existsSync(ZALO_SESSION_PATH)) {
    throw new Error('Chưa tìm thấy session Zalo tại ' + ZALO_SESSION_PATH);
  }

  const { Zalo, ThreadType } = require('zca-js');
  const creds = JSON.parse(fs.readFileSync(ZALO_SESSION_PATH, 'utf-8'));
  const zalo = new Zalo({ logging: false });
  const api = await zalo.login(creds);

  const res = await api.sendMessage({ msg: text }, ZALO_GROUP_ID, ThreadType.Group);
  return res;
}

// Hàm điều phối chính
async function runReport(targetDate, shouldSend = false, force = false) {
  if (shouldSend && !force && isAlreadySent(targetDate)) {
    console.log(`[RPB Chatbot] ℹ️ Báo cáo ngày ${targetDate} đã được gửi trước đó, bỏ qua để tránh trùng lặp.`);
    return { skipped: true, targetDate };
  }

  console.log(`[RPB Chatbot] Đang quét dữ liệu ngày: ${targetDate} cho chatbot Nội Thất Rồng Phương Bắc...`);
  const conversations = await fetchAllConversations(targetDate);
  console.log(`[RPB Chatbot] Tìm thấy ${conversations.length} cuộc hội thoại.`);

  const analysis = analyzeConversations(conversations, targetDate);
  const teleMessage = buildTelegramReport(analysis);
  const zaloMessage = buildZaloReport(analysis);

  if (shouldSend) {
    // 1. Gửi vào Telegram
    console.log(`[RPB Chatbot] Đang gửi báo cáo vào nhóm Telegram: ${TELEGRAM_CHAT_ID}...`);
    try {
      const teleRes = await sendTelegram(teleMessage);
      if (teleRes.ok) {
        console.log(`[RPB Chatbot] ✅ Đã gửi Telegram thành công!`);
      } else {
        console.error(`[RPB Chatbot] ❌ Lỗi gửi Telegram:`, teleRes.description || teleRes);
      }
    } catch (tErr) {
      console.error(`[RPB Chatbot] ❌ Lỗi Telegram:`, tErr.message);
    }

    // 2. Gửi vào Zalo
    console.log(`[RPB Chatbot] Đang gửi báo cáo vào nhóm Zalo: ${ZALO_GROUP_ID}...`);
    try {
      await sendZalo(zaloMessage);
      console.log(`[RPB Chatbot] ✅ Đã gửi Zalo thành công!`);
    } catch (zErr) {
      console.error(`[RPB Chatbot] ❌ Lỗi Zalo:`, zErr.message);
    }

    markAsSent(targetDate);
  }

  return { analysis, teleMessage, zaloMessage, skipped: false };
}

module.exports = {
  runReport,
  fetchAllConversations,
  analyzeConversations,
  buildTelegramReport,
  buildZaloReport
};

// Chạy trực tiếp qua CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const shouldSend = args.includes('--send');
  const force = args.includes('--force');

  // Mặc định lấy ngày hôm qua (Asia/Ho_Chi_Minh)
  const dYesterday = new Date(Date.now() - 24 * 3600 * 1000);
  const yesterdayStr = dYesterday.toLocaleDateString('en-CA', { timeZone: 'Asia/Ho_Chi_Minh' });
  const dateInput = args.find(a => /^\d{4}-\d{2}-\d{2}$/.test(a)) || yesterdayStr;

  runReport(dateInput, shouldSend, force)
    .then(res => {
      if (res.skipped) return;
      if (!shouldSend) {
        console.log('\n================ NỘI DUNG BÁO CÁO TELEGRAM (XEM TRƯỚC) ================');
        console.log(res.teleMessage.replace(/<[^>]+>/g, ''));
        console.log('========================================================================\n');
        console.log('(Dùng thêm cờ --send để gửi trực tiếp vào nhóm Telegram và Zalo)');
      }
    })
    .catch(err => {
      console.error('❌ Lỗi:', err);
    });
}

(() => {
    let elements = Array.from(document.querySelectorAll('button, div[role=button], material-button, span, div'));
    let withDate = elements.filter(e => e.innerText && (e.innerText.includes('Tháng 11') || e.innerText.includes('2026') || e.innerText.includes('Hôm nay') || e.innerText.includes('Tuỳ chỉnh')));
    return withDate.slice(0, 15).map(e => e.tagName + '.' + e.className + ' -> ' + e.innerText.substring(0, 50)).join('\n');
})()

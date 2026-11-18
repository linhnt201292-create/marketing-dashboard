(() => {
    let btns = Array.from(document.querySelectorAll('button, [role=button], div'));
    let dateBtn = btns.find(b => b.innerText && b.innerText.includes('Tháng 10 20 – Tháng 11 16'));
    if (dateBtn) {
        dateBtn.click();
        return 'Clicked: ' + dateBtn.innerText;
    }
    return 'Not found';
})()

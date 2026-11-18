tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t starts with "https://ads.google.com/aw/accounts" then
                set active tab of w to t
                tell t
                    return execute javascript " (() => {     let dateElements = Array.from(document.querySelectorAll('*')).filter(el => {         return el.children.length === 0 && el.innerText && (             el.innerText.includes('Tháng 10 20') ||              el.innerText.includes('30 ngày qua') ||             el.innerText.includes('Tuỳ chỉnh')         );     });     if (dateElements.length > 0) {         // click parent or itself         let target = dateElements[0].closest('button, [role=button], div') || dateElements[0];         target.click();         return 'Clicked: ' + dateElements[0].innerText;     }     return 'No date element found'; })() "
                end tell
            end if
        end repeat
    end repeat
    return "Tab not found"
end tell
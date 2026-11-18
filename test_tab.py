import subprocess

js = """
(() => {
    let allButtons = Array.from(document.querySelectorAll('button, [role=button], div'));
    let dateBtn = allButtons.find(b => b.innerText && (b.innerText.includes('Tháng 10 20') || b.innerText.includes('30 ngày qua')));
    if (dateBtn) {
        dateBtn.click();
        return 'Clicked dateBtn: ' + dateBtn.innerText;
    }
    return 'Not found, sample: ' + allButtons.filter(b => b.innerText && b.innerText.length < 30).slice(0, 10).map(b => b.innerText.trim()).join(' | ');
})()
"""

clean_js = js.replace("\n", " ").replace('"', '\\"')

script = f'''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (id of t as string) is "1215344120" then
                set active tab of w to t
                tell t
                    return execute javascript "{clean_js}"
                end tell
            end if
        end repeat
    end repeat
end tell'''

with open('/Users/ted/Desktop/Code/RPB/run_script.applescript', 'w') as f:
    f.write(script)

res = subprocess.run(['osascript', '/Users/ted/Desktop/Code/RPB/run_script.applescript'], capture_output=True, text=True)
print('Result:', res.stdout)

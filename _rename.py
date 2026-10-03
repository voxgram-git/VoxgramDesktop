import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/Telegram/Resources/langs")

with open("lang.strings", "r", encoding="utf-8") as f:
    content = f.read()

if not os.path.exists("lang.strings.bak"):
    with open("lang.strings.bak", "w", encoding="utf-8") as f:
        f.write(content)

LINE_RE = re.compile(r'^(\s*"[^"]+"\s*=\s*)"((?:[^"\\]|\\.)*)"(\s*;.*)$')

def replace_in_value(line: str) -> str:
    m = LINE_RE.match(line)
    if not m:
        return line
    prefix, value, suffix = m.group(1), m.group(2), m.group(3)

    # URLs (longest patterns first)
    value = value.replace("telegram.org", "voxgram.fun")
    value = value.replace("https://t.me/", "https://voxgram.fun/")
    value = re.sub(r'(?<!\w)t\.me/', 'voxgram.fun/', value)

    # Brand
    value = value.replace("Telegram Desktop", "Voxgram Desktop")
    value = re.sub(r'\bTelegram\b', 'Voxgram', value)
    value = re.sub(r'\btelegram\b', 'voxgram', value)

    return prefix + '"' + value + '"' + suffix


out_lines = [replace_in_value(line) for line in content.splitlines(keepends=True)]

with open("lang.strings", "w", encoding="utf-8") as f:
    f.write("".join(out_lines))

with open("lang.strings", "r", encoding="utf-8") as f:
    new = f.read()

print("Telegram remaining:", new.count("Telegram"))
print("Voxgram count:   ", new.count("Voxgram"))
print("t.me remaining:   ", new.count("t.me"))
print("voxgram.fun count: ", new.count("voxgram.fun"))

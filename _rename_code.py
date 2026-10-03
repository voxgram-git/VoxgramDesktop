"""
Заменяет t.me/https://t.me в C++ исходниках tdesktop на voxgram.fun.
НЕ трогает tg:// (URL-схема приложения — ломать нельзя).
"""
import os
import re

ROOT = r"C:\tdesktop\Telegram\SourceFiles"

# Паттерны безопасные — только "t.me..." в строковых литералах
# (внутри Qt _q строк или обычных "" строк).
# Не трогаем:
#  - telegram.me (legacy) можно заменить на voxgram.fun
#  - t.me как часть имени переменной
PATTERNS = [
    (re.compile(r'"https://t\.me/'), '"https://voxgram.fun/'),
    (re.compile(r'"t\.me/'),         '"voxgram.fun/'),
    (re.compile(r"'https://t\.me/"), "'https://voxgram.fun/"),
    (re.compile(r"'t\.me/"),         "'voxgram.fun/"),
    # Ubuntu/GitHub/issue tracker URLs оставляем как есть — они в комментариях.
]

total_files = 0
total_replacements = 0

for dirpath, _, filenames in os.walk(ROOT):
    for name in filenames:
        if not name.endswith((".cpp", ".h")):
            continue
        path = os.path.join(dirpath, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except (OSError, UnicodeDecodeError):
            continue

        orig = text
        local_count = 0
        for pat, repl in PATTERNS:
            new_text, n = pat.subn(repl, text)
            if n:
                text = new_text
                local_count += n

        if local_count:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            total_files += 1
            total_replacements += local_count

print(f"Files changed: {total_files}")
print(f"Replacements:  {total_replacements}")

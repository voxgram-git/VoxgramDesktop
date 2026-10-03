import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PUBKEY_PATH = os.path.join(HERE, "pubkey.asc")
CPP_PATH = os.path.join(HERE, "Telegram", "SourceFiles", "mtproto", "mtproto_dc_options.cpp")

with open(PUBKEY_PATH, "r", encoding="utf-8") as f:
    pem = f.read().strip()

# Extract body lines between BEGIN/END
match = re.search(
    r"-----BEGIN RSA PUBLIC KEY-----\s*(.*?)\s*-----END RSA PUBLIC KEY-----",
    pem, re.DOTALL,
)
if not match:
    raise SystemExit("pubkey.asc doesn't look like PEM RSA PUBLIC KEY")

body_lines = [ln.strip() for ln in match.group(1).splitlines() if ln.strip()]

# Build the C string block
block_lines = ["-----BEGIN RSA PUBLIC KEY-----"] + body_lines + ["-----END RSA PUBLIC KEY-----"]
c_string = "\\\n".join(ln + "\\n" for ln in block_lines[:-1]) + "\\\n" + block_lines[-1]
c_literal = '"\\\n' + c_string + '"'

with open(CPP_PATH, "r", encoding="utf-8") as f:
    cpp = f.read()

# Replace both key blocks (test + prod use the same key since we have one server)
placeholder_re = re.compile(
    r'"\\\n-----BEGIN RSA PUBLIC KEY-----\\n\\\n'
    r'(?:VOXGRAM_PUBKEY_LINE_\d+_HERE\\n\\\n)+'
    r'-----END RSA PUBLIC KEY-----"',
    re.DOTALL,
)
# NOTE: pass the replacement as a lambda — re.sub treats string
# replacements as templates and would interpret the backslash-newline
# continuations and \\n escape sequences inside c_literal, producing a
# broken C string. A function replacement is taken verbatim.
new_cpp, n = placeholder_re.subn(lambda _: c_literal, cpp)
if n == 0:
    raise SystemExit("Placeholder not found in mtproto_dc_options.cpp — already applied?")

with open(CPP_PATH, "w", encoding="utf-8") as f:
    f.write(new_cpp)

print(f"Replaced {n} key block(s).")
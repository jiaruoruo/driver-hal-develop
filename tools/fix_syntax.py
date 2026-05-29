#!/usr/bin/env python3
"""修复 server.py 中的语法错误：rstrip('/\') → rstrip('/\\')"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

SERVER_PY = r'd:\AI\myproject\driver-hal-develop\gui\server.py'

with open(SERVER_PY, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复：rstrip('/\') 是非法的，应该是 rstrip('/\\')
old = "local_path = local_path.rstrip('/\\') + '_' + str(int(_t.time()))"
new = "local_path = local_path.rstrip('/\\\\') + '_' + str(int(_t.time()))"

# 实际上在 Python 源码中 '/\' 应该是 '/\\' (两个字符: slash, backslash)
# 让我直接用字节来检查
print("File size:", len(content))

# 找到并显示第 946 行附近内容
lines = content.split('\n')
print(f"Line 944: {repr(lines[943])}")
print(f"Line 945: {repr(lines[944])}")
print(f"Line 946: {repr(lines[945])}")
print(f"Line 947: {repr(lines[946])}")

# 修复：将 .rstrip('/\') 替换为 .rstrip('/\\')
# 在文件中实际存储的可能是 rstrip('/\') (3 chars inside quotes)
import re

# 找到包含 rstrip 和时间戳的那行
for i, line in enumerate(lines):
    if 'rstrip' in line and 'time' in line and 'local_path' in line:
        print(f"\nFound at line {i+1}: {repr(line)}")
        # 修复这一行
        fixed_line = re.sub(r"\.rstrip\(['\"].*?['\"]\)", ".rstrip('/\\\\')", line)
        print(f"Fixed: {repr(fixed_line)}")
        lines[i] = fixed_line

fixed_content = '\n'.join(lines)
with open(SERVER_PY, 'w', encoding='utf-8') as f:
    f.write(fixed_content)
print("\n[OK] 已修复并保存")

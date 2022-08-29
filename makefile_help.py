import re
import sys

makefile_lines = sys.stdin.readlines()
target_comment_pairs = []
idx = 0
while idx < len(makefile_lines):
    comment_match = re.match(r"^## ([\w ]+)$$", makefile_lines[idx])
    if comment_match:
        comment = comment_match.group(1)
        idx += 1
        target_match = re.match(r"^([\w/-]+):.*\n$$", makefile_lines[idx])
        target = target_match.group(1)
        target_comment_pairs.append((target, comment))
    idx += 1

max_target_length = 0
for target, _ in target_comment_pairs:
    if len(target) > max_target_length:
        max_target_length = len(target)

for target, comment in target_comment_pairs:
    print(f"{target:{max_target_length + 1}} {comment}")

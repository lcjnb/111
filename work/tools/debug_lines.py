"""Print the content lines the validator considers untagged."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path("skills/scripts").resolve()))

from validate_workbench import _content_lines, TAGS

for name in sys.argv[1:]:
    path = Path(name)
    print("==", path.name)
    for number, line in enumerate(_content_lines(path.read_text(encoding="utf-8")), start=1):
        if not any(tag in line for tag in TAGS):
            print(number, repr(line))

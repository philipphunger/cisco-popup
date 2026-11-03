"""Set GitHub metadata before publishing."""
import json
from pathlib import Path
import re
import sys

if len(sys.argv) != 2 or not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", sys.argv[1]):
    raise SystemExit("Usage: python scripts/configure_repository.py GITHUB_USERNAME")
owner = sys.argv[1]
manifest = Path(__file__).resolve().parents[1] / "custom_components/cisco_popup/manifest.json"
data = json.loads(manifest.read_text(encoding="utf-8"))
data.update(documentation=f"https://github.com/{owner}/cisco-popup",
            issue_tracker=f"https://github.com/{owner}/cisco-popup/issues",
            codeowners=[f"@{owner}"])
manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
print("Repository metadata updated.")

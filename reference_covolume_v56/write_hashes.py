#!/usr/bin/env python3
"""Refresh hashes of this component's top-level deliverables only."""
from pathlib import Path
import hashlib
import json

here = Path(__file__).resolve().parent
values = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(here.iterdir())
          if p.is_file() and p.name != 'hashes.json'}
(here / 'hashes.json').write_text(json.dumps(values, indent=2) + '\n')
print(json.dumps({'component': here.name, 'top_level_files': len(values)}))

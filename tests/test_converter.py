from annotation_converter import convert
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
path_to_kognic_annotation = ROOT.parent / "examples" / "kognic_format.json"

with open(path_to_kognic_annotation, 'r') as content:
    kognic_annotation = json.load(content)

open_label_annotation = convert(kognic_annotation)

print(json.dumps(open_label_annotation, indent=2)[:1000])

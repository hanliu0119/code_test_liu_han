# tests/test_example_usage.py
from annotation_converter import convert
import json
from pathlib import Path

def test_convert():
    """Test conversion runs successfully and returns valid OpenLABEL structure."""
    ROOT = Path(__file__).resolve().parents[0]
    path_to_kognic_annotation = ROOT.parent / "examples" / "kognic_format.json"

    # Load example input
    with open(path_to_kognic_annotation, "r") as content:
        kognic_annotation = json.load(content)

    # Run conversion
    open_label_annotation = convert(kognic_annotation)

    # Basic structural assertions
    assert isinstance(open_label_annotation, dict)
    assert "data" in open_label_annotation
    assert "openlabel" in open_label_annotation["data"]
    ol = open_label_annotation["data"]["openlabel"]
    assert "objects" in ol
    assert "frames" in ol

    # Optional: print partial output for debugging (truncated)
    print(json.dumps(open_label_annotation, indent=2)[:1000])

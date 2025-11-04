# tests/test_api.py
# Purpose: API-level tests for /convert endpoint using FastAPI TestClient.
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import json
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)
EXAMPLES = Path(__file__).resolve().parents[1] / "examples"

def test_convert_get_status_and_shape():
    """Ensure GET /convert accepts JSON body and returns expected top-level structure."""
    kognic = json.loads((EXAMPLES / "kognic_format.json").read_text())
    resp = client.request("GET", "/convert", json=kognic)
    assert resp.status_code == 200
    data = resp.json()
    assert "data" in data
    assert "openlabel" in data["data"]


def test_convert_get_bbox_matches_example_one_id():
    """Spot-check bbox values for one id against the provided open_label_format.json."""
    kognic = json.loads((EXAMPLES / "kognic_format.json").read_text())
    expected = json.loads((EXAMPLES / "open_label_format.json").read_text())

    resp = client.request("GET", "/convert", json=kognic)
    assert resp.status_code == 200
    out = resp.json()

    check_id = "9610f0ef-185f-41c6-a500-db0d568a8feb"
    bbox_out = out["data"]["openlabel"]["frames"]["0"]["objects"][check_id]["object_data"]["bbox"][0]["val"]
    bbox_expected = expected["data"]["openlabel"]["frames"]["0"]["objects"][check_id]["object_data"]["bbox"][0]["val"]

    # Compare floats with tolerance
    for a, b in zip(bbox_out, bbox_expected):
        assert abs(a - b) < 1e-6

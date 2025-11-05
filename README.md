# Kognic Coding Assignment

This coding assignment is designed to mimic some of the coding tasks that you might encounter while working together with Kognic. In order to complete this assignment you need to be proficient in Python, know how python packages are generated and be familiar with basic REST APIs. You are free to use any libraries you want.

> Hint: The `pydantic` library can be very powerful when dealing with json structures

## Assignment - Annotation Format Conversion Service

### Background
Annotations are produced during the process of labeling data. An annotation is a text file (usually json) that describes the content of the data. If you for instance were to produce a bounding-box annotation for an image containing a vehicle, the resulting annotation in the *kognic_format* could look something like this:
```
{
    "objects": [
        {
            "type": "vehicle",
            "id": "d9c42ffd-ed63-4f6a-8ac7-227de8a9945f"
            "position": {
                "x_min": 50,
                "x_max": 150,
                "y_min": 50,
                "y_max": 150
            }
        }
    ]
}
```

, where the `id` field is an identifier of the vehicle object, and `x_min`, `x_max`, `y_min`, `y_max` defines the boundaries of the box in pixel coordinates.

![2022-03-09-07-27-07-27-52](https://user-images.githubusercontent.com/65158011/157385146-1a6f6c3e-8c44-446b-8ad8-58384c692192.png)

> Hint: This is not how the bounding box coordinates are defined in the openlabel format


### Assignment
One challenge when dealing with annotations is that there many different formats available. Due to this there is a need for being able to convert to and from different formats, all while making sure that the contents of the annotations are not altered.

For this assignment you are tasked with creating a REST API that performs conversion of annotations from a simplified version of the *Kognic* format to a simplified version of the *OpenLABEL* format. In order to implement this you have two files available, `kognic_format.json` containing the annotation in the Kognic format, as well as `open_label_format.json` containing the same annotation but in OpenLABEL format. These files both describe an annotation consisting of 3 different classes - `Vehicle`, `Animal` and `LicensePlate`.

In the annotation files there are 3 instances of the `Vehicle` class, 1 instance of the `Animal` class and 1 instance of the `LicensePlate` class present, but the API should be able convert annotations containing any number instances of these 3 different classes.

The API should be able to receive a GET http-request containing a json on the kognic json format and respond with the OpenLABEL converted annotation.

In order to make communication with the API easier you are also expected to provide a python client in the form of a pip-installable python package. You are free to design the client as you wish as long as it can after installation be used in a way similar to this example:

```python
from annotation_converter import convert
import json

path_to_kognic_annotation = 'kognic_format.json'
with open(path_to_kognic_annotation, 'r') as content:
    kognic_annotation = json.load(content)

open_label_annotation = convert(kognic_annotation)
```
### Regarding ASAM OpenLabel
Included is a HTML file with documentation regarding the ASAM OpenLabel format. The document includes the full specification of the format, but for this code test you will only need a small part of it

> Hint: 7.10.1. Bounding boxes


### How to deliver the assignment
The finished assignment should be pushed to this github repository on a branch named `code_test_<yourname>`. In addition to all the neccessary code it should contain a README that describes:
1. How to start the REST API locally
2. How to install and use your python-library


--------------------------------------------------------------------------------------

## 1. Installation

### Option A — Install locally
```bash
git clone https://github.com/hanliu0119/code_test_liu_han.git
cd code_test_liu_han
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Option B — One-click setup
If you prefer automation:
```bash
chmod +x setup.sh
./setup.sh
```

This script will create `.venv`, upgrade `pip`, and install all dependencies.

---

## 2. Project Structure

```
code_test_liu_han/
├── annotation_converter/          # Core logic package
│   ├── __init__.py                # Exports convert()
│   ├── bbox.py                    # Converts ExtremePointBox → [cx, cy, w, h]
│   ├── converter.py               # Main conversion pipeline (Kognic → OpenLABEL)
│   ├── mapping.py                 # Constants and class mappings
│   └── models.py                  # Pydantic data models for input/output schema
│
├── api/                           # REST API layer
│   ├── __init__.py
│   └── app.py                     # FastAPI app exposing /convert endpoint
│
├── examples/                      # Sample data and usage demo
│   ├── kognic_format.json
│   ├── open_label_format.json
│   └── example_client_usage.py
│
├── tests/                         # Unit and API integration tests
│   ├── test_converter.py
│   └── test_api.py
│
├── setup.sh                       # Optional setup helper
├── README.md
├── pyproject.toml                 # Build metadata and dependencies
└── .gitignore
```

---

## 3. How the Conversion Works

### Overview
The `convert()` function transforms a Kognic-style annotation into an OpenLABEL-style annotation while keeping all semantic information unchanged.

### Step-by-step Flow

#### 1️⃣ Input Validation
```python
k = KognicAnnotation.model_validate(kognic)
```
- Uses Pydantic models to verify structure and types.
- Maps `"class"` (reserved word) → `klass` via `Field(alias="class")`.

#### 2️⃣ Build Global Object Definitions
```python
for obj_id, prop_wrapper in k.shapeProperties.items():
    sp = prop_wrapper.get("@all")
    klass = sp.klass or ""
    mapped = CLASS_MAP.get(klass, klass or "Unknown")
    objects[obj_id] = ObjectDef(name=obj_id, type=mapped)
```
- Reads each object's class/type.  
- Uses `CLASS_MAP` to standardize class names (`Vehicle`, `Animal`, `LicensePlate`).  
- Stores all objects under `openlabel.objects`.

#### 3️⃣ Group Features by Timestamp
```python
ts = str(feature.properties.get(FRAME_KEY, 0))
frame_objects[ts][obj_id] = ...
```
- Groups detections into `frames` using `"@timestamp"` as frame key.

#### 4️⃣ Convert Coordinates
```python
cx, cy, w, h = extreme_box_to_cxcywh(feature.geometry.coordinates.model_dump())
```
- From `bbox.py`: converts Kognic “ExtremePointBox” → OpenLABEL `[cx, cy, w, h]`.

#### 5️⃣ Attach Optional Attributes
```python
if prop.Unclear is not None:
    booleans.append(BooleanEntry(name=UNCLEAR_KEY, val=prop.Unclear))
if prop.ObjectType is not None:
    texts.append(TextEntry(name=OBJECT_TYPE_KEY, val=prop.ObjectType))
```
- Adds `boolean` and `text` attributes if present (e.g., `"Unclear"`, `"ObjectType"`).

#### 6️⃣ Assemble Final OpenLABEL Output
```python
root = OpenLabelRoot(
    data={"openlabel": OpenLabel(objects=objects, frames=frames)}
)
return root.model_dump()
```
- Produces a dict identical in structure to `examples/open_label_format.json`.

---

## 4. Tests （REST API + Python）

### 1️⃣ test_convert.py
Run the example conversion directly through pytest:
```bash
pytest -s -v tests/test_convert.py
```
- `-s` allows `print()` output to appear in the console.  
- Verifies that the example file in `examples/` can be successfully converted end-to-end.

---

### 2️⃣ test_api.py
You can test the API endpoint in two ways:

**a. Using curl**
```bash
uvicorn api.app:app --reload
curl -X GET "http://127.0.0.1:8000/convert" \
  -H "Content-Type: application/json" \
  --data-binary @examples/kognic_format.json
```
- Starts the FastAPI server locally and sends a GET request with the sample input.  
- Confirms the REST interface responds correctly with OpenLABEL-format output.

**b. Using pytest**
```bash
pytest -v tests/test_api.py
```
- Runs an automated integration test via FastAPI’s `TestClient`.  
- Checks that `/convert` returns status code 200 and a valid JSON structure.

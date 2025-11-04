from typing import Dict, Any, DefaultDict
from collections import defaultdict

from .bbox import extreme_box_to_cxcywh
from .mapping import CLASS_MAP, STREAM_DEFAULT, UNCLEAR_KEY, OBJECT_TYPE_KEY, FRAME_KEY
from .models import (
    KognicAnnotation, OpenLabelRoot, OpenLabel, ObjectDef, Frame, FrameObject,
    ObjectData, BBox, BooleanEntry, TextEntry
)

def convert(kognic: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a simplified Kognic-format annotation (dict)
    to the simplified OpenLABEL-format (dict), matching the provided example.
    """
    k = KognicAnnotation.model_validate(kognic)

    # 1) Build 'objects' dictionary: id -> {name, type}
    objects: Dict[str, ObjectDef] = {}

    for obj_id, prop_wrapper in k.shapeProperties.items():
        sp = prop_wrapper.get("@all")
        if not sp:
            continue
        # class/type
        klass = sp.klass or ""
        mapped = CLASS_MAP.get(klass, klass or "Unknown")
        objects[obj_id] = ObjectDef(name=obj_id, type=mapped)

    # 2) Build frames data grouped by timestamp (string keys)
    frame_objects: DefaultDict[str, Dict[str, FrameObject]] = defaultdict(dict)

    for feature in k.shapes.CAM.features:
        obj_id = feature.id
        # ensure object exists (in case shapeProperties missing)
        if obj_id not in objects:
            # try to infer a default type if absent
            objects[obj_id] = ObjectDef(name=obj_id, type="Unknown")

        # timestamp (OpenLABEL uses string keys for frames)
        ts = str(feature.properties.get(FRAME_KEY, 0))

        # bbox conversion
        assert feature.geometry.type == "ExtremePointBox"
        cx, cy, w, h = extreme_box_to_cxcywh(feature.geometry.coordinates.model_dump())

        bbox = BBox(
            name=f"bbox-{obj_id.split('-')[0]}",
            stream=STREAM_DEFAULT,
            val=[cx, cy, w, h],
        )

        # optional boolean/text from shapeProperties
        prop = k.shapeProperties.get(obj_id, {}).get("@all")
        booleans = []
        texts = []
        if prop and prop.Unclear is not None:
            booleans.append(BooleanEntry(name=UNCLEAR_KEY, val=bool(prop.Unclear)))
        if prop and prop.ObjectType is not None:
            texts.append(TextEntry(name=OBJECT_TYPE_KEY, val=str(prop.ObjectType)))

        obj_data = ObjectData(
            bbox=[bbox],
            boolean=booleans or None,
            text=texts or None,
        )

        frame_objects[ts][obj_id] = FrameObject(object_data=obj_data)

    frames: Dict[str, Frame] = {ts: Frame(objects=objs) for ts, objs in frame_objects.items()}

    root = OpenLabelRoot(
        data={
            "openlabel": OpenLabel(
                objects=objects,
                frames=frames or {"0": Frame(objects={})},
            )
        }
    )
    return root.model_dump()

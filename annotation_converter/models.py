from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

# --- Kognic (simplified) ---

class ExtremePoint(BaseModel):
    coordinates: List[float]  # [x, y]

class ExtremeCoordinates(BaseModel):
    maxX: ExtremePoint
    maxY: ExtremePoint
    minX: ExtremePoint
    minY: ExtremePoint

class Geometry(BaseModel):
    type: str  # "ExtremePointBox"
    coordinates: ExtremeCoordinates

class Feature(BaseModel):
    id: str
    type: str = "Feature"
    geometry: Geometry
    properties: Dict[str, Any] = {}

class FeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[Feature]

class Shapes(BaseModel):
    CAM: FeatureCollection  # for this assignment we only need CAM

class ShapePropertyAll(BaseModel):
    ObjectType: Optional[str] = None
    Unclear: Optional[bool] = None
    klass: Optional[str] = Field(default=None, alias="class")

class KognicAnnotation(BaseModel):
    certainty: Optional[str] = None
    shapeProperties: Dict[str, Dict[str, ShapePropertyAll]]
    shapes: Shapes
    model_config = {"extra": "allow", "populate_by_name": True}

# --- OpenLABEL (simplified to match sample) ---

class BBox(BaseModel):
    name: str
    stream: str
    val: List[float]

class BooleanEntry(BaseModel):
    name: str
    val: bool

class TextEntry(BaseModel):
    name: str
    val: str

class ObjectData(BaseModel):
    bbox: Optional[List[BBox]] = None
    boolean: Optional[List[BooleanEntry]] = None
    text: Optional[List[TextEntry]] = None

class FrameObject(BaseModel):
    object_data: ObjectData

class Frame(BaseModel):
    objects: Dict[str, FrameObject]

class ObjectDef(BaseModel):
    name: str
    type: str

class OpenLabel(BaseModel):
    objects: Dict[str, ObjectDef]
    frames: Dict[str, Frame]

class OpenLabelRoot(BaseModel):
    data: Dict[str, OpenLabel]

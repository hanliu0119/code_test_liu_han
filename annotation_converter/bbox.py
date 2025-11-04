from typing import Tuple, Mapping

def extreme_box_to_cxcywh(coords: Mapping) -> Tuple[float, float, float, float]:
    """
    Kognic 'ExtremePointBox' provides:
      - minX.coordinates = [x, y_at_minX]
      - maxX.coordinates = [x, y_at_maxX]
      - minY.coordinates = [x_at_minY, y]
      - maxY.coordinates = [x_at_maxY, y]
    We compute axis-aligned box:
      w = maxX.x - minX.x
      h = maxY.y - minY.y
      cx = minX.x + w/2
      cy = minY.y + h/2
    """
    min_x = float(coords["minX"]["coordinates"][0])
    max_x = float(coords["maxX"]["coordinates"][0])
    min_y = float(coords["minY"]["coordinates"][1])
    max_y = float(coords["maxY"]["coordinates"][1])

    w = max_x - min_x
    h = max_y - min_y
    cx = min_x + w / 2.0
    cy = min_y + h / 2.0
    return (cx, cy, w, h)

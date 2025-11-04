from fastapi import FastAPI, Body
from annotation_converter import convert

app = FastAPI(title="Kognic → OpenLABEL Converter (simplified)", version="0.1.0")

# Spec asks for GET with a JSON body (unusual but supported).
@app.get("/convert")
def convert_get(kognic: dict = Body(..., description="Kognic-format JSON")) -> dict:
    return convert(kognic)

# Also expose POST for convenience.
# @app.post("/convert")
# def convert_post(kognic: dict = Body(...)) -> dict:
#     return convert(kognic)

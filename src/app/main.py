from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CI/CD Demo", version="0.1.0")

# In-memory store — intentionally simple; the point is to have something to test
_items: list[dict] = []


class Item(BaseModel):
    name: str
    description: str = ""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def list_items():
    return {"items": _items}


@app.get("/items/{name}")
def get_item(name: str):
    for i in _items:
        if i["name"] == name:
            return i
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", status_code=201)
def create_item(item: Item):
    if any(i["name"] == item.name for i in _items):
        raise HTTPException(status_code=409, detail="Item already exists")
    record = item.model_dump()
    _items.append(record)
    return record

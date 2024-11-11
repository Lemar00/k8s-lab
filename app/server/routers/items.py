from fastapi import APIRouter, Depends, HTTPException
from app.server.database import get_db
from asyncpg import Connection
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Pydantic model for Item
class Item(BaseModel):
    name: str

# Get all items from the database
@router.get("/items", response_model=List[Item])
async def get_items(db: Connection = Depends(get_db)):
    try:
        # Fetch all items from the 'items' table
        items = await db.fetch("SELECT * FROM items")
        return [Item(name=row['name']) for row in items]
    except Exception as e:
        # Handle any potential errors during the fetch operation
        raise HTTPException(status_code=500, detail=str(e))

# Create a new item in the database
@router.post("/items", response_model=Item)
async def create_item(item: Item, db: Connection = Depends(get_db)):
    try:
        # Insert the item into the 'items' table and return the created row
        row = await db.fetchrow(
            "INSERT INTO items (name) VALUES ($1) RETURNING *", item.name
        )
        return Item(name=row['name'])
    except Exception as e:
        # Raise an exception if there's an issue during insertion
        raise HTTPException(status_code=500, detail=str(e))

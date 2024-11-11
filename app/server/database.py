import os
import asyncpg
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager

# FastAPI app initialization
app = FastAPI()

# Environment variables for database credentials with default values
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_PORT = int(os.getenv("DB_PORT", 5432))

# Database connection string for reuse
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Function to initialize database connection and create tables if they don't exist
async def init_db():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        """)
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        await conn.close()

# Async context manager for database connections
@asynccontextmanager
async def get_db_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()

# Dependency for database connection, usable in route handlers
async def get_db():
    async with get_db_connection() as conn:
        yield conn

# Example route to add an item to the database
@app.post("/items/")
async def create_item(name: str, db=Depends(get_db)):
    try:
        await db.execute("INSERT INTO items (name) VALUES ($1)", name)
        return {"status": "Item added", "name": name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating item: {e}")

# Example route to retrieve all items
@app.get("/items/")
async def read_items(db=Depends(get_db)):
    try:
        items = await db.fetch("SELECT * FROM items")
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {e}")

# Event handler to initialize the database on startup
@app.on_event("startup")
async def startup():
    await init_db()

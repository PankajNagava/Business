from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json, os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (frontend assets)
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

PRODUCTS_FILE = "backend/products.json"

def load_products():
    with open(PRODUCTS_FILE, "r") as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=4)

@app.get("/products")
def get_products():
    return load_products()

@app.post("/add_product")
def add_product(product: dict):
    products = load_products()
    product["id"] = len(products) + 1
    products.append(product)
    save_products(products)
    return {"message": "Product added"}

@app.post("/delete_product")
def delete_product(product_id: int):
    products = load_products()
    updated = [p for p in products if p["id"] != product_id]
    save_products(updated)
    return {"message": "Product deleted"}

@app.post("/edit_product")
def edit_product(product: dict):
    products = load_products()
    for i, p in enumerate(products):
        if p["id"] == product["id"]:
            products[i] = product
            save_products(products)
            return {"message": "Product updated"}
    raise HTTPException(status_code=404, detail="Product not found")

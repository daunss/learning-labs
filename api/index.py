# tetap my elaina di hati, nim 144 tetep hadir mas
# kalo saya sih mending elaina, sory ngetroll dikit
import os
import uuid
from datetime import datetime
from typing import Optional, List, Any
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="PasarSuara Pintar REST API",
    description="Backend REST API Tugas Akhir Learning Labs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed database memori warung pasar suara
db = {
    "users": [
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "email": "bu.siti@demo.com",
            "phone_number": "628123456001",
            "name": "Bu Siti",
            "role": "umkm",
            "preferred_dialect": "jv",
            "city": "Yogyakarta",
            "created_at": "2026-10-04T08:00:00Z"
        },
        {
            "id": "22222222-2222-2222-2222-222222222222",
            "email": "pak.joyo@demo.com",
            "phone_number": "628123456002",
            "name": "Pak Joyo",
            "role": "supplier",
            "preferred_dialect": "jv",
            "city": "Sleman",
            "created_at": "2026-10-04T08:00:00Z"
        },
        {
            "id": "33333333-3333-3333-3333-333333333333",
            "email": "mang.ujang@demo.com",
            "phone_number": "628123456003",
            "name": "Mang Ujang",
            "role": "umkm",
            "preferred_dialect": "su",
            "city": "Bandung",
            "created_at": "2026-10-04T08:00:00Z"
        }
    ],
    "user_preferences": [
        {
            "id": "p1111111-0000-0000-0000-000000000001",
            "user_id": "11111111-1111-1111-1111-111111111111",
            "language": "jv",
            "currency": "IDR",
            "timezone": "Asia/Jakarta",
            "notification_enabled": True,
            "low_stock_threshold": 10
        },
        {
            "id": "p2222222-0000-0000-0000-000000000001",
            "user_id": "22222222-2222-2222-2222-222222222222",
            "language": "jv",
            "currency": "IDR",
            "timezone": "Asia/Jakarta",
            "notification_enabled": True,
            "low_stock_threshold": 50
        },
        {
            "id": "p3333333-0000-0000-0000-000000000001",
            "user_id": "33333333-3333-3333-3333-333333333333",
            "language": "su",
            "currency": "IDR",
            "timezone": "Asia/Jakarta",
            "notification_enabled": True,
            "low_stock_threshold": 15
        }
    ],
    "inventory": [
        {
            "id": "a1111111-0000-0000-0000-000000000001",
            "user_id": "11111111-1111-1111-1111-111111111111",
            "product_name": "Beras Premium",
            "stock_qty": 25.0,
            "unit": "kg",
            "min_sell_price": 13000.0,
            "max_buy_price": 12000.0,
            "description": "Beras putih kualitas premium warung",
            "created_at": "2026-10-04T08:00:00Z",
            "updated_at": "2026-10-04T08:00:00Z"
        },
        {
            "id": "a1111111-0000-0000-0000-000000000002",
            "user_id": "11111111-1111-1111-1111-111111111111",
            "product_name": "Minyak Goreng",
            "stock_qty": 10.0,
            "unit": "liter",
            "min_sell_price": 18000.0,
            "max_buy_price": 16000.0,
            "description": "Minyak goreng sawit bantal",
            "created_at": "2026-10-04T08:00:00Z",
            "updated_at": "2026-10-04T08:00:00Z"
        },
        {
            "id": "a2222222-0000-0000-0000-000000000001",
            "user_id": "22222222-2222-2222-2222-222222222222",
            "product_name": "Beras IR64 Super",
            "stock_qty": 500.0,
            "unit": "kg",
            "min_sell_price": 11500.0,
            "max_buy_price": None,
            "description": "Beras panen langsung dari sawah",
            "created_at": "2026-10-04T08:00:00Z",
            "updated_at": "2026-10-04T08:00:00Z"
        },
        {
            "id": "a3333333-0000-0000-0000-000000000001",
            "user_id": "33333333-3333-3333-3333-333333333333",
            "product_name": "Cabai Merah",
            "stock_qty": 20.0,
            "unit": "kg",
            "min_sell_price": 45000.0,
            "max_buy_price": 40000.0,
            "description": "Cabai merah keriting segar",
            "created_at": "2026-10-04T08:00:00Z",
            "updated_at": "2026-10-04T08:00:00Z"
        }
    ],
    "transactions": [
        {
            "id": "t1111111-0000-0000-0000-000000000001",
            "user_id": "11111111-1111-1111-1111-111111111111",
            "type": "SALE",
            "product_name": "Nasi Rames",
            "qty": 15.0,
            "price_per_unit": 12000.0,
            "total_amount": 180000.0,
            "raw_voice_text": "Tadi laku nasi rames limolas porsi, rolas ewu siji",
            "created_at": "2026-10-04T09:00:00Z"
        },
        {
            "id": "t1111111-0000-0000-0000-000000000002",
            "user_id": "11111111-1111-1111-1111-111111111111",
            "type": "PURCHASE",
            "product_name": "Beras Premium",
            "qty": 25.0,
            "price_per_unit": 11800.0,
            "total_amount": 295000.0,
            "raw_voice_text": "Tuku beras 25 kilo neng Pak Joyo",
            "created_at": "2026-10-04T10:00:00Z"
        },
        {
            "id": "t1111111-0000-0000-0000-000000000003",
            "user_id": "11111111-1111-1111-1111-111111111111",
            "type": "EXPENSE",
            "product_name": "Gas LPG",
            "qty": 2.0,
            "price_per_unit": 22000.0,
            "total_amount": 44000.0,
            "raw_voice_text": "Beli gas loro tabung",
            "created_at": "2026-10-04T11:00:00Z"
        }
    ],
    "orders": [
        {
            "id": "b1111111-0000-0000-0000-000000000001",
            "buyer_id": "11111111-1111-1111-1111-111111111111",
            "seller_id": "22222222-2222-2222-2222-222222222222",
            "order_number": "ORD-20261004-001",
            "status": "DELIVERED",
            "total_amount": 295000.0,
            "notes": "Kulakan Beras IR64 via negosiasi AI",
            "created_at": "2026-10-04T07:40:00Z",
            "updated_at": "2026-10-04T08:00:00Z"
        }
    ],
    "order_items": [
        {
            "id": "oi111111-0000-0000-0000-000000000001",
            "order_id": "b1111111-0000-0000-0000-000000000001",
            "inventory_id": "a2222222-0000-0000-0000-000000000001",
            "product_name": "Beras IR64 Super",
            "quantity": 25.0,
            "unit_price": 11800.0,
            "subtotal": 295000.0,
            "created_at": "2026-10-04T07:40:00Z"
        }
    ],
    "negotiation_logs": [
        {
            "id": "n1111111-0000-0000-0000-000000000001",
            "buyer_id": "11111111-1111-1111-1111-111111111111",
            "seller_id": "22222222-2222-2222-2222-222222222222",
            "product_name": "Beras IR64 Super",
            "initial_offer": 12000.0,
            "final_price": 11800.0,
            "status": "SUCCESS",
            "transcript": {
                "messages": [
                    {"role": "buyer_agent", "content": "Bisa 11.800/kg?"},
                    {"role": "seller_agent", "content": "Deal 11.800/kg"}
                ]
            },
            "created_at": "2026-10-04T07:30:00Z",
            "completed_at": "2026-10-04T07:35:00Z"
        }
    ],
    "notifications": [
        {
            "id": "m1111111-0000-0000-0000-000000000001",
            "user_id": "11111111-1111-1111-1111-111111111111",
            "type": "transaction",
            "title": "Transaksi Baru",
            "message": "Transaksi SALE sebesar Rp 180000 telah dicatat",
            "read": True,
            "created_at": "2026-10-04T09:01:00Z"
        },
        {
            "id": "m1111111-0000-0000-0000-000000000002",
            "user_id": "11111111-1111-1111-1111-111111111111",
            "type": "inventory",
            "title": "Stok Menipis",
            "message": "Produk Minyak Goreng tinggal 10 liter",
            "read": False,
            "created_at": "2026-10-04T09:05:00Z"
        }
    ]
}

# Schemas
class InventoryCreate(BaseModel):
    user_id: str
    product_name: str
    stock_qty: float = 0.0
    unit: str = "kg"
    min_sell_price: float
    max_buy_price: Optional[float] = None
    description: Optional[str] = ""

class InventoryUpdate(BaseModel):
    product_name: str
    stock_qty: float
    unit: str = "kg"
    min_sell_price: float
    max_buy_price: Optional[float] = None
    description: Optional[str] = ""

class InventoryPatch(BaseModel):
    product_name: Optional[str] = None
    stock_qty: Optional[float] = None
    unit: Optional[str] = None
    min_sell_price: Optional[float] = None
    max_buy_price: Optional[float] = None
    description: Optional[str] = None

class TransactionCreate(BaseModel):
    user_id: str
    type: str
    product_name: Optional[str] = None
    qty: Optional[float] = None
    price_per_unit: Optional[float] = None
    total_amount: Optional[float] = None
    raw_voice_text: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    phone_number: str
    email: Optional[str] = None
    role: str = "umkm"
    preferred_dialect: str = "id"
    city: Optional[str] = None

class OrderItemInput(BaseModel):
    inventory_id: str
    product_name: str
    quantity: float
    unit_price: float

class OrderCreate(BaseModel):
    buyer_id: str
    seller_id: str
    notes: Optional[str] = ""
    items: List[OrderItemInput]

class OrderStatusUpdate(BaseModel):
    status: str

class NegotiationCreate(BaseModel):
    buyer_id: Optional[str] = None
    seller_id: Optional[str] = None
    product_name: str
    initial_offer: float
    final_price: Optional[float] = None
    status: str = "PENDING"
    transcript: Optional[dict] = None

@app.get("/")
def read_root():
    return {
        "pesan": "tetap my elaina di hati mas, sory ngetroll dikit",
        "project": "PasarSuara Pintar REST API",
        "nim": "21114012610144",
        "status": "online",
        "docs": "/docs",
        "endpoints": {
            "inventory": [
                "GET /api/inventory",
                "GET /api/inventory/{id}",
                "POST /api/inventory",
                "PUT /api/inventory/{id}",
                "PATCH /api/inventory/{id}",
                "DELETE /api/inventory/{id}"
            ],
            "transactions": [
                "GET /api/transactions",
                "GET /api/transactions/{id}",
                "POST /api/transactions"
            ],
            "users": [
                "GET /api/users",
                "GET /api/users/{id}",
                "POST /api/users"
            ],
            "orders": [
                "GET /api/orders",
                "GET /api/orders/{id}",
                "POST /api/orders",
                "PATCH /api/orders/{id}/status"
            ],
            "negotiations": [
                "GET /api/negotiations",
                "POST /api/negotiations"
            ],
            "notifications": [
                "GET /api/notifications",
                "PATCH /api/notifications/{id}/read"
            ],
            "system": [
                "GET /api/health",
                "GET /api/stats"
            ]
        }
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "sehat walafiat mas",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "In-Memory Store (Aman Sentosa)"
    }

@app.get("/api/stats")
def get_stats():
    total_sales = sum(t["total_amount"] for t in db["transactions"] if t["type"] == "SALE" and t.get("total_amount"))
    total_purchases = sum(t["total_amount"] for t in db["transactions"] if t["type"] == "PURCHASE" and t.get("total_amount"))
    return {
        "success": True,
        "data": {
            "total_users": len(db["users"]),
            "total_inventory_items": len(db["inventory"]),
            "total_transactions": len(db["transactions"]),
            "total_orders": len(db["orders"]),
            "financial_summary": {
                "total_sales_amount": total_sales,
                "total_purchases_amount": total_purchases,
                "currency": "IDR"
            }
        }
    }

# INVENTORY (CRUD Utama)
@app.get("/api/inventory")
def get_inventory(user_id: Optional[str] = None, search: Optional[str] = None, low_stock: Optional[bool] = False):
    items = []
    for item in db["inventory"]:
        owner = next((u for u in db["users"] if u["id"] == item["user_id"]), None)
        item_copy = {**item, "owner_name": owner["name"] if owner else None}
        items.append(item_copy)

    if user_id:
        items = [i for i in items if i["user_id"] == user_id]
    if search:
        s = search.lower()
        items = [i for i in items if s in i["product_name"].lower()]
    if low_stock:
        items = [i for i in items if i["stock_qty"] <= 10]

    return {
        "success": True,
        "message": "data barang beres ditarik mas",
        "total": len(items),
        "data": items
    }

@app.get("/api/inventory/{item_id}")
def get_single_inventory(item_id: str):
    item = next((i for i in db["inventory"] if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Barang ID '{item_id}' gak ketemu mas")
    owner = next((u for u in db["users"] if u["id"] == item["user_id"]), None)
    return {
        "success": True,
        "data": {**item, "owner_name": owner["name"] if owner else None, "owner_city": owner.get("city") if owner else None}
    }

@app.post("/api/inventory", status_code=status.HTTP_201_CREATED)
def create_inventory(item: InventoryCreate):
    new_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    new_item = {
        "id": new_id,
        "user_id": item.user_id,
        "product_name": item.product_name.strip(),
        "stock_qty": float(item.stock_qty),
        "unit": item.unit,
        "min_sell_price": float(item.min_sell_price),
        "max_buy_price": float(item.max_buy_price) if item.max_buy_price is not None else None,
        "description": item.description or "",
        "created_at": now,
        "updated_at": now
    }
    db["inventory"].insert(0, new_item)
    return {
        "success": True,
        "message": "barang baru berhasil masuk warung mas",
        "data": new_item
    }

@app.put("/api/inventory/{item_id}")
def update_inventory_full(item_id: str, item: InventoryUpdate):
    idx = next((i for i, x in enumerate(db["inventory"]) if x["id"] == item_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Barang ID '{item_id}' gak ketemu mas")
    
    current = db["inventory"][idx]
    now = datetime.utcnow().isoformat()
    current.update({
        "product_name": item.product_name.strip(),
        "stock_qty": float(item.stock_qty),
        "unit": item.unit,
        "min_sell_price": float(item.min_sell_price),
        "max_buy_price": float(item.max_buy_price) if item.max_buy_price is not None else None,
        "description": item.description or "",
        "updated_at": now
    })
    return {
        "success": True,
        "message": "barang sukses diupdate full mas",
        "data": current
    }

@app.patch("/api/inventory/{item_id}")
def patch_inventory(item_id: str, patch_data: InventoryPatch):
    idx = next((i for i, x in enumerate(db["inventory"]) if x["id"] == item_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Barang ID '{item_id}' gak ketemu mas")

    current = db["inventory"][idx]
    fields = patch_data.model_dump(exclude_unset=True)
    if not fields:
        raise HTTPException(status_code=400, detail="gaada field yang mau diupdate mas")

    for k, v in fields.items():
        if v is not None:
            current[k] = v
    current["updated_at"] = datetime.utcnow().isoformat()

    return {
        "success": True,
        "message": "stok/harga barang beres diupdate mas",
        "data": current
    }

@app.delete("/api/inventory/{item_id}")
def delete_inventory(item_id: str):
    idx = next((i for i, x in enumerate(db["inventory"]) if x["id"] == item_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Barang ID '{item_id}' gak ketemu mas")

    db["inventory"].pop(idx)
    return {
        "success": True,
        "message": f"barang '{item_id}' udah dibabat mas"
    }

# TRANSACTIONS
@app.get("/api/transactions")
def get_transactions(user_id: Optional[str] = None, type: Optional[str] = None):
    txs = db["transactions"]
    if user_id:
        txs = [t for t in txs if t["user_id"] == user_id]
    if type:
        txs = [t for t in txs if t["type"].upper() == type.upper()]
    return {
        "success": True,
        "message": "buku kas beres ditarik mas",
        "total": len(txs),
        "data": txs
    }

@app.get("/api/transactions/{tx_id}")
def get_single_transaction(tx_id: str):
    tx = next((t for t in db["transactions"] if t["id"] == tx_id), None)
    if not tx:
        raise HTTPException(status_code=404, detail=f"Transaksi ID '{tx_id}' gak ketemu mas")
    return {"success": True, "data": tx}

@app.post("/api/transactions", status_code=status.HTTP_201_CREATED)
def create_transaction(tx: TransactionCreate):
    valid_types = ["SALE", "PURCHASE", "EXPENSE"]
    tx_type = tx.type.upper()
    if tx_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"tipe transaksi harus: {', '.join(valid_types)} mas")

    total = tx.total_amount
    if total is None:
        if tx.qty and tx.price_per_unit:
            total = float(tx.qty) * float(tx.price_per_unit)
        else:
            raise HTTPException(status_code=400, detail="isi total_amount atau qty sama harga satuan mas")

    new_tx = {
        "id": str(uuid.uuid4()),
        "user_id": tx.user_id,
        "type": tx_type,
        "product_name": tx.product_name,
        "qty": float(tx.qty) if tx.qty else None,
        "price_per_unit": float(tx.price_per_unit) if tx.price_per_unit else None,
        "total_amount": float(total),
        "raw_voice_text": tx.raw_voice_text,
        "created_at": datetime.utcnow().isoformat()
    }
    db["transactions"].insert(0, new_tx)

    # auto update stok
    if tx.product_name and tx.qty:
        inv = next((i for i in db["inventory"] if i["user_id"] == tx.user_id and i["product_name"].lower() == tx.product_name.lower()), None)
        if inv:
            if tx_type == "SALE":
                inv["stock_qty"] = max(0.0, inv["stock_qty"] - float(tx.qty))
            elif tx_type == "PURCHASE":
                inv["stock_qty"] += float(tx.qty)

    return {
        "success": True,
        "message": f"transaksi {tx_type} beres dicatat ke buku kas mas",
        "data": new_tx
    }

# USERS
@app.get("/api/users")
def get_users():
    users = []
    for u in db["users"]:
        pref = next((p for p in db["user_preferences"] if p["user_id"] == u["id"]), None)
        users.append({**u, "preferences": pref})
    return {
        "success": True,
        "message": "list pedagang beres diambil mas",
        "total": len(users),
        "data": users
    }

@app.get("/api/users/{user_id}")
def get_user_detail(user_id: str):
    u = next((x for x in db["users"] if x["id"] == user_id), None)
    if not u:
        raise HTTPException(status_code=404, detail=f"User ID '{user_id}' gak ketemu mas")
    pref = next((p for p in db["user_preferences"] if p["user_id"] == u["id"]), None)
    inv = [i for i in db["inventory"] if i["user_id"] == u["id"]]
    return {
        "success": True,
        "data": {**u, "preferences": pref, "inventory_count": len(inv), "inventory": inv}
    }

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    new_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    new_user = {
        "id": new_id,
        "name": user.name.strip(),
        "phone_number": user.phone_number.strip(),
        "email": user.email,
        "role": user.role,
        "preferred_dialect": user.preferred_dialect,
        "city": user.city,
        "created_at": now
    }
    db["users"].append(new_user)
    db["user_preferences"].append({
        "id": str(uuid.uuid4()),
        "user_id": new_id,
        "language": user.preferred_dialect,
        "currency": "IDR",
        "timezone": "Asia/Jakarta",
        "notification_enabled": True,
        "low_stock_threshold": 10
    })
    return {
        "success": True,
        "message": "member baru resmi gabung mas",
        "data": new_user
    }

# ORDERS (N:N Junction Table)
@app.get("/api/orders")
def get_orders():
    orders = []
    for o in db["orders"]:
        buyer = next((u for u in db["users"] if u["id"] == o["buyer_id"]), None)
        seller = next((u for u in db["users"] if u["id"] == o["seller_id"]), None)
        items = [oi for oi in db["order_items"] if oi["order_id"] == o["id"]]
        orders.append({
            **o,
            "buyer_name": buyer["name"] if buyer else None,
            "seller_name": seller["name"] if seller else None,
            "items": items
        })
    return {
        "success": True,
        "message": "semua orderan beres ditarik mas",
        "total": len(orders),
        "data": orders
    }

@app.get("/api/orders/{order_id}")
def get_order_detail(order_id: str):
    o = next((x for x in db["orders"] if x["id"] == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail=f"Order ID '{order_id}' gak ketemu mas")
    buyer = next((u for u in db["users"] if u["id"] == o["buyer_id"]), None)
    seller = next((u for u in db["users"] if u["id"] == o["seller_id"]), None)
    items = [oi for oi in db["order_items"] if oi["order_id"] == o["id"]]
    return {
        "success": True,
        "data": {
            **o,
            "buyer_name": buyer["name"] if buyer else None,
            "seller_name": seller["name"] if seller else None,
            "items": items
        }
    }

@app.post("/api/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    if not order.items:
        raise HTTPException(status_code=400, detail="keranjang belanjaannya kosong melompong mas")

    order_id = str(uuid.uuid4())
    order_num = f"ORD-{int(datetime.utcnow().timestamp())}"
    now = datetime.utcnow().isoformat()

    total_amount = 0.0
    prepared_items = []
    for itm in order.items:
        subtotal = float(itm.quantity) * float(itm.unit_price)
        total_amount += subtotal
        prepared_items.append({
            "id": str(uuid.uuid4()),
            "order_id": order_id,
            "inventory_id": itm.inventory_id,
            "product_name": itm.product_name,
            "quantity": float(itm.quantity),
            "unit_price": float(itm.unit_price),
            "subtotal": subtotal,
            "created_at": now
        })

    new_order = {
        "id": order_id,
        "buyer_id": order.buyer_id,
        "seller_id": order.seller_id,
        "order_number": order_num,
        "status": "PENDING",
        "total_amount": total_amount,
        "notes": order.notes or "",
        "created_at": now,
        "updated_at": now
    }
    db["orders"].insert(0, new_order)
    db["order_items"].extend(prepared_items)

    return {
        "success": True,
        "message": f"order {order_num} berhasil dibuat mas",
        "data": {**new_order, "items": prepared_items}
    }

@app.patch("/api/orders/{order_id}/status")
def update_order_status(order_id: str, status_data: OrderStatusUpdate):
    o = next((x for x in db["orders"] if x["id"] == order_id), None)
    if not o:
        raise HTTPException(status_code=404, detail=f"Order ID '{order_id}' gak ketemu mas")

    valid_statuses = ["PENDING", "CONFIRMED", "DELIVERED", "CANCELLED"]
    s = status_data.status.upper()
    if s not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"status tidak valid mas, pilihan: {', '.join(valid_statuses)}")

    o["status"] = s
    o["updated_at"] = datetime.utcnow().isoformat()
    return {
        "success": True,
        "message": f"status order sukses jadi {s} mas",
        "data": o
    }

# NEGOTIATIONS
@app.get("/api/negotiations")
def get_negotiations():
    logs = []
    for n in db["negotiation_logs"]:
        buyer = next((u for u in db["users"] if u["id"] == n["buyer_id"]), None)
        seller = next((u for u in db["users"] if u["id"] == n["seller_id"]), None)
        logs.append({
            **n,
            "buyer_name": buyer["name"] if buyer else None,
            "seller_name": seller["name"] if seller else None
        })
    return {
        "success": True,
        "message": "data negosiasi beres ditarik mas",
        "total": len(logs),
        "data": logs
    }

@app.post("/api/negotiations", status_code=status.HTTP_201_CREATED)
def create_negotiation(neg: NegotiationCreate):
    now = datetime.utcnow().isoformat()
    new_neg = {
        "id": str(uuid.uuid4()),
        "buyer_id": neg.buyer_id,
        "seller_id": neg.seller_id,
        "product_name": neg.product_name,
        "initial_offer": float(neg.initial_offer),
        "final_price": float(neg.final_price) if neg.final_price is not None else None,
        "status": neg.status.upper(),
        "transcript": neg.transcript or {},
        "created_at": now,
        "completed_at": now if neg.status.upper() == "SUCCESS" else None
    }
    db["negotiation_logs"].insert(0, new_neg)
    return {
        "success": True,
        "message": "ronde tawar menawar berhasil disimpan mas",
        "data": new_neg
    }

# NOTIFICATIONS
@app.get("/api/notifications")
def get_notifications(user_id: Optional[str] = None, unread: Optional[bool] = False):
    notifs = db["notifications"]
    if user_id:
        notifs = [n for n in notifs if n["user_id"] == user_id]
    if unread:
        notifs = [n for n in notifs if not n["read"]]
    return {
        "success": True,
        "message": "notifikasi beres diambil mas",
        "total": len(notifs),
        "data": notifs
    }

@app.patch("/api/notifications/{notif_id}/read")
def mark_notification_read(notif_id: str):
    notif = next((n for n in db["notifications"] if n["id"] == notif_id), None)
    if not notif:
        raise HTTPException(status_code=404, detail=f"Notifikasi ID '{notif_id}' gak ketemu mas")
    notif["read"] = True
    return {
        "success": True,
        "message": "notifikasi udah dibaca mas, aman",
        "data": notif
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 3000))
    print(f"gas nyala di port {port} mas, santai ga bakal meledak")
    uvicorn.run("api.index:app", host="0.0.0.0", port=port, reload=True)

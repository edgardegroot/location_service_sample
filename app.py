from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Customer Delivery Location Service")

CUSTOMERS = {
    "Mueller": {"address": "DHL Packstation 101, Amsinckstraße 28, 20097 Hamburg", "delivery_date": "2025-02-20"},
    "Schmidt": {"address": "DHL Paketshop, Landsberger Allee 171, 10369 Berlin", "delivery_date": "2025-02-21"},
    "Weber": {"address": "DHL Freight Center, Am Nordkanal 1, 41236 Mönchengladbach", "delivery_date": "2025-02-22"},
    # … rest unchanged …
}

class DeliveryResponse(BaseModel):
    customer_name: str
    delivery_address: str
    delivery_date: str

@app.get("/delivery/{customer_name}", response_model=DeliveryResponse)
def get_delivery(customer_name: str):
    if customer_name not in CUSTOMERS:
        raise HTTPException(status_code=404, detail=f"Customer '{customer_name}' not found")
    info = CUSTOMERS[customer_name]
    return DeliveryResponse(
        customer_name=customer_name,
        delivery_address=info["address"],
        delivery_date=info["delivery_date"],
    )

@app.get("/customers")
def list_customers():
    return {"customers": list(CUSTOMERS.keys())}
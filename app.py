from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import date, timedelta
import random

app = FastAPI(title="Customer Delivery Location Service")

# ----------------------------
# Delivery date configuration
# ----------------------------
START_DATE = date(2026, 3, 4)
END_DATE = date(2026, 3, 8)

def random_delivery_date():
    delta_days = (END_DATE - START_DATE).days
    return (START_DATE + timedelta(days=random.randint(0, delta_days))).isoformat()

# ----------------------------
# Customer data
# ----------------------------
CUSTOMERS = {
    "Mueller": {"last_location": "DHL Packstation 101, Amsinckstraße 28, 20097 Hamburg"},
    "Schmidt": {"last_location": "DHL Paketshop, Landsberger Allee 171, 10369 Berlin"},
    "Weber": {"last_location": "DHL Freight Center, Am Nordkanal 1, 41236 Mönchengladbach"},
    "Fischer": {"last_location": "DHL Packstation 102, Zeppelinstraße 1, 70372 Stuttgart"},
    "Bauer": {"last_location": "DHL Zustellbasis, Industriestraße 20, 80339 München"},
    "Schneider": {"last_location": "DHL Paketzentrum, Carl-Benz-Straße 9, 60386 Frankfurt am Main"},
    "Hoffmann": {"last_location": "DHL Packstation 103, Venloer Straße 383, 50825 Köln"},
    "Koch": {"last_location": "DHL Paketshop, Königstraße 27, 90402 Nürnberg"},
    "Richter": {"last_location": "DHL Freight Center, Huckarder Straße 111, 44147 Dortmund"},
    "Klein": {"last_location": "DHL Packstation 104, Willy-Brandt-Platz 3, 45127 Essen"},
    "Wolf": {"last_location": "DHL Zustellbasis, Nürnberger Straße 91, 01187 Dresden"},
    "Neumann": {"last_location": "DHL Packstation 105, Schloßstraße 20, 12163 Berlin"},
    "Braun": {"last_location": "DHL Paketshop, Marktplatz 8, 76133 Karlsruhe"},
    "Zimmermann": {"last_location": "DHL Freight Center, Lise-Meitner-Straße 5, 30179 Hannover"},
    "Hartmann": {"last_location": "DHL Packstation 106, Bismarckstraße 10, 04109 Leipzig"},
    "Meier": {"last_location": "DHL Paketshop, Leopoldstraße 64, 80802 München"},
    "Degroot": {"last_location": "DHL Paketshop, Coolsingel 45, 3012 AD Rotterdam"},
    "Edgar": {"last_location": "DHL Packstation 102, Zeppelinstraße 1, 70372 Stuttgart"},
}

# Attach random delivery dates
for customer in CUSTOMERS.values():
    customer["delivery_date"] = random_delivery_date()

# ----------------------------
# API response model
# ----------------------------
class DeliveryResponse(BaseModel):
    customer_name: str
    last_location: str
    delivery_date: str

# ----------------------------
# API endpoints
# ----------------------------
@app.get("/delivery", response_model=DeliveryResponse)
@app.get("/delivery/", response_model=DeliveryResponse)
def get_delivery(
    customer_name: str = Query(..., description="Customer name")
):
    normalized = customer_name.strip().lower()

    for name, info in CUSTOMERS.items():
        if name.lower() == normalized:
            return DeliveryResponse(
                customer_name=name,
                last_location=info["last_location"],
                delivery_date=info["delivery_date"],
            )

    raise HTTPException(
        status_code=404,
        detail=f"Customer '{customer_name}' not found"
    )

@app.get("/customers")
def list_customers():
    return {"customers": list(CUSTOMERS.keys())}
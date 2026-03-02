from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, timedelta
import random

app = FastAPI(title="Customer Delivery Location Service")

# Allowed delivery date range
START_DATE = date(2026, 3, 4)
END_DATE = date(2026, 3, 8)

def random_delivery_date():
    delta_days = (END_DATE - START_DATE).days
    return (START_DATE + timedelta(days=random.randint(0, delta_days))).isoformat()

CUSTOMERS = {
    "Mueller": {"address": "DHL Packstation 101, Amsinckstraße 28, 20097 Hamburg"},
    "Schmidt": {"address": "DHL Paketshop, Landsberger Allee 171, 10369 Berlin"},
    "Weber": {"address": "DHL Freight Center, Am Nordkanal 1, 41236 Mönchengladbach"},
    "Fischer": {"address": "DHL Packstation 102, Zeppelinstraße 1, 70372 Stuttgart"},
    "Bauer": {"address": "DHL Zustellbasis, Industriestraße 20, 80339 München"},
    "Schneider": {"address": "DHL Paketzentrum, Carl-Benz-Straße 9, 60386 Frankfurt am Main"},
    "Hoffmann": {"address": "DHL Packstation 103, Venloer Straße 383, 50825 Köln"},
    "Koch": {"address": "DHL Paketshop, Königstraße 27, 90402 Nürnberg"},
    "Richter": {"address": "DHL Freight Center, Huckarder Straße 111, 44147 Dortmund"},
    "Klein": {"address": "DHL Packstation 104, Willy-Brandt-Platz 3, 45127 Essen"},
    "Wolf": {"address": "DHL Zustellbasis, Nürnberger Straße 91, 01187 Dresden"},
    "Neumann": {"address": "DHL Packstation 105, Schloßstraße 20, 12163 Berlin"},
    "Braun": {"address": "DHL Paketshop, Marktplatz 8, 76133 Karlsruhe"},
    "Zimmermann": {"address": "DHL Freight Center, Lise-Meitner-Straße 5, 30179 Hannover"},
    "Hartmann": {"address": "DHL Packstation 106, Bismarckstraße 10, 04109 Leipzig"},
    "Meier": {"address": "DHL Paketshop, Leopoldstraße 64, 80802 München"},
    "Degroot": {"address": "DHL Paketshop, Coolsingel 45, 3012 AD Rotterdam"},
}

# Attach random delivery dates (within the range)
for customer in CUSTOMERS.values():
    customer["delivery_date"] = random_delivery_date()


class DeliveryResponse(BaseModel):
    customer_name: str
    delivery_address: str
    delivery_date: str


@app.get("/delivery/", response_model=DeliveryResponse)
def get_delivery(customer_name: str = Query(..., description="Name of the customer")):
    if customer_name not in CUSTOMERS:
        raise HTTPException(status_code=404, detail=f"Customer '{customer_name}' not found")
    info = CUSTOMERS[customer_name]
    return DeliveryResponse(
        customer_name=customer_name,
        last_location=info["address"],
        delivery_date=info["delivery_date"],
    )


@app.get("/customers")
def list_customers():
    return {"customers": list(CUSTOMERS.keys())}
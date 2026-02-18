from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import random

app = FastAPI(title="Customer Delivery Location Service")

CUSTOMERS = {
    "Mueller": {"address": "DHL Packstation 101, Amsinckstraße 28, 20097 Hamburg", "delivery_date": "2025-02-20"},
    "Schmidt": {"address": "DHL Paketshop, Landsberger Allee 171, 10369 Berlin", "delivery_date": "2025-02-21"},
    "Weber": {"address": "DHL Freight Center, Am Nordkanal 1, 41236 Mönchengladbach", "delivery_date": "2025-02-22"},
    "Fischer": {"address": "DHL Packstation 102, Zeppelinstraße 1, 70372 Stuttgart", "delivery_date": "2025-02-23"},
    "Bauer": {"address": "DHL Zustellbasis, Industriestraße 20, 80339 München", "delivery_date": "2025-02-24"},
    "Schneider": {"address": "DHL Paketzentrum, Carl-Benz-Straße 9, 60386 Frankfurt am Main", "delivery_date": "2025-02-20"},
    "Hoffmann": {"address": "DHL Packstation 103, Venloer Straße 383, 50825 Köln", "delivery_date": "2025-02-21"},
    "Koch": {"address": "DHL Paketshop, Königstraße 27, 90402 Nürnberg", "delivery_date": "2025-02-22"},
    "Richter": {"address": "DHL Freight Center, Huckarder Straße 111, 44147 Dortmund", "delivery_date": "2025-02-23"},
    "Klein": {"address": "DHL Packstation 104, Willy-Brandt-Platz 3, 45127 Essen", "delivery_date": "2025-02-24"},
    "Wolf": {"address": "DHL Zustellbasis, Nürnberger Straße 91, 01187 Dresden", "delivery_date": "2025-02-20"},
    "Schroeder": {"address": "DHL Paketzentrum, Hansestraße 12, 28217 Bremen", "delivery_date": "2025-02-21"},
    "Neumann": {"address": "DHL Packstation 105, Schloßstraße 20, 12163 Berlin", "delivery_date": "2025-02-22"},
    "Braun": {"address": "DHL Paketshop, Marktplatz 8, 76133 Karlsruhe", "delivery_date": "2025-02-23"},
    "Zimmermann": {"address": "DHL Freight Center, Lise-Meitner-Straße 5, 30179 Hannover", "delivery_date": "2025-02-24"},
    "Hartmann": {"address": "DHL Packstation 106, Bismarckstraße 10, 04109 Leipzig", "delivery_date": "2025-02-20"},
    "Krueger": {"address": "DHL Zustellbasis, Hammer Landstraße 45, 20537 Hamburg", "delivery_date": "2025-02-21"},
    "Lange": {"address": "DHL Paketzentrum, Konrad-Adenauer-Ufer 3, 50668 Köln", "delivery_date": "2025-02-22"},
    "Werner": {"address": "DHL Packstation 107, Bahnhofstraße 15, 47051 Duisburg", "delivery_date": "2025-02-23"},
    "Meier": {"address": "DHL Paketshop, Leopoldstraße 64, 80802 München", "delivery_date": "2025-02-24"},
    "Lehmann": {"address": "DHL Freight Center, Stresemannstraße 78, 10963 Berlin", "delivery_date": "2025-02-20"},
    "Schmitz": {"address": "DHL Packstation 108, Friedrichstraße 50, 40217 Düsseldorf", "delivery_date": "2025-02-21"},
    "Schulze": {"address": "DHL Zustellbasis, Magdeburger Straße 22, 06112 Halle (Saale)", "delivery_date": "2025-02-22"},
    "Maier": {"address": "DHL Paketzentrum, Ulmer Straße 68, 86154 Augsburg", "delivery_date": "2025-02-23"},
    "Berger": {"address": "DHL Packstation 109, Kaiserstraße 29, 55116 Mainz", "delivery_date": "2025-02-24"},
    "Koenig": {"address": "DHL Paketshop, Ernst-Reuter-Platz 2, 10587 Berlin", "delivery_date": "2025-02-20"},
    "Huber": {"address": "DHL Freight Center, Rosenheimer Straße 30, 83022 Rosenheim", "delivery_date": "2025-02-21"},
    "Kaiser": {"address": "DHL Packstation 110, Hohenzollernring 72, 50672 Köln", "delivery_date": "2025-02-22"},
    "Fuchs": {"address": "DHL Zustellbasis, Berliner Straße 33, 69120 Heidelberg", "delivery_date": "2025-02-23"},
    "Peters": {"address": "DHL Paketzentrum, Bürgermeister-Smidt-Straße 41, 28195 Bremen", "delivery_date": "2025-02-24"},
    "Lang": {"address": "DHL Packstation 111, Prinzregentenstraße 7, 86150 Augsburg", "delivery_date": "2025-02-20"},
    "Jung": {"address": "DHL Paketshop, Kurfürstendamm 195, 10707 Berlin", "delivery_date": "2025-02-21"},
    "Scholz": {"address": "DHL Freight Center, Siemensstraße 20, 42551 Velbert", "delivery_date": "2025-02-22"},
    "Roth": {"address": "DHL Packstation 112, Bahnhofsplatz 1, 97070 Würzburg", "delivery_date": "2025-02-23"},
    "Frank": {"address": "DHL Zustellbasis, Theodor-Heuss-Straße 6, 38122 Braunschweig", "delivery_date": "2025-02-24"},
    "Friedrich": {"address": "DHL Paketzentrum, Robert-Bosch-Straße 10, 64293 Darmstadt", "delivery_date": "2025-02-20"},
    "Beck": {"address": "DHL Packstation 113, Marienstraße 5, 30171 Hannover", "delivery_date": "2025-02-21"},
    "Guenther": {"address": "DHL Paketshop, Hafenstraße 18, 48153 Münster", "delivery_date": "2025-02-22"},
    "Vogel": {"address": "DHL Freight Center, Flughafenstraße 21, 70629 Stuttgart", "delivery_date": "2025-02-23"},
    "Winkler": {"address": "DHL Packstation 114, Steinweg 3, 07743 Jena", "delivery_date": "2025-02-24"},
    "Lorenz": {"address": "DHL Zustellbasis, Industriepark 12, 56218 Mülheim-Kärlich", "delivery_date": "2025-02-20"},
    "Baumann": {"address": "DHL Paketzentrum, Dieselstraße 4, 85748 Garching bei München", "delivery_date": "2025-02-21"},
    "Seidel": {"address": "DHL Packstation 115, Poststraße 11, 08056 Zwickau", "delivery_date": "2025-02-22"},
    "Brandt": {"address": "DHL Paketshop, Am Wall 135, 28195 Bremen", "delivery_date": "2025-02-23"},
    "Hahn": {"address": "DHL Freight Center, Schillerstraße 14, 99096 Erfurt", "delivery_date": "2025-02-24"},
    "Keller": {"address": "DHL Packstation 116, Rheinstraße 45, 55218 Ingelheim am Rhein", "delivery_date": "2025-02-20"},
    "Pohl": {"address": "DHL Zustellbasis, Gewerbepark 7, 09648 Mittweida", "delivery_date": "2025-02-21"},
    "Vogt": {"address": "DHL Paketzentrum, Gutenbergstraße 9, 24118 Kiel", "delivery_date": "2025-02-22"},
    "Sauer": {"address": "DHL Packstation 117, Ludwigstraße 21, 93047 Regensburg", "delivery_date": "2025-02-23"},
    "Arnold": {"address": "DHL Paketshop, Große Straße 42, 49074 Osnabrück", "delivery_date": "2025-02-24"},
}


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
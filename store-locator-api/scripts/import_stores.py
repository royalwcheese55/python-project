import csv
from app.db.database import SessionLocal
from app.models.store import Store

CSV_PATH = "data/stores_50.csv"

def import_stores():
    db = SessionLocal()
    created = 0
    updated = 0

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            store = db.query(Store).filter(
                Store.store_id == row["store_id"]
            ).first()

            if store:
                updated += 1
            else:
                store = Store(store_id=row["store_id"])
                db.add(store)
                created += 1

            store.name = row["name"]
            store.store_type = row["store_type"]
            store.status = row["status"]
            store.latitude = float(row["latitude"])
            store.longitude = float(row["longitude"])

            store.address_street = row["address_street"]
            store.address_city = row["address_city"]
            store.address_state = row["address_state"]
            store.address_postal_code = row["address_postal_code"]
            store.address_country = row["address_country"]

            store.phone = row["phone"]
            store.services = row["services"]

            store.hours_mon = row["hours_mon"]
            store.hours_tue = row["hours_tue"]
            store.hours_wed = row["hours_wed"]
            store.hours_thu = row["hours_thu"]
            store.hours_fri = row["hours_fri"]
            store.hours_sat = row["hours_sat"]
            store.hours_sun = row["hours_sun"]

        db.commit()
        db.close()

    print(f"Import complete → created: {created}, updated: {updated}")

if __name__ == "__main__":
    import_stores()
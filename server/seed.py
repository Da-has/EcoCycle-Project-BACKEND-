from app import app
from models import db, User, WasteItem, ExchangeRequest

def seed_data():
    with app.app_context():   # ✅ REQUIRED
        print("🌱 Seeding database...")

        ExchangeRequest.query.delete()
        WasteItem.query.delete()
        User.query.delete()

        producer = User(
            name="Green Farms Ltd",
            email="producer@ecocycle.com",
            role="producer"
        )

        recycler = User(
            name="Eco Recyclers",
            email="recycler@ecocycle.com",
            role="recycler"
        )

        db.session.add_all([producer, recycler])
        db.session.commit()

        plastic = WasteItem(
            name="Plastic Bottles",
            category="plastic",
            quantity=120,
            unit="kg",
            location="Nairobi",
            user_id=producer.id
        )

        db.session.add(plastic)
        db.session.commit()

        request = ExchangeRequest(
            status="pending",
            user_id=recycler.id,
            waste_item_id=plastic.id
        )

        db.session.add(request)
        db.session.commit()

        print("✅ Done!")

if __name__ == "__main__":
    seed_data()

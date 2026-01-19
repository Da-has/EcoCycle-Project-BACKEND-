from app import app
from models import db, Industry, Waste, WasteRequest

with app.app_context():
    print("Clearing database...")

    WasteRequest.query.delete()
    Waste.query.delete()
    Industry.query.delete()
    db.session.commit()

    print("Seeding industries...")

    industries = [
        Industry(name="EcoSteel Ltd", industry_code=101, description="Steel manufacturing"),
        Industry(name="GreenPlast", industry_code=102, description="Plastic processing"),
        Industry(name="RecyclePro", industry_code=103, description="Recycling services"),
        Industry(name="BioLoop", industry_code=104, description="Organic waste recycling"),
        Industry(name="UniCycle", industry_code=105, description="Circular economy solutions"),
        Industry(name="GlassWorks KE", industry_code=106, description="Glass manufacturing"),
        Industry(name="MetalCore", industry_code=107, description="Metal fabrication"),
        Industry(name="WasteXchange", industry_code=108, description="Waste trading platform"),
        Industry(name="AgriCycle", industry_code=109, description="Agricultural waste reuse"),
        Industry(name="EcoRenew", industry_code=110, description="Renewable material recovery"),
    ]

    db.session.add_all(industries)
    db.session.commit()

    print("Seeding wastes...")

    wastes = [
        Waste(name="Scrap Metal", wasteType="Metal", quantity=500, unit="kg", industry_id=industries[0].id),
        Waste(name="Plastic Pellets", wasteType="Plastic", quantity=300, unit="kg", industry_id=industries[1].id),
        Waste(name="Glass Shards", wasteType="Glass", quantity=200, unit="kg", industry_id=industries[5].id),
        Waste(name="Organic Waste", wasteType="Organic", quantity=1000, unit="kg", industry_id=industries[3].id),
        Waste(name="Aluminium Offcuts", wasteType="Metal", quantity=150, unit="kg", industry_id=industries[6].id),
    ]

    db.session.add_all(wastes)
    db.session.commit()

    print("Seeding waste requests...")

    requests = [
        WasteRequest(
            quantity_requested=100,
            status="pending",
            details="Request for recycling",
            industry_id=industries[2].id,
            waste_id=wastes[0].id,
        ),
        WasteRequest(
            quantity_requested=50,
            status="approved",
            details="Approved exchange",
            industry_id=industries[4].id,
            waste_id=wastes[1].id,
        ),
        WasteRequest(
            quantity_requested=200,
            status="rejected",
            details="Quantity unavailable",
            industry_id=industries[8].id,
            waste_id=wastes[3].id,
        ),
    ]

    db.session.add_all(requests)
    db.session.commit()

    print("Database seeded successfully!")

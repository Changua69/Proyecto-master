from app.database import rooms_collection

def init_rooms():
    
    rooms_collection.delete_many({})  

    rooms = []

    for i in range(1, 9):
        rooms.append({
            "number": i,
            "type": "estandar",
            "price": 100000,
            "status": "disponible"
        })

    for i in range(9, 17):
        rooms.append({
            "number": i,
            "type": "familiar",
            "price": 180000,
            "status": "disponible"
        })

    for i in range(17, 25):
        rooms.append({
            "number": i,
            "type": "suite",
            "price": 300000,
            "status": "disponible"
        })

    rooms_collection.insert_many(rooms)
from faker import Faker
import random
from pymongo import MongoClient

fake = Faker()
client = MongoClient("mongodb://localhost:27017/")
db = client["restaurant"]
db.tables.delete_many({})

for i in range(1, 31):
    table_number = i 
    seats = random.randint(2, 8)

    db.tables.insert_one({
        "_id": str(i),
        "value": "#".join([
            str(i),
            str(table_number),
            str(seats),
        ])
    })

print("Inserted 30 rows into 'tables' collection.")

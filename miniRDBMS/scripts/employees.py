from faker import Faker
import random
from pymongo import MongoClient

fake = Faker()
client = MongoClient("mongodb://localhost:27017/")
db = client["restaurant"]

staff_names = [
    "Alice Carter", "Bob Nguyen", "Charlie Smith", "Diana Lopez", "Ethan Green",
    "Fiona Kim", "George Patel", "Hannah Zhao", "Ivan Rossi", "Julia Cohen",
    "Kevin Müller", "Lily Anders", "Marco Silva", "Nina Horvath", "Oscar Dubois",
    "Paula Svensson", "Quinn Novak", "Rita Kaur", "Samir Abbas", "Tina Yamamoto"
]
roles = ['chef', 'waiter', 'manager', 'host']
db.staff.delete_many({})

for i in range(1, 21):
    name = staff_names[i - 1]
    email = fake.unique.email()
    role = random.choice(roles)
    if role == 'manager':
        salary = round(random.uniform(4000, 6000), 2)
    elif role == 'chef':
        salary = round(random.uniform(3000, 5000), 2)
    elif role == 'waiter':
        salary = round(random.uniform(1800, 3000), 2)
    else:
        salary = round(random.uniform(2000, 3500), 2)
    db.staff.insert_one({
        "_id": str(i),
        "value": "#".join([
            str(i),
            name,
            email,
            role,
            str(salary),
        ])
    })

print("Inserted 20 rows into 'staff' collection.")

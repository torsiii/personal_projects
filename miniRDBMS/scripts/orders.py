from faker import Faker
import random
from pymongo import MongoClient

fake = Faker()
client = MongoClient("mongodb://localhost:27017/")
db = client["restaurant"]

customer_names = [
    "Alice Carter", "Bob Nguyen", "Charlie Smith", "Diana Lopez", "Ethan Green",
    "Fiona Kim", "George Patel", "Hannah Zhao", "Ivan Rossi", "Julia Cohen",
    "Kevin Müller", "Lily Anders", "Marco Silva", "Nina Horvath", "Oscar Dubois",
    "Paula Svensson", "Quinn Novak", "Rita Kaur", "Samir Abbas", "Tina Yamamoto",
    "Umar Jafari", "Valeria Gomez", "Walter Sun", "Ximena Lee", "Yusuf O'Brien",
    "Zara Mendes", "Aaron Koenig", "Bella Tran", "Cecil Yu", "Dana Ahmed",
    "Eli Roth", "Fatima Singh", "Gabe Moreau", "Hiro Tanaka", "Ines Müller",
    "Jakub Novak", "Kaori Arai", "Leo Fischer", "Maya Varga", "Niko Horváth",
    "Ola Nilsen", "Petra Blanka", "Qadir Choi", "Rene Dubois", "Safa Ghali",
    "Tomasz Zielinski", "Ulrik Thomsen", "Vera Barta", "Waleed Kazemi", "Yuki Ito"
]
staff_names = [
    "Alice Carter", "Bob Nguyen", "Charlie Smith", "Diana Lopez", "Ethan Green",
    "Fiona Kim", "George Patel", "Hannah Zhao", "Ivan Rossi", "Julia Cohen",
    "Kevin Müller", "Lily Anders", "Marco Silva", "Nina Horvath", "Oscar Dubois",
    "Paula Svensson", "Quinn Novak", "Rita Kaur", "Samir Abbas", "Tina Yamamoto"
]
db.reservations.delete_many({})

                            
for i in range(1, 31):
    customer_name = random.choice(customer_names)
    employee_name = random.choice(staff_names)           
    total = str(round(random.uniform(15.0, 200.0), 2))

    db.orders.insert_one({
        "_id": str(i),
        "value": "#".join([
            str(i),
            customer_name,
            employee_name,
            total
        ])
    })

print("Inserted 30 rows into 'orders' collection.")

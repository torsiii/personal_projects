from faker import Faker
import random
from pymongo import MongoClient

fake = Faker()
client = MongoClient("mongodb://localhost:27017/")
db = client["restaurant"]

db.tables.delete_many({})

customer_names = [
    # replace this with your actual 50 customer names
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

for i in range(1, 31):
    table_number = str(random.randint(1, 30))
    customer_name = random.choice(customer_names)
    guest_count = str(random.randint(1, 8))

    db.reservations.insert_one({
        "_id": str(i),
        "value": "#".join([
            str(i),              # id
            table_number,        # table_number
            customer_name,       # customer_name
            guest_count          # guest_count
        ])
    })

print("Inserted 30 rows into 'reservations' collection.")

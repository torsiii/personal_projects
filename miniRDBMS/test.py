from pymongo import MongoClient
import random
import string
import sys

def generate_data(db_name, table_name, count):
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    table = db[table_name]
    metadata = db["_metadata"].find_one({"table_name": table_name})

    if not metadata:
        print(f"[ERROR] Metadata for table '{table_name}' not found.")
        return

    columns = list(metadata["columns"].keys())
    types = metadata["columns"]

    print(f"Generating {count} rows in '{db_name}.{table_name}'...")
    for i in range(count):
        key = f"gen{i}"
        values = []

        for col in columns:
            col_type = types[col]
            if col_type == "int":
                values.append(str(random.randint(1, 100)))
            elif col_type == "float":
                values.append(f"{random.uniform(1, 100):.2f}")
            else:
                values.append(''.join(random.choices(string.ascii_lowercase, k=5)))

        value_string = "#".join(values)
        table.insert_one({"_id": key, "value": value_string})

        if i % 5000 == 0 and i > 0:
            print(f"Inserted {i} rows...")

    print(f" Done. Inserted {count} rows into '{table_name}'.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_data.py <database_name> <table_name> <row_count>")
        sys.exit(1)

    db_name = sys.argv[1]
    table_name = sys.argv[2]
    try:
        row_count = int(sys.argv[3])
    except ValueError:
        print("Row count must be an integer.")
        sys.exit(1)

    generate_data(db_name, table_name, row_count)

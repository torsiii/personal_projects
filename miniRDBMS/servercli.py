from termcolor import colored
from pymongo import MongoClient  
import socket
import json
import os
from colorama import init
init()
import sys
from colorama import Fore, Style

mongo_client = MongoClient("mongodb://localhost:27017/")
META_FILE = "db_meta.json"

if not os.path.exists(META_FILE):
    with open(META_FILE, "w") as f:
        json.dump({}, f)


def read_metadata_from_file():
    with open(META_FILE, "r") as f:
        return json.load(f)


def save_metadata_to_file(data):
    with open(META_FILE, "w") as f:
        json.dump(data, f, indent=4)


def handle_create_database(db_name):
    metadata = read_metadata_from_file()
    if db_name in metadata:
        return f"Error: the '{db_name}' database already exists."
    metadata[db_name] = {}
    save_metadata_to_file(metadata)
    import json

    return json.dumps({
        "status": "success",
        "message": "Database created successfully."
    })



def handle_create_table(db_name, table_name, columns, unique_keys, foreign_keys):
    metadata = read_metadata_from_file()
    if db_name not in metadata:
        return f"Error: the '{db_name}' database doesn't exist."

    if table_name in metadata[db_name]:
        return f"Error: the '{table_name}' table already exists in the '{db_name}' database."

    metadata[db_name][table_name] = {
        "columns": columns,
        "unique_indexes": unique_keys,
        "foreign_keys": foreign_keys
    }
    save_metadata_to_file(metadata)

    #mongo db
    db = mongo_client[db_name]
    metadata_coll = db["_metadata"]

    metadata_doc = {
    "table_name": table_name,
    "columns": columns,
    "unique_indexes": unique_keys,
    "foreign_keys": foreign_keys
    }
    metadata_coll.insert_one(metadata_doc)
    #return  f"'{table_name}' table created in the '{db_name}' database."
    return json.dumps({
        "status": "success",
        "message": "Table was created successfully."
    })


def handle_drop_database(db_name):
    metadata = read_metadata_from_file()
    if db_name not in metadata:
        return f"Error: the '{db_name}' database does not exist."

    del metadata[db_name]
    save_metadata_to_file(metadata)
    #return f"'{db_name}' database is dropped." 
    return json.dumps({
        "status": "success",
        "message": "Database is dropped."
    })



def handle_drop_table(db_name, table_name):
    metadata = read_metadata_from_file()
    if db_name not in metadata:
        return f"Error: the '{db_name}' database doesn't exist."

    if table_name not in metadata[db_name]:
        return f"Error: '{table_name}' table doesn't exist in the '{db_name}'  database."

    del metadata[db_name][table_name]
    save_metadata_to_file(metadata)
    db = mongo_client[db_name]
    db["_metadata"].delete_one({"table_name": table_name})

    #return f"'{table_name}' table is dropped from the '{db_name}' database."
    return json.dumps({
        "status": "success",
        "message": "Table is dropped."
    })

  

def handle_insert(db_name, table_name, key, value):
    db = mongo_client[db_name]
    table = db[table_name]
    metadata = db["_metadata"].find_one({"table_name": table_name})

    if not metadata:
        return f"Error: Metadata for table '{table_name}' not found."

    #checking primary key
    if table.find_one({"_id": key}):
        return f"Error: Primary key '{key}' already exists in table '{table_name}'."

    columns = metadata.get("columns", {})
    column_names = list(columns.keys())
    values = value.split("#")
    if len(values) != len(column_names):
        return f"Error: Column count mismatch."

    row_data = dict(zip(column_names, values))

    #validating unique constraints
    for col_name in metadata.get("unique_indexes", []):
        index_coll = db[f"index_{table_name}_{col_name}"]
        if index_coll.find_one({"_id": row_data[col_name]}):
            return f"Error: Duplicate value for UNIQUE column '{col_name}'."

    #validating foreign key constraints
    for fk_col, fk_info in metadata.get("foreign_keys", {}).items():
        ref_table = db[fk_info["ref_table"]]
        ref_col = fk_info["ref_column"]
        ref_metadata = db["_metadata"].find_one({"table_name": fk_info["ref_table"]})

        if ref_col == "_id": 
            exists = ref_table.find_one({"_id": row_data[fk_col]})
        else:
            ref_columns = list(ref_metadata["columns"].keys())
            for ref_row in ref_table.find():
                values = ref_row["value"].split("#")
                ref_data = dict(zip(ref_columns, values))
                if ref_data.get(ref_col) == row_data[fk_col]:
                    exists = True
                    break
            else:
                exists = False

        if not exists:
            return f"Error: Foreign key constraint failed on column '{fk_col}', value '{row_data[fk_col]}' not found in '{fk_info['ref_table']}'."

    table.insert_one({"_id": key, "value": value})

    #index files update
    for col_name in metadata.get("unique_indexes", []):
        db[f"index_{table_name}_{col_name}"].insert_one({"_id": row_data[col_name], "pk": key})

    for col_name in metadata.get("non_unique_indexes", []):
        index_coll = db[f"index_{table_name}_{col_name}"]
        existing = index_coll.find_one({"_id": row_data[col_name]}) 
        if existing:
            index_coll.update_one({"_id": row_data[col_name]}, {"$push": {"pks": key}}) 
        else:
            index_coll.insert_one({"_id": row_data[col_name], "pks": [key]})

    return f"Row with key '{key}' inserted successfully into '{table_name}'." 

def handle_delete(db_name, table_name, key):
    db = mongo_client[db_name]
    table = db[table_name]
    metadata = db["_metadata"].find_one({"table_name": table_name})

    if not metadata:
        return f"Error: Metadata for table '{table_name}' not found."

    parent_row = table.find_one({"_id": key})
    if not parent_row:
        return f"Error: Key '{key}' not found in table '{table_name}'."

    parent_values = parent_row["value"].split("#")
    parent_columns = list(metadata["columns"].keys())
    parent_data = dict(zip(parent_columns, parent_values))

    #implementing cascading delete
    for child_meta in db["_metadata"].find(): 
        for fk_col, fk_info in child_meta.get("foreign_keys", {}).items():
            fk_target_table, fk_target_col = fk_info["ref_table"], fk_info["ref_column"]

            if fk_target_table == table_name:
                child_table_name = child_meta["table_name"]
                child_table = db[child_table_name]

                referencing_rows = []
                for child_row in child_table.find():
                    child_values = child_row["value"].split("#")
                    child_columns = list(child_meta["columns"].keys())
                    child_data = dict(zip(child_columns, child_values))

                    child_fk_value = child_data.get(fk_col, "").strip()

                    if fk_target_col == "_id":
                        parent_target_value = str(key).strip()
                    else:
                        parent_target_value = str(parent_data.get(fk_target_col, "")).strip()

                    if child_fk_value == parent_target_value:
                        referencing_rows.append(child_row["_id"])

                for child_key in referencing_rows:
                    cascade_result = handle_delete(db_name, child_table_name, child_key)
                    print(f"Cascade deleted key '{child_key}' from '{child_table_name}'.")
    
    table.delete_one({"_id": key})


    for col_name in metadata.get("unique_indexes", []):
        db[f"index_{table_name}_{col_name}"].delete_one({"_id": parent_data[col_name]})

    for col_name in metadata.get("non_unique_indexes", []):
        index_coll = db[f"index_{table_name}_{col_name}"]
        index_coll.update_one({"_id": parent_data[col_name]}, {"$pull": {"pks": key}})
        index_coll.delete_one({"_id": parent_data[col_name], "pks": []})

    return f"Row with key '{key}' deleted from '{table_name}'." 

def handle_create_index(db_name, table_name, column_name):
    
    db = mongo_client[db_name]
    metadata_coll = db["_metadata"]
    metadata = metadata_coll.find_one({"table_name": table_name})

    if not metadata:
        return f"Error: Metadata for table '{table_name}' not found."

    if column_name not in metadata.get("columns", {}):
        return f"Error: Column '{column_name}' does not exist in table '{table_name}'."

    index_name = f"index_{table_name}_{column_name}"

    if index_name in db.list_collection_names():
        return f"Error: Index on '{column_name}' already exists."

    #buliding the index collection
    index_coll = db[index_name]
    main_table = db[table_name]

    is_unique = column_name in metadata.get("unique_indexes", [])

    for row in main_table.find():
        pk = row["_id"]
        values = row["value"].split("#")
        columns = list(metadata["columns"].keys())
        row_data = dict(zip(columns, values))
        #value = row_data[column_name]
        # added neccessary type casting when storing index values, so querying works later
        column_types = metadata["columns"]
        expected_type = column_types.get(column_name)

        if expected_type == "int":
            try:
                value = int(row_data[column_name])
            except:
                value = row_data[column_name]
        elif expected_type == "float":
            try:
                value = float(row_data[column_name])
            except:
                value = row_data[column_name]
        else:
            value = row_data[column_name]


        if is_unique:
            index_coll.insert_one({"_id": value, "pk": pk})
        else:
            existing = index_coll.find_one({"_id": value})
            if existing:
                index_coll.update_one({"_id": value}, {"$push": {"pks": pk}})
            else:
                index_coll.insert_one({"_id": value, "pks": [pk]})

    if is_unique:
        if "unique_indexes" not in metadata:
            metadata["unique_indexes"] = []
        if column_name not in metadata["unique_indexes"]:
            metadata["unique_indexes"].append(column_name)
    else:
        if "non_unique_indexes" not in metadata:
            metadata["non_unique_indexes"] = []
        if column_name not in metadata["non_unique_indexes"]:
            metadata["non_unique_indexes"].append(column_name)

    metadata_coll.update_one({"table_name": table_name}, {"$set": metadata})

    return  f"Index on '{column_name}' created successfully for '{table_name}'." 

def handle_list_databases():
    dbs = mongo_client.list_database_names()
    return "Databases:\n" + "\n".join(dbs)

def handle_list_tables(db_name):
    if db_name not in mongo_client.list_database_names():
        return f"Error: the '{db_name}' database does not exist."
    tables = mongo_client[db_name].list_collection_names()
    return  f"Tables in '{db_name}':\n" + "\n".join(tables)

def handle_select(db_name, table_name, columns, conditions):
    
    db = mongo_client[db_name]
    table = db[table_name]
    metadata = db["_metadata"].find_one({"table_name": table_name})

    if not metadata:
        return f"Error: Metadata for table '{table_name}' not found."

    column_names = list(metadata.get("columns", {}).keys())

    indexed_sets = []   # collecting all indexed pk-s that satisfy condition
    remaining_conditions = []   # if the column had no index => brute force approach


    #======= impossible range conditions check ======
    condition_map = {}
    for cond in conditions:
        col = cond["column"]
        op = cond["operator"]
        val = cond["value"]

        if col not in condition_map:
            condition_map[col] = {"gt": None, "lt": None}

        try:
            num_val = float(val)
        except ValueError:
            continue  # skip non-numeric values

        if op in (">", ">="):
            if condition_map[col]["gt"] is None or num_val > condition_map[col]["gt"]:
                condition_map[col]["gt"] = num_val
        elif op in ("<", "<="):
            if condition_map[col]["lt"] is None or num_val < condition_map[col]["lt"]:
                condition_map[col]["lt"] = num_val

    for col, bounds in condition_map.items(): 
        if bounds["gt"] is not None and bounds["lt"] is not None and bounds["gt"] >= bounds["lt"]:
            return f"Invalid range query on column '{col}': no value can satisfy the condition."
    # ============================================

    
    for cond in conditions:
        col = cond["column"]
        op = cond["operator"]
        val = cond["value"]

        #if the col has an index => accessing the relevant index collection
        if col in metadata.get("unique_indexes", []) or col in metadata.get("non_unique_indexes", []):
            index_coll = db.get_collection(f"index_{table_name}_{col}")

            column_type = metadata["columns"].get(col)
            try:
                if column_type == "int":
                    val = int(val)
                elif column_type == "float":
                    val = float(val)
            except:
                pass 

            if op == "=":
                matches = index_coll.find({"_id": val}) 
            elif op in [">", ">=", "<", "<="]:
                mongo_op = {"<": "$lt", "<=": "$lte", ">": "$gt", ">=": "$gte"}[op]
                try:
                    val_converted = float(val)
                except ValueError:
                    val_converted = val  # leave as string if conversion doesnt work

                matches = index_coll.find({"_id": {mongo_op: val_converted}})

            else:
                remaining_conditions.append(cond) # pl. !=
                continue

            # extracting pk-s from index
            pk_set = set()
            for match in matches: 
                if "pk" in match:
                    pk_set.add(match["pk"])
                elif "pks" in match:
                    pks = match["pks"]
                    if isinstance(pks, list):
                        for pk in pks:
                            pk_set.add(pk)
                    else:
                        print(f"type issue for 'pks': {type(pks)} in {match}")
            indexed_sets.append(pk_set)
        else:
            
            remaining_conditions.append(cond)

    if indexed_sets:
        #intersection of matching key sets (AND)
        candidate_keys = set.intersection(*indexed_sets) # * = set.intersection(*[A, B, C]) → set.intersection(A, B, C)
    else:
        #full table scan
        candidate_keys = set(row["_id"] for row in table.find())

        if conditions:
            search_key = conditions[0]["column"]
            if search_key in column_names:
                column_types = metadata["columns"]

                def extract_sort_value(row):
                    value_parts = row["value"].split("#")
                    row_data = dict(zip(column_names, value_parts)) 
                    val = row_data.get(search_key) 
                    
                    try:
                        if column_types[search_key] == "int":
                            return int(val)
                        elif column_types[search_key] == "float":
                            return float(val)
                    except:
                        pass
                    return val or ""

                sorted_rows = sorted(table.find(), key=extract_sort_value)
                candidate_keys = [row["_id"] for row in sorted_rows]
    
    results = []
    rows = table.find({"_id": {"$in": list(candidate_keys)}}) 
    for row in rows:
        key = row["_id"]
        value_parts = row["value"].split("#")
        column_types = metadata["columns"]
        row_data = {}
        for col, val in zip(column_names, value_parts):
            expected_type = column_types[col]
            if expected_type == "int":
                try:
                    row_data[col] = int(val)
                except:
                    row_data[col] = val
            elif expected_type == "float":
                try:
                    row_data[col] = float(val)
                except:
                    row_data[col] = val
            else:
                row_data[col] = val 

        match = True
        for cond in remaining_conditions: 
            col = cond["column"]
            op = cond["operator"]
            val = cond["value"]

            cell = row_data.get(col)
            if cell is None:
                match = False
                break

            
            try:
                cell_val = float(cell)
                cond_val = float(val)
            except:
                cell_val = cell
                cond_val = val

            if op == "=" and not (cell_val == cond_val):
                match = False
            elif op == ">" and not (cell_val > cond_val):
                match = False
            elif op == ">=" and not (cell_val >= cond_val):
                match = False
            elif op == "<" and not (cell_val < cond_val):
                match = False
            elif op == "<=" and not (cell_val <= cond_val):
                match = False

        if match:
            results.append((key, row_data))

    # creating query result
    output = []
    duplicates = set()
    for key, row_data in results:
        if columns == ["*"]:
            projected = {"_id": key}
            projected.update(row_data)
        else:
            projected = {"_id": key}
            for col in columns:
                projected[col] = row_data.get(col, "NULL")

        row_tuple = tuple(projected.items())
        if row_tuple not in duplicates:
            duplicates.add(row_tuple)
            output.append(projected)
 

    return json.dumps(output, indent=2)

def handle_join_select(db_name, tables, join_conditions, columns, conditions_per_table):
    db = mongo_client[db_name]

    partial_results = {}
    for table in tables:
        conds = conditions_per_table.get(table, [])
        result = json.loads(handle_select(db_name, table, ["*"], conds))
        partial_results[table] = []
        for row in result:
            row_id = row.pop("_id", None)
            partial_results[table].append({"_id": row_id, **row})

    # JOIN conditions: {(left_table, right_table): (left_col, right_col)}
    join_map = {}
    for cond in join_conditions:
        key = (cond["left_table"], cond["right_table"])
        join_map[key] = (cond["left_column"], cond["right_column"])

    def get_join_condition(left_table, right_table): # t2.col = t1.col-re also works
        if (left_table, right_table) in join_map:
            return join_map[(left_table, right_table)]
        elif (right_table, left_table) in join_map:
            col_r, col_l = join_map[(right_table, left_table)]
            return col_l, col_r
        else:
            return None, None

    result_rows = []
    for row in partial_results[tables[0]]:
        #result_rows.append({f"{tables[0]}.{k}": v for k, v in row.items() if k != "_id"})
        result = {}
        for k, v in row.items():
            if k == "_id":
                result[f"{tables[0]}._id"] = v 
            else:
                result[f"{tables[0]}.{k}"] = v
        result_rows.append(result)

    for i in range(1, len(tables)):
        left_table = tables[i - 1]
        right_table = tables[i]

        left_col, right_col = get_join_condition(left_table, right_table)
        if not left_col or not right_col:
            return f"Error: Missing join condition between {left_table} and {right_table}"

        meta = db["_metadata"].find_one({"table_name": right_table})
        if not meta or right_col not in meta["columns"]:
            return f"Error: Column '{right_col}' not found in table '{right_table}'"

        right_type = meta["columns"][right_col] 
        cast_func = int if right_type == "int" else float if right_type == "float" else str

        index_name = f"index_{right_table}_{right_col}"
        if index_name not in db.list_collection_names():
            return f"Error: Join requires an index on {right_table}.{right_col}"

        index_coll = db[index_name]
        right_rows_coll = db["temp_" + right_table]
        right_rows_coll.drop()
        for row in partial_results[right_table]:
            right_rows_coll.insert_one(row)

        # JOIN
        new_result = []
        for row in result_rows: 
            left_val = row.get(f"{left_table}.{left_col}")
            try:
                join_val = cast_func(left_val)
            except:
                continue

            # Index lookup
            match_keys = []
            for doc in index_coll.find({"_id": join_val}):
                if "pk" in doc:
                    match_keys.append(doc["pk"])
                elif "pks" in doc:
                    match_keys.extend(doc["pks"])

            if not match_keys:
                continue

            right_matches = right_rows_coll.find({"_id": {"$in": match_keys}})
            for rrow in right_matches: 
                joined = dict(row)
                joined.update({f"{right_table}.{k}": v for k, v in rrow.items() if k != "_id"})
                new_result.append(joined)

        result_rows = new_result

    if columns == ["*"]:
        final = result_rows
    else:
        final = [{col: row.get(col, "NULL") for col in columns} for row in result_rows]

    return json.dumps(final[:1000], indent=2, default=str)


def apply_group_by_to_result(rows, group_by, having=None, order_by=None):
    group_column = group_by.get("group_column", "").strip()
    aggregates = group_by.get("aggregates", [])  # list of {agg_column, operation}
    grouped = {}

    def safe_lookup(row, key): 
        for k, v in row.items():
            if k.strip().lower() == key.strip().lower():
                return v
        return None

    for row in rows:
        gval = safe_lookup(row, group_column)
        if gval is None:
            continue
        if gval not in grouped:
            grouped[gval] = {}

        for agg in aggregates:
            col = agg.get("agg_column", "").strip()
            op = agg.get("operation", "COUNT").strip().upper()

            aval = safe_lookup(row, col)
            try:
                aval = float(aval)
            except:
                if op != "COUNT": 
                    continue

            key = f"{op}_{col}"
            if key not in grouped[gval]:
                if op == "MIN":
                    grouped[gval][key] = aval
                elif op == "MAX":
                    grouped[gval][key] = aval
                elif op == "SUM":
                    grouped[gval][key] = aval
                elif op == "AVG":
                    grouped[gval][key] = {"sum": aval, "count": 1}
                elif op == "COUNT":
                    grouped[gval][key] = 1
            else:
                if op == "MIN":
                    grouped[gval][key] = min(grouped[gval][key], aval)
                elif op == "MAX":
                    grouped[gval][key] = max(grouped[gval][key], aval)
                elif op == "SUM":
                    grouped[gval][key] += aval
                elif op == "AVG":
                    grouped[gval][key]["sum"] += aval
                    grouped[gval][key]["count"] += 1
                elif op == "COUNT":
                    grouped[gval][key] += 1

    output = []
    for gval, stats in grouped.items():
        row = {"group": gval}
        for agg in aggregates:
            col = agg.get("agg_column", "").strip()
            op = agg.get("operation", "COUNT").strip().upper()
            key = f"{op}_{col}"
            if op == "AVG":
                avg_data = stats.get(key, {"sum": 0, "count": 0})
                row[f"{op}_{col}"] = avg_data["sum"] / avg_data["count"] if avg_data["count"] > 0 else None
            else:
                row[f"{op}_{col}"] = stats.get(key)

        if having:
            h_col = having.get("column", "").strip()
            h_op = having.get("operator", "")
            try:
                h_val = float(having.get("value", 0))
                current_val = float(row.get(h_col))
                if h_op == ">" and not (current_val > h_val): continue
                if h_op == ">=" and not (current_val >= h_val): continue
                if h_op == "<" and not (current_val < h_val): continue
                if h_op == "<=" and not (current_val <= h_val): continue
                if h_op == "=" and not (current_val == h_val): continue
            except:
                continue
        if order_by:
            output = apply_order_by(output, order_by)


        output.append(row)

    return json.dumps(output, indent=2, default=str)


def process_command(command):
    try:
        data = json.loads(command)
        action = data.get("action")


        if action == "CREATE_DATABASE":
            return handle_create_database(data["db_name"])
        elif action == "CREATE_TABLE":
            return handle_create_table(data["db_name"], data["table_name"], data["columns"],data.get("unique_keys", []), data.get("foreign_keys", {}))
        elif action == "DROP_DATABASE":
            return handle_drop_database(data["db_name"])
        elif action == "DROP_TABLE":
            return handle_drop_table(data["db_name"], data["table_name"])
        elif action == "INSERT":
            return handle_insert(data["db_name"], data["table_name"], data["key"], data["value"])
        elif action == "DELETE":
            return handle_delete(data["db_name"], data["table_name"], data["key"])
        elif action == "CREATE_INDEX":
            return handle_create_index(data["db_name"], data["table_name"], data["column_name"])
        elif action == "LIST_DATABASES":
            return handle_list_databases()
        elif action == "LIST_TABLES":
            return handle_list_tables(data["db_name"])
        elif action == "SELECT":
            db_name = data["db_name"]
            table = data["table_name"]
            columns = data.get("columns", ["*"])

            if "group_by" in data:
                group_col = data["group_by"].get("group_column")
                if group_col and group_col not in columns and columns != ["*"]:
                    columns.append(group_col)

                for agg in data["group_by"].get("aggregates", []):
                    agg_col = agg.get("agg_column")
                    if agg_col and agg_col not in columns and columns != ["*"]:
                        columns.append(agg_col)

            conditions = data.get("conditions", [])
            raw_result = json.loads(handle_select(db_name, table, columns, conditions))

            if "group_by" in data:
                return apply_group_by_to_result(raw_result, data["group_by"], data.get("having"))
            else:
                if "order_by" in data:
                    raw_result = apply_order_by(raw_result, data["order_by"])

                return json.dumps(raw_result, indent=2)


        elif action == "JOIN_SELECT":
            db_name = data["db_name"]
            tables = data["tables"]
            join_conditions = data.get("join_conditions", [])
            columns = data.get("columns", ["*"])
            conditions_per_table = data.get("conditions", {})
            
            for table_conds in conditions_per_table.values():
                for cond in table_conds:
                    cond_col = cond.get("column")
                    if cond_col and cond_col not in columns and columns != ["*"]:
                        columns.append(cond_col)

            if "group_by" in data:
                group_col = data["group_by"].get("group_column")
                if group_col and group_col not in columns and columns != ["*"]:
                    columns.append(group_col)

                for agg in data["group_by"].get("aggregates", []):
                    agg_col = agg.get("agg_column")
                    if agg_col and agg_col not in columns and columns != ["*"]:
                        columns.append(agg_col)

            raw_result = json.loads(handle_join_select(db_name, tables, join_conditions, columns, conditions_per_table))

            if "group_by" in data:
                return apply_group_by_to_result(
                    raw_result,
                    data["group_by"],
                    data.get("having"),
                    data.get("order_by")  
                )

            return json.dumps(raw_result, indent=2)

        else:
            return "Error: Unknown action."
    except Exception as e:
        return f"Error processing the command: {str(e)}"


def apply_order_by(rows, order_by):
    column = order_by["column"]
    desc = order_by.get("desc", False)

    try:
        return sorted(rows, key=lambda r: r.get(column), reverse=desc)
    except Exception:
        return rows

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)
    print("\U0001F525 \033[32mServer is running\033[32m \U0001F525")

    while True:
        client_socket, _ = server_socket.accept()
        command = client_socket.recv(1024).decode()

        if not command:
            continue
        response = process_command(command)
        client_socket.sendall(response.encode())
        client_socket.close()


if __name__ == "__main__":
    start_server()
from sortedcontainers import SortedDict

# Indexing for columns
class indexColumns:
    def __init__(self):
        self.container = SortedDict()

    def insert(self, value, pointer):
        # Return key value if it is available in the dictionary
        self.container.setdefault(value, set()).add(pointer)

# Database 
class db:
    def __init__(self, table_name, columns):
        self.name = table_name
        self.table = {}
        self.columns = {}
        self.row_id = 0
        self.index = {}

        # Indexing
        for i, (column_name, index_flag) in enumerate(columns):
            self.columns[column_name] = i
            if index_flag == True:
                self.index[i] = indexColumns()

    # Insert rows to database table
    def insert(self, table_name, values):
        rows_insert = []
        if len(values) != len(self.columns):
            print(f"Invalid amount of values to insert into {table_name}!")
        else:
            print(f"len val {len(values)}   len cols {len(self.columns)}")
            row = self.row_id
            print(f"row  {row}")
            for column_name in self.index:
                print(f"cols   {column_name}")
                row_i = self.columns[column_name]
                self.index[column_name].insert(values[row_i], row)
            self.table[row] = values
            self.row_id += 1
            rows_insert.append(values)
        return rows_insert

# Storager
class storager:
    def __init__(self):
        self.table = {}

    # Create Database
    def create_db(self, table_name, columns):
        if columns:
            self.table[table_name] = db(table_name, columns)
            print(f"Table {table_name} has been successfully created!")
        else:
            print(f"Table {table_name} columns are empty!")

    # Insert data to storage
    def insert_db(self, table_name, values):
        if table_name not in self.table:
            print(f"Table {table_name} does not exist!")
        else:
            if len(values) != len(self.table[table_name].columns):
                print(f"Invalid amount of values to insert into {table_name}!")
            else:
                rows_insert = self.table[table_name].insert(table_name, values)
                print(f"{len(rows_insert)} row(s) has been inserted into {table_name}!")

if __name__ == "__main__":
    storage = storager()
    index = indexColumns()

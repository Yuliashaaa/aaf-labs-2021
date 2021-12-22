from sortedcontainers import SortedDict

# Indexing for columns
class indexColumns:
    def __init__(self):
        self.container = SortedDict()

# Database 
class db:
    def __init__(self, table_name, columns):
        self.name = table_name
        self.table = {}
        self.row_id = 0
        self.columns = {}
        self.index = {}

        for i, (column_name, index_flag) in enumerate(columns):
            self.columns[column_name] = i
            if index_flag == True:
                self.index[i] = indexColumns()

    def insert(self, values):
        rows_insert = []
        if len(values) == len(self.columns):
            

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

    # Insert data to database
    def insert_db(self, table_name, values):
        if table_name not in self.table:
            print(f"Table {table_name} does not exist!")
        else:
            if len(values) != len(self.table[table_name].columns):
                print(f"Invalid amount of values to insert into {table_name}!")
            else:
                rows_insert = self.table[table_name].insert(values)
                print(f"{len(rows_insert)} row(s) has been inserted into {table_name}!")

if __name__ == "__main__":
    storage = storager()

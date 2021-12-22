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

# Storager
class storager:
    def __init__(self):
        self.table = {}

    def create_db(self, table_name, columns):
        if columns:
            self.table[table_name] = db(table_name, columns)
            print(f"Table {table_name} has been successfully created!")
        else:
            print(f"Table {table_name} columns are empty!")

if __name__ == "__main__":
    storage = storager()

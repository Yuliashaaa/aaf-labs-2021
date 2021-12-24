from sortedcontainers import SortedDict
from terminaltables import GithubFlavoredMarkdownTable

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
            row = self.row_id
            #print(f"self.columns  {self.columns}")
            for indexed_columns in self.index:
                #print(f"index[indexed-col]   {self.index[indexed_columns]}")
                row_i = list(self.columns.keys())[list(self.columns.values()).index(indexed_columns)]
                col_i = int(self.columns[row_i])
                #print(f"row_i   {row_i}")
                #print(f"col_i   {col_i}")
                #print(f"index[row_i]   {self.index[col_i]}")
                self.index[col_i].insert(values[col_i], row)
            self.table[row] = values
            self.row_id += 1
            rows_insert.append(values)
            print(f"self.table[row]   {self.table[row]}")
        return rows_insert

    # Select from database table
    def select(self, columns, condition, order):
        # Basic selection
        table_data = []
        if not condition and not order:
            if columns == list('*'):
                table_data.append(self.columns)
                for i in range (0, self.row_id):
                    table_data.append(self.table[i])
        table = GithubFlavoredMarkdownTable(table_data)
        print(table.table)

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
                # Deleting excessive symbols in names
                for indx, word in enumerate(values):
                    exch = word
                    first = exch[0]
                    last = exch[-1]
                    print(exch)
                    print(first, last)
                    if first in ['"', '”', '“']:
                        exch = exch[1:]
                        last = exch[-1]
                    if last in ['"', '”', '“']:
                        exch = exch[:-1]
                    values[indx] = exch
                    print(exch)
                    print(values[indx])
                rows_insert = self.table[table_name].insert(table_name, values)
                print(f"{len(rows_insert)} row(s) has been inserted into {table_name}!")

    def select_db(self, table_name, columns, condition, order):
        #print(f"Select {columns} from {table_name}!")
        # Check table existance in database
        if table_name not in self.table:
            print(f"Table {table_name} does not exist!")
        else:
            table_select = self.table[table_name].select(columns, condition, order)
            return table_select

    def delete_db(self, table_name, condition):
        if not condition:
            rows_delete = self.table[table_name].delete()
            print(f"{len(rows_delete)} row(s) has been deleted from {table_name}!")

if __name__ == "__main__":
    storage = storager()
    index = indexColumns()

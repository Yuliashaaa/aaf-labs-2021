def create(table_name, columns):
    DB = database(table_name, columns)
    print ('Table', table_name, 'has been created with columns ', columns)
    return DB

class database:
    def __init__(self, table_name, columns) -> None:
        self.table_name = table_name
        self.tables = columns

    def select(self, table_name):
        print ('SELECTED', table_name)
    
    def insert(self, table_name, values):
        print ('Inserted row with ', values, ' in ', table_name)

    def delete(self, table_name):
        print ('Deleted ', table_name)

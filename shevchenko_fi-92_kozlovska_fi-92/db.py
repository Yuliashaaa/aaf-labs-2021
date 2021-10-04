class DB:
    def __init__(self) -> None:
        self.tables = {}

    def create(self, table_name, columns):
        print ('Table', table_name, 'has been created')

    def select(self, table_name):
        print ('SELECTED', table_name)
    
    def insert(self, table_name, values):
        print ('Inserted row with ', values, ' in ', table_name)

    def delete(self, table_name):
        print ('Deleted ', table_name)

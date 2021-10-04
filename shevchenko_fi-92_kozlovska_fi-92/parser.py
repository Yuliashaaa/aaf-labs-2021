import db, re # Import db.py and Regular Expressions

class Parser:
    def __init__(self):                         # App init
        while True:
            query = input('--> ')
            for command in query.split(';'):    # Split commands with ';' : CREATE ...; SELECT ... 
                if command:                     
                    print (self.action(command))
        
    def action(self, query:str) -> str:         # TODO: optimization
        query = self.parse_command(query)       # Split input command to the list of commands
        command = query[0]

        if command == 'CREATE':
            _, table_name, columns = query
            action_call = db.create(table_name, columns)
        elif command == 'SELECT':
            _, table_name, columns = query
            action_call = db.select(table_name, columns)
        elif command == 'INSERT':
            _, table_name, values = query
            action_call = db.insert(table_name, values)
        elif command == 'DELETE':
            _, table_name = query
            action_call = db.delete(table_name)
        else:
            action_call = self.error()

        return action_call

    def error(self):
        return 'ERROR, COMMAND NOT FOUND'

    def parse_command(self, query) -> list:     # Split input for list of [command, arg1, arg2, arg3]
        str = re.findall(r'\S+', query)
        word = str[0]
        try:
            if str.index(word)+1 >= len(str): raise Exception('too short')
            if word.upper() == 'CREATE':
                columns = {}
                table_name = str[str.index(word)+1] # If str[0] == CREATE => str[1] = table_name
                m = query.split('(', 1)[1].split(')')[0].replace(',', '').split()   # Parse arguments
                for column in m:
                    if column == 'INDEXED':
                        pass
                    elif column == m[-1] or m[m.index(column)+1] != 'INDEXED':   
                        columns[column] = False
                    elif m[m.index(column)+1] == 'INDEXED':
                        columns[column] = True
                        
                return ['CREATE', table_name, columns]
            elif word.upper() == 'SELECT':
                selected = str[1]
                table_name = str[str.index('FROM')+1]       
                
                return ['SELECT', table_name, selected]

            elif word.upper() == 'INSERT':
                table_name = str[1]
                values = query.split('(', 1)[1].split(')')[0].replace(',', '').split()
                return ['INSERT',table_name, values]
            elif word.upper() == 'DELETE':
                table_name = str[str.index('FROM')+1]
                return ['DELETE', table_name]

        except:
            print('The list is too short')
            return [0]

if __name__ == '__main__':
    client = Parser()

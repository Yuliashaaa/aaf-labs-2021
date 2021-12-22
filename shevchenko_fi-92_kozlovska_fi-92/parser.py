# Importing libraries
import re
import storage as db
import sys

storage = db.storager()

# Parser process:
# Parsing words -- DONE!
# Exit function -- DONE!
# Create function -- DONE!
# Insert function -- create insert function in db class and indexColumns class
# Select function
# Delete finction

# Function to parse words into commands and find command type if it is possible
def parse(self, words):
    command = re.findall(r'\S+', words)
    print(command)
    command_type = command[0]
    command_type = command_type.upper()
    symbols = ['(', ')', ',', '.', ';']

    # Find command type and arguments or print command error
    if command_type not in Parser.COMMANDS:
        print(f"Command '{command_type}' not found!")
    elif command_type == 'EXIT':    
        print('Stopping program...')
        Parser.exit_command = True
        sys.exit()  
    elif command_type == 'CREATE':
        table_name = command[1]
        if re.match(Parser.NAMES, table_name) and table_name.upper() not in Parser.COMMANDS and table_name.upper() not in Parser.SPECIAL_WORDS:
            columns = []
            i = 2

            # Deleting excessive symbols
            for indx, word in enumerate(command):
                exch = word
                first = exch[0]
                last = exch[-1]
                #print(exch)
                #print(first, last)
                if first in symbols:
                    exch = exch[1:]
                    last = exch[-1]
                if last in symbols:
                    exch = exch[:-1]
                command[indx] = exch
                #print(exch)
                #print(command[indx])

            # Searching indexing columns and mark them to indexed_flag = True
            while i < len(command):
                if i + 1 < len(command):
                    indexed_word = command[i + 1]
                    if indexed_word.upper() == 'INDEXED':
                        indexed_flag = True
                    else:
                        indexed_flag = False
                    columns.append([command[i], indexed_flag])
                    i += int(indexed_flag)
                else:
                    indexed_flag = False
                    columns.append([command[i], indexed_flag])
                i += 1
            print(columns)
            command_exec = storage.create_db(table_name, columns)
        else:
            print('Invalid table name!')
    elif command_type == 'INSERT':
        values = []
        i = 2
        if command[1].upper() not in Parser.COMMANDS and command[1].upper() not in Parser.SPECIAL_WORDS:
            table_name = command[1]
        elif command[2].upper() not in Parser.COMMANDS and command[2].upper() not in Parser.SPECIAL_WORDS:
            table_name = command[2]
            i += 1

        # Deleting excessive symbols
        for indx, word in enumerate(command):
            exch = word
            first = exch[0]
            last = exch[-1]
            #print(exch)
            #print(first, last)
            if first in symbols:
                exch = exch[1:]
                last = exch[-1]
            if last in symbols:
                exch = exch[:-1]
            command[indx] = exch
            #print(exch)
            #print(command[indx])

        while i < len(command):
            values.append(command[i])
            i += 1
        print(values)
        command_exec = storage.insert_db(table_name, values)
    elif command_type == 'SELECT':
        # select(command)
        print('SELECT command')
    elif command_type == 'DELETE':
        # delete(command)
        print('DELETE command')
    return command_exec


# Parser class
class Parser:
    NAMES = r"[a-zA-Z][a-zA-Z0-9_]*"
    COMMANDS = {'CREATE', 'INSERT', 'SELECT', 'DELETE', 'EXIT'}
    SPECIAL_WORDS = {'INDEXED', 'INTO', 'FROM', 'WHERE', 'ORDER_BY'}

    def __init__(self):
        input_command = ''
        input_accept = True
        exit_command = False
        print('Use "EXIT" command to stop this program')

        while not exit_command:
            while input_accept:
                input_command += ' ' + input('>>').strip()
                if ';' in input_command:
                    for words in input_command.split(';'):
                        if words:
                            #print(words)
                            parse(self, words)
                            input_accept = False
            input_accept = True

        #command = re.findall(r'\S+', words)
        #print(command)

if __name__ == '__main__':
    parser = Parser()

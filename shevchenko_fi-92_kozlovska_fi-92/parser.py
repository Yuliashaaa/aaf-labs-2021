# Importing libraries
import re
import storage as db
import sys

storage = db.storager()

# Parser process:
# Parsing words -- DONE!
# Exit function -- DONE!
# Create function -- DONE!
# Insert function
# Select function
# Delete finction

# Function to parse words into commands and find command type if it is possible
def parse(self, words):
    command = re.findall(r'\S+', words)
    print(command)
    command_type = command[0]
    command_type = command_type.upper()

    # Find command type and arguments or print command error
    if command_type not in Parser.COMMANDS:
        print(f"Command '{command_type}' not found!")
    elif command_type == 'EXIT':    
        print('Stopping program...')
        Parser.exit_command = True
        sys.exit()  
    elif command_type == 'CREATE':
        table_name = command[1]
        if re.match(Parser.NAMES, table_name) and table_name not in Parser.COMMANDS and table_name not in Parser.SPECIAL_WORDS:
            columns = []
            symbols = ['(', ')', ',', '.', ';']
            i = 2

            # Deleting excessive symbols
            for indx, word in enumerate(command):
                first = word[0]
                last = word[-1]
                #print(word)
                #print(first, last)
                if first in symbols:
                    word_ch = word[1:]
                    command[indx] = word_ch
                    #print(word_ch)
                if last in symbols:
                    word_ch = word[:-1]
                    command[indx] = word_ch
                    #print(word_ch)

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
        # insert(command)
        print('INSERT command')
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

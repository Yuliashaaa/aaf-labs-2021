# Parser and Command Line Interface
import re
from db import db

class Parser:
    NAMES = r"[a-zA-Z][a-zA-Z0-9_]*"
    COMMANDS = {"CREATE", "INSERT", "SELECT", "DELETE"}
    SPECIAL_WORDS = {"INDEXED", "INTO", "FROM", "WHERE", "ORDER_BY"}
    OPERATORS = {"=", "!=", ">", "<", ">=", "<="}
    OPERATORS_LIST = list(OPERATORS)

    class StopTheLoop(Exception):
        pass

    def __init__(self): # Initialization of the application
        self.db = db()
        print("Starting the Client! Use 'EXIT;' command to stop the programm.")
        input_query = ""
        while True:
            input_query += " " + input("-->").strip()
            if ";" in input_query:
                for command in input_query.split(";"): # Split commands with ';' : CREATE ...; SELECT ...
                    if command:
                        command = command.strip()
                        if command.upper() == "EXIT": # Exit command to stop the program
                            raise Parser.StopTheLoop
                        try:
                            response = self.action(command) # Try to parse and complete the commands
                        except IndexError:
                            response = "ERROR: invalid command! Try again."
                        except Exception as e:
                            response = "ERROR: {}".format(str(e))
                        print(response)
                        input_query = ""

    def action(self, command: str) -> str: # Choose type of command and make an action with it
        tokens = Parser.parse_command(command)
        command_type = tokens[0]

        if command_type == "CREATE":
            _, table_name, columns = tokens
            response = self.db.create(table_name, columns)
        elif command_type == "INSERT":
            _, table_name, values = tokens
            response = self.db.insert(table_name, values)
        elif command_type == "SELECT":
            _, table_name, columns, condition, group_columns = tokens
            response = self.db.select(table_name, columns, condition, group_columns)
        elif command_type == "DELETE":
            _, table_name, condition = tokens
            response = self.db.delete(table_name, condition)
        else:
            response = "command not found!"

        return response

    def parse_command(command: str) -> list: # Parse the command to the list of tokens
        query = command.split()
        query = list(filter(lambda x: x != "", sum([elements.split(",") for elements in query], [])))

        for i, elements in enumerate(query):
            if elements not in Parser.OPERATORS_LIST:
                check = [operator in elements for operator in Parser.OPERATORS_LIST]
                if any(check):
                    operator = Parser.OPERATORS_LIST[check.index(True)]
                    insert_element = elements.split(operator)
                    insert_element.insert(1, operator)
                    query = query[:i] + insert_element + query[i + 1]
                    break

        tokens = []
        i = 0

        while i < len(query) and query[i].upper() not in Parser.COMMANDS: 
            i += 1
        if i >= len(query):
            raise Exception("command not found!")

        command_type = query[i].upper()
        tokens.append(command_type)
        i += 1

        if command_type == "CREATE": # Parsing CREATE command
            if re.match(Parser.NAMES, query[i]) and not query[i].upper() in Parser.SPECIAL_WORDS:
                tokens.append(query[i])
                i += 1
            else:
                raise Exception("invalid table name!")

            columns = []

            while i < len(query):
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                if re.match(Parser.NAMES, query[i]):
                    if query[i].upper() in Parser.SPECIAL_WORDS:
                        raise Exception("special word before column name!")
                    if (i + 1) < len(query):
                        next_element = query[i + 1]
                        for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                            if symbols in next_element:
                                next_element = next_element.replace(symbols, "")
                        isIndexed = next_element.upper() == "INDEXED"
                    else:
                        isIndexed = False
                    columns.append([query[i], isIndexed])
                    i += isIndexed
                i += 1
            
            tokens.append(columns)

        elif command_type == "INSERT": # Parsing INSERT command
            if i < len(query) and query[i].upper() in Parser.SPECIAL_WORDS:
                i += 1
            if i < len(query) and re.match(Parser.NAMES, query[i]) and not query[i].upper() in Parser.SPECIAL_WORDS:
                tokens.append(query[i])
                i += 1
            else:
                raise Exception("invalid table name!")
            
            values = []

            while i < len(query):
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                values.append(str(query[i]))
                i += 1

            tokens.append(values)

        elif command_type == "SELECT": # Parsig SELECT command
            columns = []

            while i < len(query) and query[i].upper() != "FROM":
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                if query[i] == "*":
                    columns = []
                    i += 1
                elif re.match(Parser.NAMES, query[i]) and query[i].upper() not in Parser.SPECIAL_WORDS:
                    columns.append(query[i])
                    i += 1
                else:
                    raise Exception("invalid column name!")
            
            if i < len(query) and query[i].upper() == "FROM":
                i += 1
            if i < len(query) and re.match(Parser.NAMES, query[i]) and not query[i].upper() in Parser.SPECIAL_WORDS:
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                
                tokens.append(query[i])
                tokens.append(columns)
                i += 1  
            else:
                raise Exception("invalid table name!")
            
            condition = []

            if i < len(query) and query[i].upper() == "WHERE":
                i += 1
                while i < len(query) and len(condition < 3):
                    for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                        if symbols in query[i]:
                            query[i] = query[i].replace(symbols, "")
                    condition.append(str(query[i]))
                    i += 1
            tokens.append(condition)

            group_columns = []

            if i < len(query) and query[i].upper() == "ORDER_BY":
                i += 1
                while i < len(query):
                    for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                        if symbols in query[i]:
                            query[i] = query[i].replace(symbols, "")
                    if re.match(Parser.NAMES, query[i]) and not query[i].upper in Parser.SPECIAL_WORDS:
                        group_columns.append(query[i])
                        i += 1
                    else:
                        raise Exception("invalid group column name!")
            tokens.append(group_columns)

        elif command_type == "DELETE": # Parsing DELETE command
            if i < len(query) and query[i].upper() in Parser.SPECIAL_WORDS:
                i += 1
            if i < len(query) and re.match(Parser.NAMES, query[i]) and not query[i].upper() in Parser.SPECIAL_WORDS:
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                tokens.append(query[i])
                i += 1
            else:
                raise Exception("invalid table name")
            if i < len(query) and query[i].upper() in Parser.SPECIAL_WORDS:
                i += 1

            condition = []

            while i < len(query):
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                condition.append(str(query[i]))
                if query[i].upper() in Parser.SPECIAL_WORDS:
                    raise Exception("invalid column name in WHERE!")
                condition.append(query[i])
                i += 1
            tokens.append(condition)

        return tokens

if __name__ == "__main__":
    client = Parser()

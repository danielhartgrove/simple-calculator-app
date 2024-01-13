import tkinter as tk

memory = "0" #single integer width memory

def isDigit(string):
    try:
        int(string)
        return True
    except:
        return False


def tokenise(string):  # turn a string into a list of tokens
    string.strip(" ")
    chars = list(string)
    tokens = []
    current_number = ''
    tokenised_string = ''

    # group all digits together
    for char in chars:
        if isDigit(char):
            current_number += char
        else:
            if current_number:
                tokens.append(current_number)
                current_number = ''
            tokens.append(char)

    if current_number:
        tokens.append(current_number)

    return tokens

def findindex(char, list):
    for i in range(len(list)):
        if list[i] == char:
            return i
    return -1

def create_ast(tokens): # turn a list of tokens into an abstract syntax tree
    ast = []
    
    if ("-" in tokens):                                     #s
        index = findindex("-", tokens)
        ast.append(["-", create_ast(tokens[0 : index]), create_ast(tokens[index + 1: len(tokens)])])
    elif ("+" in tokens):                                   #a
        index = findindex("+", tokens)
        ast.append(["+", create_ast(tokens[0 : index]), create_ast(tokens[index + 1: len(tokens)])])
    elif ("*" in tokens):                                   #m
        index = findindex("*", tokens)
        ast.append(["*", create_ast(tokens[0 : index]), create_ast(tokens[index + 1: len(tokens)])])
    elif ("/" in tokens):                                   #d
        index = findindex("/", tokens)
        ast.append(["/", create_ast(tokens[0 : index]), create_ast(tokens[index + 1: len(tokens)])])
    elif ("^" in tokens):                                   #i
        index = findindex("^", tokens)
        ast.append(["^", create_ast(tokens[0 : index]), create_ast(tokens[index + 1: len(tokens)])])
    elif (len(tokens) == 1):
        ast.append(tokens[0])
    return ast[0]

def evaluate(string):   # evaluat
    tokens = tokenise(string)
    ast = create_ast(tokens)
    evaluated_ast = evaluate_ast(ast)
    return evaluated_ast

def evaluate_ast(ast):
    if (ast[0] == "+"):
        return evaluate_ast(ast[1]) + evaluate_ast(ast[2])
    elif (ast[0] == "-"):
        return evaluate_ast(ast[1]) - evaluate_ast(ast[2])
    elif (ast[0] == "*"):
        return evaluate_ast(ast[1]) * evaluate_ast(ast[2])
    elif (ast[0] == "/"):
        return evaluate_ast(ast[1]) / evaluate_ast(ast[2])
    elif (ast[0] == "^"):
        return evaluate_ast(ast[1]) ** evaluate_ast(ast[2])
    else:
        return int(ast)


def submit(entry_window):
    string_to_evaluate = entry_window.get()
    output = evaluate(string_to_evaluate)
    entry_window.delete(0, tk.END)
    entry_window.insert(0, output)


def add_to_entry(entry_window, text):
    if entry_window.get() != "Invalid input":
        entry_window.insert(tk.END, text)
    else:
        entry_window.delete(0, tk.END)
        entry_window.insert(tk.END, text)
    

def create_button(window, text, entry_window):
    return tk.Button(window, text=text, command=lambda:
    add_to_entry(entry_window, text))

def remember(entry_window):
    global memory
    memory = entry_window.get()

def recall(entry_window):
    global memory
    entry_window.insert(tk.END, memory)

def main():
    memory = 0
    window = tk.Tk()
    entry_window = tk.Entry(window)
    # Configure the grid
    window.resizable(False, False)

    window.grid_rowconfigure(0, minsize=50)
    window.grid_columnconfigure(0, minsize=50)
    window.grid_columnconfigure(1, minsize=50)
    window.grid_columnconfigure(2, minsize=50)
    
    entry_window.grid(row=0, column=0, columnspan=3, sticky="nsew")

    # Create buttons using a loop
    button_texts = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "(", "0", ")", "+", "-", "^", "*", "/"]
    equals_Button = tk.Button(window, text="=", command=lambda: submit(entry_window))
    memory_Button = tk.Button(window, text="M+", command=lambda: remember(entry_window))
    recall_Button = tk.Button(window, text="MR", command=lambda: recall(entry_window))
    clear_Button = tk.Button(window, text="CLR", command=lambda: entry_window.delete(0, tk.END))
    buttons = [create_button(window, text, entry_window) for text in button_texts]

    # Pack the buttons
    countx = 0
    county = 1
    for button in buttons:
        button.grid(row = county, column = countx, columnspan = 1, sticky = "nsew")
        countx+=1
        if countx == 3:
            county+=1
            countx=0

    equals_Button.grid(row=county, column=countx, columnspan=1, sticky="nsew")
    memory_Button.grid(row=county+1, column=0, columnspan=1, sticky="nsew")
    recall_Button.grid(row=county+1, column=2, columnspan=1, sticky="nsew")
    clear_Button.grid(row=county+1, column=1, columnspan=1, sticky="nsew")
    window.mainloop()

main()
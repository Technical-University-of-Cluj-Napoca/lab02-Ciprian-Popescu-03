import os
from BST import BST
from search_engine import get_char

if __name__ == "__main__":
    print("Start typing (press ESC to quit):")
    prefix = ""

    bst = BST("ex04/words.txt", file=True)

    while True:
        ch = get_char()

        if ord(ch) == 27:
            print("\nExiting...")
            break

        if ch in ("\b", "\x7f"):
            prefix = prefix[:-1]
        elif ch == "\r":  
            continue
        else:
            prefix += ch.lower()


        os.system("cls" if os.name == "nt" else "clear")
        print(f"Current input >> {prefix}")
        suggestions = bst.autocomplete(prefix)
        if suggestions:
            for s in suggestions[:5]:  
                print(s)
        else:
            print("No matches found.")

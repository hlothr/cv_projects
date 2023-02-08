import tkinter as tk
import os

WORD_TYPING_SPEED = 150


def get_input_file_content():
    """
    Get the content of the input text file
    """
    input_file_path = input_txt.get("1.0", "end-1c").strip()
    words = tk.Listbox(root)
    try:
        if os.path.isfile(input_file_path) and input_file_path.endswith('.txt'):
            with open(input_file_path, 'r') as file:
                words = file.read()
            output_txt.insert(tk.END, words)
            output_txt.see(tk.END)  # scroll to the end of the text widget
            output_txt.config(state='disabled')  # make the text widget readonly
        else:
            raise ValueError("Error: Not specified path/invalid file path or file extension")
    except Exception as e:
        output_txt.insert(tk.END, str(e))
    return words


def type_words(words):
    """
    Type the words of the text file one by one
    """
    if words:
        word = words.pop(0)
        word_label.config(text=word)
        root.after(WORD_TYPING_SPEED, type_words, words)
    else:
        word_label.config(text="All words typed")


# Create the main window
root = tk.Tk()
root.title("Text Typer")

# Create labels, text inputs and buttons
file_path_label = tk.Label(root,
                           text="Set the directory for the text file")
input_txt = tk.Text(root, height=1,
                    width=200,
                    bg="light yellow",
                    )
output_txt = tk.Text(root, height=40,
                     width=200,
                     bg="light cyan",
                     )
display_btn = tk.Button(root,
                        height=2,
                        width=20,
                        text="Show",
                        command=get_input_file_content(),
                        )
word_label = tk.Label(root, text="",
                      height=5,
                      width=20,
                      font=('Helvetica bold', 26),
                      bg='pink',
                      )
start_btn = tk.Button(root,
                      height=2,
                      width=20,
                      text='Start',
                      command=lambda: type_words(get_input_file_content().split(' ')),
                      )

# Pack the widgets
file_path_label.pack()
input_txt.pack()
display_btn.pack()
output_txt.pack()
start_btn.pack()
word_label.pack()
root.mainloop()
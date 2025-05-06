import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# Function to connect to the database
def connect_db():
    return sqlite3.connect("spel.db")


# Function to refresh the table of words
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT wl.OriginalWord, wl.AbbrvWord, wt.type_name, ar.rule_name
    FROM word_library wl
    JOIN word_types wt ON wl.WordType = wt.id
    JOIN abbreviation_rules ar ON wl.AbbrvRule = ar.id
    ORDER BY wl.OriginalWord
    """)
    
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    
    conn.close()


# Function to add a word to the database
def add_word():
    original = original_entry.get()
    abbreviation = abbrv_entry.get()
    word_type = word_type_combobox.get()
    abbrv_rule = abbrv_rule_combobox.get()

    if not original or not abbreviation:
        messagebox.showerror("Input Error", "Both original and abbreviated words are required!")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Get the corresponding type and rule IDs
    cursor.execute("SELECT id FROM word_types WHERE type_name = ?", (word_type,))
    word_type_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM abbreviation_rules WHERE rule_name = ?", (abbrv_rule,))
    abbrv_rule_id = cursor.fetchone()[0]

    # Insert the word into the database
    cursor.execute("""
    INSERT INTO word_library (OriginalWord, AbbrvWord, WordType, AbbrvRule)
    VALUES (?, ?, ?, ?)
    """, (original, abbreviation, word_type_id, abbrv_rule_id))

    conn.commit()
    conn.close()

    refresh_table()


# Function to remove a word from the database
def remove_word():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a word to remove.")
        return

    word = tree.item(selected_item)["values"][0]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM word_library WHERE OriginalWord = ?", (word,))
    conn.commit()
    conn.close()

    refresh_table()


# Function to search words in the database
def search_words():
    search_term = search_entry.get()
    
    if not search_term:
        messagebox.showwarning("Search Error", "Please enter a search term.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT wl.OriginalWord, wl.AbbrvWord, wt.type_name, ar.rule_name
    FROM word_library wl
    JOIN word_types wt ON wl.WordType = wt.id
    JOIN abbreviation_rules ar ON wl.AbbrvRule = ar.id
    WHERE wl.OriginalWord LIKE ?
    ORDER BY wl.OriginalWord
    """, ('%' + search_term + '%',))

    rows = cursor.fetchall()
    
    for row in tree.get_children():
        tree.delete(row)

    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()


# Function to edit a word in the database
def edit_word():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a word to edit.")
        return

    original = tree.item(selected_item)["values"][0]
    abbreviation = tree.item(selected_item)["values"][1]
    word_type = tree.item(selected_item)["values"][2]
    abbrv_rule = tree.item(selected_item)["values"][3]

    # Update entry fields with the selected word data
    original_entry.delete(0, tk.END)
    abbrv_entry.delete(0, tk.END)
    original_entry.insert(0, original)
    abbrv_entry.insert(0, abbreviation)
    word_type_combobox.set(word_type)
    abbrv_rule_combobox.set(abbrv_rule)

    # Remove the word from the tree
    remove_word()

    # Then re-add the updated word
    add_word()


# Setup the Tkinter window
root = tk.Tk()
root.title("SPEL Word Abbreviation System")

# Frame for the form
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Original word input
original_label = tk.Label(frame, text="Original Word:")
original_label.grid(row=0, column=0, padx=10, pady=5)
original_entry = tk.Entry(frame, width=20)
original_entry.grid(row=0, column=1, padx=10, pady=5)

# Abbreviated word input
abbrv_label = tk.Label(frame, text="Abbreviated Word:")
abbrv_label.grid(row=1, column=0, padx=10, pady=5)
abbrv_entry = tk.Entry(frame, width=20)
abbrv_entry.grid(row=1, column=1, padx=10, pady=5)

# Word type combobox
word_type_label = tk.Label(frame, text="Word Type:")
word_type_label.grid(row=2, column=0, padx=10, pady=5)
word_type_combobox = ttk.Combobox(frame, values=["Noun", "Verb", "Adjective", "Adverb", "Preposition", "Conjunction", "Pronoun", "Article"], state="readonly")
word_type_combobox.grid(row=2, column=1, padx=10, pady=5)

# Abbreviation rule combobox
abbrv_rule_label = tk.Label(frame, text="Abbreviation Rule:")
abbrv_rule_label.grid(row=3, column=0, padx=10, pady=5)
abbrv_rule_combobox = ttk.Combobox(frame, values=["Phonetic", "Truncation", "Vowel Removal", "Standard"], state="readonly")
abbrv_rule_combobox.grid(row=3, column=1, padx=10, pady=5)

# Buttons for actions
add_button = tk.Button(frame, text="Add Word", command=add_word)
add_button.grid(row=4, column=0, padx=10, pady=10)

remove_button = tk.Button(frame, text="Remove Word", command=remove_word)
remove_button.grid(row=4, column=1, padx=10, pady=10)

edit_button = tk.Button(frame, text="Edit Word", command=edit_word)
edit_button.grid(row=4, column=2, padx=10, pady=10)

# Search bar
search_label = tk.Label(frame, text="Search Word:")
search_label.grid(row=5, column=0, padx=10, pady=5)
search_entry = tk.Entry(frame, width=20)
search_entry.grid(row=5, column=1, padx=10, pady=5)

search_button = tk.Button(frame, text="Search", command=search_words)
search_button.grid(row=5, column=2, padx=10, pady=10)

# Treeview to display words
tree = ttk.Treeview(root, columns=("OriginalWord", "AbbrvWord", "WordType", "AbbrvRule"), show="headings")
tree.heading("OriginalWord", text="Original Word")
tree.heading("AbbrvWord", text="Abbreviated Word")
tree.heading("WordType", text="Word Type")
tree.heading("AbbrvRule", text="Abbreviation Rule")
tree.pack(padx=20, pady=20)

# Refresh the table on startup
refresh_table()

root.mainloop()

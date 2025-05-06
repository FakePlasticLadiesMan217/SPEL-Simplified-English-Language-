import sqlite3

conn = sqlite3.connect("spel.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS word_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS abbreviation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS word_library (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    OriginalWord TEXT NOT NULL,
    AbbrvWord TEXT NOT NULL,
    WordType INTEGER NOT NULL,
    AbbrvRule INTEGER NOT NULL,
    FOREIGN KEY (WordType) REFERENCES word_types(id),
    FOREIGN KEY (AbbrvRule) REFERENCES abbreviation_rules(id)
);
""")

# Insert default types
word_types = ['Noun', 'Verb', 'Adjective', 'Adverb', 'Preposition', 'Conjunction', 'Pronoun', 'Article']
rules = ['Phonetic', 'Truncation', 'Vowel Removal', 'Standard']

for wt in word_types:
    cursor.execute("INSERT OR IGNORE INTO word_types (type_name) VALUES (?)", (wt,))
for r in rules:
    cursor.execute("INSERT OR IGNORE INTO abbreviation_rules (rule_name) VALUES (?)", (r,))

conn.commit()
conn.close()

print("Database and tables initialized successfully.")

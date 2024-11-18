# Import library for database operations
import sqlite3
# Import GUI components from tkinter
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Function to create a database and table if not already existing
def create_database():
    # Connect to (or create) the database file
    conn = sqlite3.connect('nilai_siswa_.db')
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Create the table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT NOT NULL,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi_fakultas TEXT
        )
    ''')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function to fetch all data from the database
def fetch_data():
    # Connect to the database
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    # Execute the command to select all records
    cursor.execute('SELECT * FROM nilai_siswa')
    # Fetch all results
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to save a new record to the database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    # Insert a new record with the provided data
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

# Function to update an existing record in the database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    # Update the record with the given ID
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

# Function to delete a record from the database based on ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    # Execute the delete command
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Function to calculate prediction based on input scores
def calculate_prediction(biologi, fisika, inggris):
    # Determine the faculty prediction based on the highest score
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak diketahui"

# Function to handle the submit button click event
def submit():
    try:
        # Get the input data from user
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # Check if the name field is empty
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        # Calculate the predicted faculty
        prediksi = calculate_prediction(biologi, fisika, inggris)
        # Save the data to the database
        save_to_database(nama, biologi, fisika, inggris, prediksi)
        # Show a success message
        messagebox.showinfo("Sukses", f"Data Berhasil disimpan!\nPrediksi fakultas: {prediksi}")
        # Clear input fields and refresh the table
        clear_inputs()
        populate_table()

    except ValueError as e:
        # Display an error message if the input is invalid
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Function to handle the update button click event
def update():
    try:
        # Check if a record is selected from the table
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk di-update.")

        # Get the selected record ID and input data
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # Check if the name field is empty
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        # Calculate the predicted faculty
        prediksi = calculate_prediction(biologi, fisika, inggris)
        # Update the data in the database
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)
        # Show a success message
        messagebox.showinfo("Sukses", "Data Berhasil diperbarui!")
        # Clear input fields and refresh the table
        clear_inputs()
        populate_table()

    except ValueError as e:
        # Display an error message if there is an issue
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Function to handle the delete button click event
def delete():
    try:
        # Check if a record is selected from the table
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk dihapus!")

        # Get the selected record ID
        record_id = int(selected_record_id.get())
        # Delete the data from the database
        delete_database(record_id)
        # Show a success message
        messagebox.showinfo("Sukses", "Data Berhasil dihapus!")
        # Clear input fields and refresh the table
        clear_inputs()
        populate_table()

    except ValueError as e:
        # Display an error message if there is an issue
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Function to clear input fields
def clear_inputs():
    # Reset all input fields to empty
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Function to populate the table with data from the database
def populate_table():
    # Clear all existing rows in the table
    for row in tree.get_children():
        tree.delete(row)
    # Insert all fetched rows into the table
    for row in fetch_data():
        tree.insert('', 'end', values=row)

# Function to fill input fields with data when a table row is selected
def fill_inputs_from_table(event):
    try:
        # Get the selected item from the table
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        # Set the input fields with the selected row's data
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        # Display an error message if no valid data is selected
        messagebox.showerror("Error", "Pilih data yang valid")

# Call function to create database and table if not existing
create_database()

# Create the main window for the application
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Define variables for user input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

# Create and place labels and input fields in the window
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Bahasa Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Membuat button
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

columns = ('id', 'nama_siswa', 'biologi', 'fisika', 'inggris', 'prediksi_fakultas')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

populate_table()

root.mainloop()
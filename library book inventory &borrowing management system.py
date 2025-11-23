import csv
import os

# --- Configuration ---
FILENAME = "library.csv"
FIELDNAMES = ["book_id", "title", "author", "quantity"]

def init_file():
    if not os.path.exists(FILENAME):
        try:
            with open(FILENAME, "w", newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(FIELDNAMES)
            print(f"Initialized file: {FILENAME}")
        except IOError as e:
            print(f"Error initializing file: {e}")

def get_all_books():
    try:
        with open(FILENAME, "r", newline="", encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=FIELDNAMES)
            next(reader) 
            return list(reader)
    except FileNotFoundError:
        print(f"Error: File '{FILENAME}' not found. Please ensure it exists or run main_menu.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return []

def write_all_books(rows):
    try:
        with open(FILENAME, "w", newline="", encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(rows)
        return True
    except IOError as e:
        print(f"Error writing to file: {e}")
        return False

def add_book():
    print("\n--- Add New Book ---")
    book_id = input("Enter Book ID (must be unique): ")
    
    rows = get_all_books()
    if any(row["book_id"] == book_id for row in rows):
        print(f"Error: Book ID '{book_id}' already exists. Please choose a unique ID.\n")
        return

    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    
    while True:
        try:
            quantity = int(input("Enter Quantity: "))
            if quantity < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid quantity. Please enter a non-negative integer.")

    new_book = {
        "book_id": book_id, 
        "title": title, 
        "author": author, 
        "quantity": str(quantity)
    }

    try:
        with open(FILENAME, "a", newline="", encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerow(new_book)
            print("Book added successfully!\n")
    except IOError as e:
        print(f"Error appending book: {e}")

def view_books():
    print("\n--- All Books in Library ---")
    rows = get_all_books()

    if not rows:
        print("No books available.\n")
        return

    print(f"{'ID':<10}{'Title':<30}{'Author':<20}{'Quantity':<10}")
    print("-" * 70)
    
    for row in rows:
        print(f"{row['book_id']:<10}{row['title']:<30}{row['author']:<20}{row['quantity']:<10}")
    print()

def search_book():
    print("\n--- Search Book ---")
    keyword = input("Enter Book ID or Book Title (partial match is OK) to search: ").strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.\n")
        return
        
    rows = get_all_books()
    found_books = []
    
    for row in rows:
        if keyword == row["book_id"].lower() or keyword in row["title"].lower():
            found_books.append(row)
    
    if found_books:
        print("Book(s) found:")
        print(f"{'ID':<10}{'Title':<30}{'Author':<20}{'Quantity':<10}")
        print("-" * 70)
        for book in found_books:
            print(f"{book['book_id']:<10}{book['title']:<30}{book['author']:<20}{book['quantity']:<10}")
    else:
        print("Book not found.\n")
    print()

def borrow_book():
    print("\n--- Borrow Book ---")
    book_id = input("Enter Book ID to borrow: ")

    rows = get_all_books()
    book_found = False
    
    for row in rows:
        if row["book_id"] == book_id:
            book_found = True
            try:
                current_quantity = int(row["quantity"])
                if current_quantity > 0:
                    row["quantity"] = str(current_quantity - 1)
                    if write_all_books(rows):
                        print("Book issued successfully!\n")
                else:
                    print("Book out of stock!\n")
            except ValueError:
                print("Error: Book quantity is not a valid number.\n")
            return

    if not book_found:
        print("Book ID not found.\n")

def return_book():
    print("\n--- Return Book ---")
    book_id = input("Enter Book ID to return: ")

    rows = get_all_books()
    book_found = False

    for row in rows:
        if row["book_id"] == book_id:
            book_found = True
            try:
                current_quantity = int(row["quantity"])
                row["quantity"] = str(current_quantity + 1)
                if write_all_books(rows):
                    print("Book returned successfully!\n")
            except ValueError:
                print("Error: Book quantity is not a valid number.\n")
            return

    if not book_found:
        print("Book ID not found.\n")

def update_book():
    print("\n--- Update Book ---")
    book_id = input("Enter Book ID to update: ")

    rows = get_all_books()
    book_found = False

    for row in rows:
        if row["book_id"] == book_id:
            book_found = True
            print(f"Current details: Title='{row['title']}', Author='{row['author']}', Quantity='{row['quantity']}'")
            
            row["title"] = input("New Title (leave blank to keep current): ") or row["title"]
            row["author"] = input("New Author (leave blank to keep current): ") or row["author"]
            
            new_quantity = input("New Quantity (leave blank to keep current): ")
            if new_quantity:
                while True:
                    try:
                        quantity_val = int(new_quantity)
                        if quantity_val < 0:
                            raise ValueError
                        row["quantity"] = str(quantity_val)
                        break
                    except ValueError:
                        print("Invalid quantity. Please enter a non-negative integer.")
                        new_quantity = input("New Quantity: ")
            
            if write_all_books(rows):
                print("Book updated successfully!\n")
            return
            
    if not book_found:
        print("Book ID not found.\n")

def delete_book():
    print("\n--- Delete Book ---")
    book_id = input("Enter Book ID to delete: ")

    rows = get_all_books()
    initial_count = len(rows)
    
    new_rows = [row for row in rows if row["book_id"] != book_id]

    if len(new_rows) == initial_count:
        print("Book ID not found.\n")
        return

    if write_all_books(new_rows):
        print("Book deleted successfully!\n")

def main_menu():
    init_file()
    while True:
        print("="*40)
        print("📚 Library Book Management System 📚")
        print("="*40)
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Update Book")
        print("7. Delete Book")
        print("8. Exit")
        print("-" * 40)

        choice = input("Enter choice (1-8): ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            borrow_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            update_book()
        elif choice == "7":
            delete_book()
        elif choice == "8":
            print("Exiting program. Goodbye! 👋")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 8.\n")

if __name__ == "__main__":
    main_menu()
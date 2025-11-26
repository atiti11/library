import mysql.connector
from datetime import date

DB_NAME = "library_2"
PASSWORD = "1111"  # TODO 1: změň na svoje heslo

# --- Databázové funkce ---
def create_database_if_not_exists(cursor, db_name):
    cursor.execute(
        "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
        (db_name,)
    )
    # pokud schéma ještě neexistuje -> vytvoř ho
    if not cursor.fetchone():
        cursor.execute(f"CREATE DATABASE {db_name}")


def create_tables_if_not_exist(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Books (
                BookID INT PRIMARY KEY AUTO_INCREMENT,
                Title VARCHAR(255) NOT NULL,
                Author VARCHAR(255) NOT NULL,
                Available BOOLEAN DEFAULT TRUE
            );
        """)
        
        # TODO 2: dovnitř cursor.execute napiš příkaz pro vytvoření tabulky Members
        cursor.execute()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Loans (
                LoanID INT PRIMARY KEY AUTO_INCREMENT,
                BookID INT NOT NULL,
                MemberID INT NOT NULL,
                LoanDate DATE NOT NULL,
                ReturnDate DATE DEFAULT NULL,
                FOREIGN KEY (BookID) REFERENCES Books(BookID),
                FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
            );
        """)
        conn.commit()
    finally:
        cursor.close()


def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=PASSWORD
        )
        cursor = conn.cursor()
        create_database_if_not_exists(cursor, DB_NAME)
        cursor.close()
        conn.close()

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=PASSWORD,
            database=DB_NAME
        )
        create_tables_if_not_exist(conn)
        return conn
    except mysql.connector.Error as e:
        raise ValueError(f"Chyba připojení nebo nastavení databáze: {e}")


def find_member_by_name(conn, name):
    # TODO 3: implementuj správnou práci s kurzorem
    # - vytvoř ho do proměnné cursor
    # - vytvoř blok finally, ve kterém cursor uzavři
    try:
        cursor = None
        cursor.execute("SELECT MemberID FROM Members WHERE Name = %s", (name,))
        result = cursor.fetchone()
        return result["MemberID"] if result else None
    except mysql.connector.Error as e:
        raise ValueError(f"Chyba při hledání člena: {e}")


def get_available_books(conn):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Books") # TODO 4: Uprav příkaz tak, aby vybral pouze dostupné knihy
        books = cursor.fetchall()
        return books
    except mysql.connector.Error as e:
        raise ValueError(f"Chyba při načítání knih: {e}")
    finally:
        cursor.close()

def borrow_book_db(conn, member_id, book_id):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Available FROM Books WHERE BookID = %s", (book_id,))
        status = cursor.fetchone()
        if not status or not status["Available"]:
            raise ValueError("Kniha není dostupná.")
        
        # TODO 6: vytvoř nový záznam o půjčce a akutalizuj knihu s daným id, celé připojení commitni, aby se vše uložilo
        cursor.execute(
            "INSERT INTO Loans (BookID, MemberID, LoanDate) VALUES ()",
        )
        cursor.execute("UPDATE Books SET Available = FALSE WHERE BookID = ")
    
    except mysql.connector.Error as e:
        raise ValueError(f"Chyba při půjčení knihy: {e}")
    finally:
        cursor.close()

def get_user_loans(conn, member_id):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.LoanID, b.BookID, b.Title
            FROM Loans l
            JOIN Books b ON l.BookID = b.BookID
            WHERE l.MemberID = %s AND l.ReturnDate IS NULL
        """, (member_id,))
        # TODO 5: do proměnné loans ulož všechny výpůjčky uživatele, které kurzor našel
        loans = None
        return loans
    except mysql.connector.Error as e:
        raise ValueError(f"Chyba při načítání půjčených knih: {e}")
    finally:
        cursor.close()

def return_book_db(conn, member_id, book_id):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Loans SET ReturnDate = %s
            WHERE BookID = %s AND MemberID = %s AND ReturnDate IS NULL
        """, (date.today(), book_id, member_id))
        cursor.execute("UPDATE Books SET Available = TRUE WHERE BookID = %s", (book_id,))
        conn.commit()
    except mysql.connector.Error as e:
        raise ValueError(f"Chyba při vracení knihy: {e}")
    finally:
        cursor.close()

# --- Uživatelské funkce ---
def get_member(conn):
    name = input("Zadej své jméno: ")
    try:
        member_id = find_member_by_name(conn, name)
        return member_id
    except ValueError as e:
        print(e)
        return None


def show_available_books(conn):
    try:
        books = get_available_books(conn)
        if books:
            print("\nDostupné knihy:")
            for book in books:
                print(f"ID: {book['BookID']} | Název: {book['Title']} | Autor: {book['Author']}")
        else:
            print("Žádné knihy nejsou momentálně dostupné.")
    except ValueError as e:
        print(e)


def borrow_book(conn, member_id):
    try:
        books = get_available_books(conn)
        if not books:
            print("Žádné knihy nejsou k dispozici.")
            return
        print("\nKnihy k půjčení:")
        for book in books:
            print(f"ID: {book['BookID']} | Název: {book['Title']}")
        book_id = int(input("Zadej ID knihy, kterou chceš půjčit: "))
        borrow_book_db(conn, member_id, book_id)
        print("✅ Kniha byla úspěšně půjčena.")
    except (ValueError, ValueError) as e:
        print(f"❌ Chyba: {e}")


def list_all_users_books(conn, member_id):
    try:
        loans = get_user_loans(conn, member_id)
        if not loans:
            print("Nemáš půjčené žádné knihy.")
            return 0
        print("\nKnihy, které máš půjčené:")
        for loan in loans:
            print(f"{loan['Title']} (ID: {loan['BookID']})")
        return len(loans)
    except ValueError as e:
        print(e)
        return 0


def return_book(conn, member_id):
    if list_all_users_books(conn, member_id) < 1:
        return
    try:
        book_id = int(input("Zadej ID knihy, kterou chceš vrátit: "))
        return_book_db(conn, member_id, book_id)
        print("✅ Kniha byla úspěšně vrácena.")
    except (ValueError, ValueError) as e:
        print(f"❌ Chyba: {e}")


# --- Hlavní program ---
def main():
    try:
        conn = connect_to_db()
    except ValueError as e:
        print(f"Nelze navázat spojení s databází: {e}")
        return

    member_id = get_member(conn)
    if not member_id:
        print("Uživatel nebyl nalezen.")
        return

    while True:
        print("\n--- MENU ---")
        print("1. Zobrazit dostupné knihy")
        print("2. Zobrazit půjčené knihy")
        print("3. Půjčit si knihu")
        print("4. Vrátit knihu")
        print("5. Ukončit program")

        choice = input("Zadej číslo akce: ")

        if choice == "1":
            show_available_books(conn)
        elif choice == "2":
            list_all_users_books(conn, member_id)
        elif choice == "3":
            borrow_book(conn, member_id)
        elif choice == "4":
            return_book(conn, member_id)
        elif choice == "5":
            print("👋 Ukončuji program. Nashledanou!")
            break
        else:
            print("❌ Neplatná volba. Zadej číslo 1–5.")

    conn.close()


if __name__ == "__main__":
    main()

# Grāmatnīcas inventāra pārvaldības sistēma
# Ar Tkinter GUI un datu saglabāšana/ielādēšana no JSON faila

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json, os

# Faila konfigurācija
DATA_FILE = "stock.json"

# Datu saglabāšana/ielāde
def save_data(stock):
    """Saglabā pašreizējos datus JSON failā!"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4, ensure_ascii=False)

def load_data():
    """Ielādē datus no JSON faila! (ja tāds eksistē)"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("୨୧ ‧₊ KĻŪDA", "Inventāra datne ir bojāta... Tiek izveidots jauns saraksts!")
            return {}
    return {
        "9780765377135": {"title": "Mistborn #1", "author": "Sanderson Brandon", "price": 19.99, "quantity": 12},
        "9780007351053": {"title": "The Picture of Dorian Gray", "author": "Wilde Oscar", "price": 3.50,
                          "quantity": 3},
        "9780356519142": {"title": "Emily Wilde's Encyclopaedia of Faeries", "author": "Fawcett Heather",
                          "price": 10.95, "quantity": 5},
        "9781471407277": {"title": "The Cruel Prince", "author": "Black Holly", "price": 11.95, "quantity": 1},
        "9781408891384": {"title": "The Song of Achilles", "author": "Madeline Miller", "price": 9.90,
                          "quantity": 4},
        "9781908670427": {"title": "Soviet Milk", "author": "Ikstena Nora", "price": 15.95, "quantity": 15}
    }

# Sistēmas klase
# Galvenais logs/main menu, nosaukums un izmērs, krāsa
class GramatuSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("✧˖°✧˖°GRĀMATNĪCAS INVENTĀRA SISTĒMA✧˖°✧˖°")
        self.root.geometry("1050x550")
        self.root.configure(bg="#FFBBE1")

        self.stock = load_data()
        self.setup_treeview()
        self.setup_buttons()
        self.refresh_table()

    # Tabulas stils/dizains
    def setup_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#B3BFFF",
                        foreground="#211832",
                        rowheight=25,
                        fieldbackground="#B3BFFF",
                        font=("Times New Roman", 12))
        style.configure("Treeview.Heading",
                        background="#DD7BDF",
                        foreground="white",
                        font=("Times New Roman", 12, "bold"))

        style.map("Treeview",
                  background=[("selected", "#FFF58A")],
                  foreground=[("selected", "#000000")])

    # Tabula/table, tā stabiņi (columns), nosaukumi un izkārtojums
        columns = ("ISBN", "Nosaukums", "Autors", "Cena", "Daudzums")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10, padx=10)

    # Pogas/buttons, to pozīcija, stils un nosaukums
    def setup_buttons(self):
        frame = tk.Frame(root)
        frame.pack(pady=10)
        btn_style = {"bg": "#DD7BDF", "fg": "white", "font": ("Times New Roman", 12, "bold"), "width": 18, "height": 1}
        tk.Button(frame, text="+ Pievienot grāmatu", command=self.add_book, **btn_style).grid(row=0, column=0, padx=6, pady=5)
        tk.Button(frame, text="⌕ Meklēt grāmatu", command=self.search_book, **btn_style).grid(row=0, column=1, padx=6, pady=5)
        tk.Button(frame, text="× Dzēst grāmatu", command=self.delete_book, **btn_style).grid(row=0, column=2, padx=6, pady=5)
        tk.Button(frame, text="↻ Atjaunot sarakstu", command=self.refresh_table, **btn_style).grid(row=0, column=3, padx=6, pady=5)
        tk.Button(frame, text="୨୧ ‧₊ Iziet", command=lambda: (save_data(self.stock), root.destroy()), **btn_style).grid(row=0, column=4,
                                                                                                              padx=6, pady=5)

    # GUI darbības funckijas - atjaunot tabulu, pievienot + saglabāt jaunu grāmatu, meklēt un dzēst grāmatas
    def refresh_table(self):
        """Atjauno/refresh tabulu ar visām grāmatām!"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for isbn, book in self.stock.items():
            self.tree.insert("", "end", values=(isbn, book["title"], book["author"], f"€{book['price']}", book["quantity"]))

    def add_book(self):
        """Pievieno jaunu grāmatu!"""
        self.add_win = tk.Toplevel(root)
        self.add_win.title("✧˖°.Pievienot grāmatu")
        self.add_win.geometry("600x400")
        self.add_win.configure(bg="#FFBBE1")

        self.isbn_entry = self.labeled_entry("☆ ISBN:")
        self.title_entry = self.labeled_entry("☆ Nosaukums:")
        self.author_entry = self.labeled_entry("☆ Autors:")
        self.price_entry = self.labeled_entry("☆ Cena (€):")
        self.quantity_entry = self.labeled_entry("☆ Daudzums:")

        tk.Button(self.add_win, text="✧˖°.Saglabāt", command=self.save_book,
                  bg="#DD7BDF", fg="white", font=("Times New Roman", 12, "bold"),
                  relief="raised", width=15).pack(pady=15)

    def labeled_entry(self, text):
        frame = tk.Frame(self.add_win, bg="#FFBBE1")
        frame.pack(pady=3)
        tk.Label(frame, text=text, bg="#FFBBE1", fg="#211832", font=("Times New Roman", 12, "bold")).pack()
        entry = tk.Entry(frame, width=30)
        entry.pack()
        return entry

    def save_book(self):
        isbn = self.isbn_entry.get().strip()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        price_text = self.price_entry.get().strip()
        quantity_text = self.quantity_entry.get().strip()

        if not all([isbn, title, author, price_text, quantity_text]):
            messagebox.showerror("୨୧ ‧₊ KĻŪDA", "Visi lauki ir obligāti jāaizpilda!")
            return
        if isbn in self.stock:
            messagebox.showerror("୨୧ ‧₊ KĻŪDA", "Grāmata ar šo ISBN jau eksistē!")
            return
        if not all(c.isdigit() or c == '-' for c in isbn):
            messagebox.showerror("୨୧ ‧₊ KĻŪDA", "ISBN drīkst saturēt tikai ciparus un defises (-)!")
            return
        try:
            price = float(price_text)
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("୨୧ ‧₊ KĻŪDA", "Cena jābūt pozitīvam skaitlim!")
            return
        try:
            quantity = int(quantity_text)
            if quantity < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("୨୧ ‧₊ KĻŪDA", "Daudzumam jābūt veselam skaitlim (0 vai lielākam)!")
            return

        self.stock[isbn] = {"title": title, "author": author, "price": price, "quantity": quantity}
        save_data(self.stock)
        messagebox.showinfo("Veiksmīgi", f"Grāmata '{title}' pievienota!")
        self.add_win.destroy()
        self.refresh_table()

    def search_book(self):
        """Meklē grāmatu pēc ISBN, nosaukuma vai autora!"""
        query = simpledialog.askstring("✧˖°.Meklēt", "Ievadiet ISBN, nosaukumu vai autoru:")
        if not query:
            return
        results = []
        for isbn, book in self.stock.items():
            if query.lower() in isbn.lower() or query.lower() in book["title"].lower() or query.lower() in book[
                "author"].lower():
                results.append((isbn, book))
        if results:
            result_text = "\n\n".join([
                f"{b['title']} ({b['author']})\nISBN: {i}, Cena: €{b['price']}, Daudzums: {b['quantity']}"
                for i, b in results
            ])
            messagebox.showinfo("✧˖°Rezultāti", result_text)
        else:
            messagebox.showwarning("୨୧ ‧₊ Nav atrasts", "Neviena grāmata neatbilst meklēšanai!")

    def delete_book(self):
        """Dzēš izvēlēto grāmatu pēc ISBN!"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("୨୧ ‧₊ Brīdinājums", "Lūdzu, izvēlieties grāmatu, kuru dzēst!")
            return
        values = self.tree.item(selected, "values")
        isbn = values[0]
        if messagebox.askyesno("୨୧ ‧₊ Apstiprinājums", f"Vai tiešām dzēst grāmatu ar ISBN {isbn}?"):
            del self.stock[isbn]
            save_data(self.stock)
            self.refresh_table()
            messagebox.showinfo("✧˖° Dzēsts", "Grāmata veiksmīgi izdzēsta!")

# Ielādēt datus un parādīt tabulā
if __name__ == "__main__":
    root = tk.Tk()
    app = GramatuSistema(root)
    root.mainloop()
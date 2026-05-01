import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []
        self.load_movies()

        # --- Интерфейс ---
        # Поля ввода
        tk.Label(root, text="Название").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр").grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(root)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Год").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(root)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Рейтинг").grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = tk.Entry(root)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопки
        tk.Button(root, text="Добавить фильм", command=self.add_movie).grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        tk.Label(root, text="Фильтр по жанру").grid(row=5, column=0, padx=5)
        self.filter_genre = tk.Entry(root)
        self.filter_genre.grid(row=5, column=1, padx=5)
        tk.Button(root, text="Фильтровать", command=self.filter_by_genre).grid(row=5, column=2, padx=5)

        tk.Label(root, text="Фильтр по году").grid(row=6, column=0, padx=5)
        self.filter_year = tk.Entry(root)
        self.filter_year.grid(row=6, column=1, padx=5)
        tk.Button(root, text="Фильтровать", command=self.filter_by_year).grid(row=6, column=2, padx=5)

        # Таблица
        self.columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(root, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)
        self.tree.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        # Заполнение таблицы
        self.update_tree()

    def validate_input(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return False

        if not year.isdigit() or not (1888 <= int(year) <= 2026):
            messagebox.showerror("Ошибка", "Год должен быть числом от 1888 до 2026.")
            return False

        try:
            rating = float(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
            return False

        return True

    def add_movie(self):
        if self.validate_input():
            movie = {
                "title": self.title_entry.get(),
                "genre": self.genre_entry.get(),
                "year": int(self.year_entry.get()),
                "rating": float(self.rating_entry.get())
            }
            self.movies.append(movie)
            self.save_movies()
            self.update_tree()
            # Очистка полей
            self.title_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.rating_entry.delete(0, tk.END)

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for movie in self.movies:
            self.tree.insert("", tk.END,
                             values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def filter_by_genre(self):
        genre = self.filter_genre.get().lower()
        filtered = [m for m in self.movies if genre in m["genre"].lower()]
        self.update_tree_with(filtered)

    def filter_by_year(self):
        year = self.filter_year.get()
        if year.isdigit():
            filtered = [m for m in self.movies if m["year"] == int(year)]
            self.update_tree_with(filtered)

    def update_tree_with(self, data):
         for i in self.tree.get_children():
             self.tree.delete(i)
         for movie in data:
             self.tree.insert("", tk.END,
                              values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def save_movies(self):
         with open("movies.json", "w", encoding="utf-8") as f:
             json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_movies(self):
         if os.path.exists("movies.json"):
             with open("movies.json", "r", encoding="utf-8") as f:
                 self.movies = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
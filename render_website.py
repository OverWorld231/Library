import json
import os
from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv


def render_page(books_page, number, books_pages):
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("template.html")
    os.makedirs("./pages", exist_ok=True)
    rendered_page = template.render(
        paired_books=books_page, 
        page_number=number + 1, 
        total_pages=len(books_pages)
    )
    with open(f"./pages/index{number+1}.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


def on_reload():
    meta_data = os.getenv("META_DATA", "meta_data.json")
    with open(meta_data, "r", encoding="utf-8") as my_file:
        books = json.load(my_file)    
    books_pages = list(chunked(books, 10))
    for number, books_page in enumerate(books_pages):
        render_page(books_page, number, books_pages)


def main():
    load_dotenv()
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".", default_filename="./pages/index1.html")


if __name__ == "__main__":
    main()
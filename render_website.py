import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import os
import more_itertools
import math


def on_reload():
    for page_id, page_books in enumerate(chunked_books, 1):
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('template.html')
        rendered_page = template.render(books=page_books,
                                        pages_amount=math.ceil(len(books)/20),
                                        page_id=page_id,)
        with open(f'pages/index{page_id}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


os.makedirs("pages/", exist_ok=True)

with open("books.json", "r", encoding="utf-8") as my_file:
    books = my_file.read()
books = json.loads(books)
chunked_books = more_itertools.chunked(books, 20)

on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')


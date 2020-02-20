"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
from ADT import list as lt
from ADT import map as map
from DataStructures import listiterator as it


"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores 
y otra para géneros
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de peliculas. Retorna el catalogo inicializado.
    """
   
    catalog = {'moviesList':None, 'directors':None, 'moviesMap': None}
    catalog['moviesList'] = lt.newList("ARRAY_LIST")
    catalog['moviesMap'] = map.newMap (1009, maptype='CHAINING')#2000 movies-smallfile
    catalog['directors'] = map.newMap (4001, maptype='PROBING') #2000 directors-smallfile
    #catalog['moviesMap'] = map.newMap (164531, maptype='CHAINING')#329044 movies-bigfile
    #catalog['directors'] = map.newMap (171863, maptype='PROBING') #85929 directors-bigfile
    return catalog


def newBook (row):
    """
    Crea una nueva estructura para almacenar los actores de una pelicula 
    """
    book = {"book_id": row['book_id'], "title":row['title'], "average_rating":row['average_rating'], "ratings_count":row['ratings_count']}
    return book

def addBookList (catalog, row):
    """
    Adiciona libro a la lista
    """
    books = catalog['booksList']
    book = newBook(row)
    lt.addLast(books, book)

def addBookMap (catalog, row):
    """
    Adiciona libro al map con key=title
    """
    books = catalog['booksMap']
    book = newBook(row)
    map.put(books, book['title'], book, compareByKey)

def newAuthor (name, row):
    """
    Crea una nueva estructura para modelar un autor y sus libros
    """
    author = {'name':"", "authorBooks":None,  "sum_average_rating":0}
    author ['name'] = name
    author['sum_average_rating'] = float(row['average_rating'])
    author ['authorBooks'] = lt.newList('SINGLE_LINKED')
    lt.addLast(author['authorBooks'],row['book_id'])
    return author

def addAuthor (catalog, name, row):
    """
    Adiciona un autor al map y sus libros
    """
    if name:
        authors = catalog['authors']
        author=map.get(authors,name,compareByKey)
        if author:
            lt.addLast(author['authorBooks'],row['book_id'])
            author['sum_average_rating'] += float(row['average_rating'])
        else:
            author = newAuthor(name, row)
            map.put(authors, author['name'], author, compareByKey)


# Funciones de consulta


def getBookInList (catalog, bookTitle):
    """
    Retorna el libro desde la lista a partir del titulo
    """
    pos = lt.isPresent(catalog['booksList'], bookTitle, compareByTitle)
    if pos:
        return lt.getElement(catalog['booksList'],pos)
    return None


def getBookInMap (catalog, bookTitle):
    """
    Retorna el libro desde el mapa a partir del titulo (key)
    """
    return map.get(catalog['booksMap'], bookTitle, compareByKey)


def getAuthorInfo (catalog, authorName):
    """
    Retorna el autor a partir del nombre
    """
    return map.get(catalog['authors'], authorName, compareByKey)

# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )  

def compareByTitle(bookTitle, element):
    return  (bookTitle == element['title'] )

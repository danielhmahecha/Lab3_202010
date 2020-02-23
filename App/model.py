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
    #catalog['moviesMap'] = map.newMap (1009, maptype='CHAINING')#2000 movies-smallfile
    #catalog['directors'] = map.newMap (4001, maptype='PROBING') #2000 directors-smallfile
    catalog['moviesMap'] = map.newMap (164531, maptype='CHAINING')#329044 movies-bigfile
    catalog['directors'] = map.newMap (171863, maptype='PROBING') #85929 directors-bigfile
    
    return catalog


def newMovie(row):

    movie = {"id": row['id'], "genres": row['genres'], "title": row['title'], "vote_average": row['vote_average'], "vote_count": row['vote_count']}
    return movie

def addMovieList (catalog, row):
    """
    Adiciona la pelicula a una lista
    """
    movies = catalog['moviesList']
    movie = newMovie(row)
    lt.addLast (movies, movie)

def addMovieMap(catalog, row):
    """
    Adicion la pelicula al map con key=id
    """
    movies = catalog['moviesMap']
    movie = newMovie(row)
    map.put(movies, movie['id'], movie, compareByKey)

def newDirector (row):
    """
    Crea una nueva estructura para modelar un director y sus películas
    """
    director = {'name':"", "directorMovies":None}
    director ['name'] = row['director_name']
    director ['directorMovies'] = lt.newList('SINGLE_LINKED')
    lt.addLast(director['directorMovies'],row['id'])
    return director

def addDirector (catalog, row):
    """
    Adiciona un autor al map y sus libros
    """
    #if name:
    directors = catalog['directors']
    director=map.get(directors, row['director_name'], compareByKey)
    if director:
        lt.addLast(director['directorMovies'],row['id'])
    else:
        director = newDirector(row)
        map.put(directors, director['name'], director, compareByKey)


# Funciones de consulta


def getBookInList (catalog, bookTitle):
    """
    Retorna el libro desde la lista a partir del titulo
    """
    pos = lt.isPresent(catalog['booksList'], bookTitle, compareByTitle)
    if pos:
        return lt.getElement(catalog['booksList'],pos)
    return None


def getDirectorInMap (catalog, name):
    """
    Retorna el director  desde el mapa de directores a partir del nombre (key)
    """
    return map.get(catalog['directors'], name, compareByKey)

def getMovieInMap (catalog, id):
    """
    Retorna la pelicula desde el mapa de peliculas a partir del id
    """
    return map.get(catalog['moviesMap'], id, compareByKey)



# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )  

def compareByName(name, element):
    return (name == element['name'])


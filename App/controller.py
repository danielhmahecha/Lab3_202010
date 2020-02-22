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
import model
import csv
from ADT import list as lt
from ADT import map as map

from DataStructures import listiterator as it
from Sorting import mergesort as sort
from time import process_time 


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Funcionaes utilitarias

def printList (lst):
    iterator = it.newIterator(lst)
    while  it.hasNext(iterator):
        element = it.next(iterator)
        result = "".join(str(key) + ": " + str(value) + ",  " for key, value in element.items())
        print (result)



def compareratings (movie1, movie2):
    return ( float(movie1['vote_average']) > float(movie2['vote_average']))


# Funciones para la carga de datos 

def loadMovies (catalog, sep=';'):
    """
    Carga las películas del archivo. 
    """
    t1_start = process_time() #tiempo inicial
    moviesfile = cf.data_dir + 'themoviesdb/SmallMoviesDetailsCleaned.csv'
    #moviesfile = cf.data_dir + 'themoviesdb/AllMoviesDetailsCleaned.csv'
    dialect = csv.excel()
    dialect.delimiter=sep
    with open(moviesfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            # Se adiciona la pelicula a la lista de peliculas
            model.addMovieList(catalog, row)
            # Se adiciona la pelicula al mapa de peliculas (key=title)
            model.addMovieMap(catalog, row)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga películas:",t1_stop-t1_start," segundos")   

def loadDirectors (catalog, sep=';'):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por 
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    t1_start = process_time() #tiempo inicial
    castingfile = cf.data_dir + 'themoviesdb/MoviesCastingRaw-small.csv'
    #castingfile = cf.data_dir + 'themoviesdb/AllMoviesCastingRaw.csv'
    dialect = csv.excel()
    dialect.delimiter=sep
    with open(castingfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            # Se adiciona el director al mapa  de directores
            model.addDirector(catalog, row)
          
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga directores:",t1_stop-t1_start," segundos")   


def initCatalog ():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog



def loadData (catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadMovies(catalog)
    loadDirectors(catalog)
    

# Funciones llamadas desde la vista y enviadas al modelo

def getDirectorInfo (catalog, name):
    t1_start = process_time() 
    director = model.getDirectorInMap(catalog, name)
    t1_stop = process_time()
   # print("\nTiempo de ejecución buscar Director:",t1_stop-t1_start," segundos\n")   
    if director:
        return director
    else:
        return None   

def getMoviesByDirector(catalog, name, minavg):
    t1_start = process_time() 
    director = getDirectorInfo (catalog, name)
    ids = director['directorMovies']
    movies = lt.newList('ARRAY_LIST')
    iterator = it.newIterator(ids)
    while  it.hasNext(iterator):
        id = it.next(iterator)
        movie = getMovieInfo (catalog, id)
        if float(movie['vote_average']) >= minavg:
            lt.addLast(movies,movie)
            
    # for id in ids:
    #     movie = getMovieInfo (catalog, id)
    #     if movie['vote_average'] >= minavg:
    #         lt.addLast(movies,movie)
    
    t1_stop = process_time()
    print("\nTiempo de ejecución buscar buenas peliculas por Director:",t1_stop-t1_start," segundos\n")

    return movies

def getMovieInfo(catalog, id):
    t1_start = process_time() #tiempo inicial
    #book=model.getBookInList(catalog, bookTitle)
    movie=model.getMovieInMap(catalog, id)
    t1_stop = process_time() #tiempo final
    #print("Tiempo de ejecución buscar pelicula:",t1_stop-t1_start," segundos")   
    if movie:
        return movie
    else:
        return None   

def getAuthorInfo(catalog, authorName):
    author=model.getAuthorInfo(catalog, authorName)
    if author:
        return author
    else:
        return None    


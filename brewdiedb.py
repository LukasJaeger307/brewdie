# Copyright 2019, Lukas Jäger 
#
# This file is part of Brewdie.
#
# Brewdie is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Brewdie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Brewdie.  If not, see <http://www.gnu.org/licenses/>. 

import sqlite3
import sys

class BrewdieDB:
    def __init__(self):
        try:
            # Establishing a connection
            connection = sqlite3.connect('brewdie.db')
            cursor = connection.cursor()

            # Querying for existing tables
            table_names = []
            for row in cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\''):
                table_names.append(row[0])

            # Creating tables if they don't exist
            if not 'Recipes' in table_names:
                cursor.execute('CREATE TABLE Recipes (name TEXT PRIMARY KEY, type TEXT, boiling_minutes INTEGER)')
            if not 'Malts' in table_names:
                cursor.execute('CREATE TABLE Malts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, gramms REAL, recipe_name TEXT)')
            if not 'Rests' in table_names:
                cursor.execute('CREATE TABLE Rests (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, temperature REAL, minutes INTEGER, position INTEGER, recipe_name TEXT)')
            if not 'HopDosages' in table_names:
                cursor.execute('CREATE TABLE HopDosages (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, minute INTEGER, gramms REAL, recipe_name TEXT)')

            connection.commit()
        
        except sqlite3.Error as e:
            if connection:
                connection.rollback()
                sys.exit(1)

        finally:
            if connection:
                connection.close()

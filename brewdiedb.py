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
from recipe import *
from brew import *

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
                cursor.execute('CREATE TABLE Recipes (name TEXT PRIMARY KEY, '
                    'type TEXT, boiling_minutes INTEGER, litres REAL, '
                    'sugar_gramms_per_litre REAL, correction_factor REAL)')
            if not 'Malts' in table_names:
                cursor.execute('CREATE TABLE Malts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, gramms REAL, recipe_name TEXT)')
            if not 'Rests' in table_names:
                cursor.execute('CREATE TABLE Rests (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, degrees REAL, minutes INTEGER, position INTEGER, recipe_name TEXT)')
            if not 'HopDosages' in table_names:
                cursor.execute('CREATE TABLE HopDosages (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, minutes INTEGER, gramms REAL, recipe_name TEXT)')
            if not 'Brews' in table_names:
                cursor.execute('CREATE TABLE Brews ('
                        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'datetime timestamp NOT NULL,'
                        'recipe TEXT NOT NULL,'
                        'note TEXT,'
                        'gravity_initial REAL,'
                        'gravity_final REAL)')
            if not 'AdditionalIngredients' in table_names:
                cursor.execute('CREATE TABLE AdditionalIngredients ('
                        'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                        'name TEXT NOT NULL,'
                        'gramms REAL,'
                        'note TEXT, '
                        'recipe_name TEXT NOT NULL)')

            connection.commit()
        
        except sqlite3.Error as e:
            if connection:
                print("Something is wrong with the database")
                connection.rollback()
                sys.exit(1)

        finally:
            if connection:
                connection.close()

    def store_recipe(self, recipe):
        try:
            # Establishing a connection
            connection = sqlite3.connect('brewdie.db')
            cursor = connection.cursor()
        
            # Querying, whether or not the recipe is already in the database
            recipe_names = []
            for row in cursor.execute('SELECT name FROM Recipes'):
                recipe_names.append(row[0])
            if recipe.name in recipe_names:
                print("Recipe is already stored in the database")
            else:
                # It is not, so we can insert it
                cursor.execute('INSERT INTO Recipes VALUES(?, ?, ?, ?, ?, ?)', 
                        (recipe.name, recipe.style, recipe.litres, 
                            recipe.sugar_gramms_per_litre,
                            recipe.boiling_minutes, recipe.correction_factor))
                for (malt_name, malt_gramms) in recipe.malts.items():
                    cursor.execute('INSERT INTO Malts(name, gramms, recipe_name) VALUES(?, ?, ?)', (malt_name, malt_gramms, recipe.name))

                index = 0
                for rest in recipe.rests:
                    cursor.execute('INSERT INTO Rests(name, degrees, minutes, position, recipe_name) VALUES(?, ?, ?, ?, ?)', (rest.name, rest.degrees, rest.minutes, index, recipe.name))
                    index = index + 1

                for hop_dosage in recipe.hop_dosages:
                    cursor.execute('INSERT INTO HopDosages(name, minutes, gramms, recipe_name) VALUES(?, ?, ?, ?)', (hop_dosage.name, hop_dosage.minutes, hop_dosage.gramms, recipe.name))

                for additional_ingredient in recipe.additional_ingredients:
                    cursor.execute('INSERT INTO AdditionalIngredients(name,'
                        'gramms, note, recipe_name) '
                        'VALUES(?, ?, ?, ?)',
                        (additional_ingredient.name,
                        additional_ingredient.gramms,
                        additional_ingredient.note,
                        recipe.name))

            connection.commit()
        except sqlite3.Error as e:
            print("Something went wrong")
            print(e)
            if connection:
                connection.rollback()
            return

        finally:
            if connection:
                connection.close()

    def store_brew(self, brew):
        try:
            # Establishing a connection
            connection = sqlite3.connect('brewdie.db',
                    detect_types = 
                    sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            cursor = connection.cursor()

            cursor.execute('INSERT INTO Brews '
                    '(datetime, recipe, note, gravity_initial, gravity_final) '
                    'VALUES(?, ?, ?, ?, ?)',
                    (brew.datetime, brew.recipe.name, brew.note,
                        brew.gravity_initial,
                        brew.gravity_final))
            connection.commit()
        except sqlite3.Error as e:
            print("Something went wrong")
            print(e)
            if connection:
                connection.rollback()
            return

        finally:
            if connection:
                connection.close()


    def row_to_recipe(self, row, cursor):
        # Converting a recipe database row into a python object
        loaded_recipe = Recipe(row[0], row[1], row[2], row[3], row[4], row[5])

        recipe_name = (loaded_recipe.name, )

        # Adding the malts
        for malt_row in cursor.execute('SELECT * FROM Malts WHERE recipe_name=?', recipe_name):
            loaded_recipe.add_malt(malt_row[1], malt_row[2])

        # Adding the rests
        for rest_row in cursor.execute('SELECT * FROM Rests WHERE recipe_name=? ORDER BY position ASC', recipe_name):
            loaded_recipe.add_rest(rest_row[1], rest_row[2], rest_row[3])

        # Adding the hop dosages
        for hop_dosage_row in cursor.execute('SELECT * FROM HopDosages WHERE recipe_name=?', recipe_name):
            loaded_recipe.add_hop_dosage(hop_dosage_row[1], hop_dosage_row[3], hop_dosage_row[2])

        # Adding the additional ingredients
        for row in cursor.execute('SELECT * FROM AdditionalIngredients WHERE '
                'recipe_name=?', recipe_name):
            loaded_recipe.add_additional_ingredient(row[1], row[2], row[3])
        
        return loaded_recipe

    def row_to_brew(self, row, brew):
        # Getting the matching recipe
        recipe = self.load_recipe(row[2])
        if not recipe:
            return None

        # Converting a brew database row into a python object
        loaded_brew = Brew(row[1], recipe, row[3], row[4], row[5])
        return loaded_brew

    def load_recipe(self, name):
        try:
            # Establishing a connection
            connection = sqlite3.connect('brewdie.db')
            cursor = connection.cursor()
        
            # Getting the recipe
            db_name = (name,)
            cursor.execute('SELECT * FROM Recipes WHERE name=?', db_name)
            row = cursor.fetchone()
            if (row):    
                loaded_recipe = self.row_to_recipe (row, cursor)
            else:
                print("Could not find recipe:",  name)
                loaded_recipe = None

        except sqlite3.Error as e:
            print("Something went wrong")
            print(e)
            if connection:
                connection.rollback()
            return

        finally:
            if connection:
                connection.close()
        return loaded_recipe
    
    def delete_recipe(self, name):
        try:
            # Establishing a connection
            connection = sqlite3.connect('brewdie.db')
            cursor = connection.cursor()
        
            # Deleting the recipe
            db_name = (name,)
            cursor.execute('DELETE FROM Recipes WHERE name=?', db_name)

            # Deleting malts, rests and hop dosages that were contained in the recipe
            cursor.execute('DELETE FROM Malts WHERE recipe_name=?', db_name)
            cursor.execute('DELETE FROM Rests WHERE recipe_name=?', db_name)
            cursor.execute('DELETE FROM HopDosages WHERE recipe_name=?', db_name)
            
            connection.commit()
        except sqlite3.Error as e:
            print("Something went wrong")
            print(e)
            if connection:
                connection.rollback()
            return

        finally:
            if connection:
                connection.close()
    
    
    def load_recipes(self):
        recipes = []
        try:
            # Establishing a connection
            connection = sqlite3.connect('brewdie.db')
            cursor = connection.cursor()
        
            # Getting all the recipes
            cursor.execute('SELECT * FROM Recipes')
            rows = cursor.fetchall()
            for row in rows:
                recipes.append(self.row_to_recipe(row, cursor))

        except sqlite3.Error as e:
            print("Something went wrong")
            print(e)
            if connection:
                connection.rollback()
            return

        finally:
            if connection:
                connection.close()
        return recipes

    def load_brews_by_recipe_name(self, recipe):
        brews = []
        try:
            # Establishing a connection
            connection = sqlite3.connect('brewdie.db',
                    detect_types = 
                    sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            cursor = connection.cursor()
            
            db_recipe = (recipe,)
            cursor.execute('SELECT * FROM Brews WHERE instr(recipe, ?) > 0',
                    db_recipe)
            rows = cursor.fetchall()
            for row in rows:
                brews.append(self.row_to_brew(row, cursor))

        except sqlite3.Error as e:
            print("Something went wrong")
            print(e)
            if connection:
                connection.rollback()
            return

        finally:
            if connection:
                connection.close()
        return brews

    def load_recipes_by_style(self, style):
        recipes = []
        try:
            # Establishing a connection
            connection = sqlite3.connect('brewdie.db')
            cursor = connection.cursor()
        
            # Getting all the recipes
            db_style = (style,)
            cursor.execute('SELECT * FROM Recipes WHERE instr(type, ?) > 0', db_style)
            rows = cursor.fetchall()
            for row in rows:
                recipes.append(self.row_to_recipe(row, cursor))

        except sqlite3.Error as e:
            print("Something went wrong")
            print(e)
            if connection:
                connection.rollback()
            return

        finally:
            if connection:
                connection.close()

        return recipes
    
    def load_recipes_by_name(self, name):
        recipes = []
        try:
            # Establishing a connection
            connection = sqlite3.connect('brewdie.db')
            cursor = connection.cursor()
        
            # Getting all the recipes
            db_name = (name,)
            cursor.execute('SELECT * FROM Recipes WHERE instr(name, ?) > 0',
                    db_name)
            rows = cursor.fetchall()
            for row in rows:
                recipes.append(self.row_to_recipe(row, cursor))

        except sqlite3.Error as e:
            print("Something went wrong")
            print(e)
            if connection:
                connection.rollback()
            return

        finally:
            if connection:
                connection.close()

        return recipes

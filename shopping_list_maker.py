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

from recipe import *
from shopping_list import *
from brewdiedb import *

class ShoppingListMaker:

    def __init__(self, brewdiedb):
        self.brewdiedb = brewdiedb

    def create_shopping_list(self):
        shoppingList = ShoppingList()
        valid_name = True
        while valid_name:
            name = input("Enter the name of the recipe: ")
            if name:
                valid_name = True
                recipe = self.brewdiedb.load_recipe(name)
                if recipe:
                    try:
                        litres = float(input("Enter the litres: "))
                        recipe = recipe.scale_to_litres(litres)
                        shoppingList.add_recipe(recipe)
                    except ValueError:
                        print("That was no valid input.")
                        print("Recipe is not added.")
                else:
                    print("Could not find recipe " + name)

            else:
                valid_name = False

        return shoppingList


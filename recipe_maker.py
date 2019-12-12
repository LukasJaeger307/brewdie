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
from brewdiedb import *

class RecipeMaker:

    def create_recipe(self):
        # Get general info on the recipe
        name = input("Enter the name of the recipe: ")
        if not name:
            return None
        style = input("Enter the style of the recipe: ")

        is_valid_input = False

        while not is_valid_input:
            try:
                boiling_minutes = int(input("Enter the number of boiling"
                    " minutes: "))
                is_valid_input = True
            except ValueError:
                print("This was no integer number. Please try again")
                is_valid_input = False

        is_valid_input = False

        while not is_valid_input:
            try:
                litres = float(input("Enter the number of litres: "))
                is_valid_input = True
            except ValueError:
                print("This was no floating point number. Please try again")
                is_valid_input = False

        recipe = Recipe(name, style, boiling_minutes, litres)

        # Add the malts
        is_valid_input = True
        while is_valid_input:
            malt_name = input("Enter a malt you wish to add to the recipe: ")
            if not malt_name:
                is_valid_input = False
            else:
                try:
                    malt_gramms = float(input("Enter the gramms of that malt: "))
                    recipe.add_malt(malt_name, malt_gramms)
                except ValueError:
                    print("This was no floating point number. The malt will not"
                    " be added.")
                finally:
                    is_valid_input = True
        
        # Add the rests
        is_valid_input = True
        while is_valid_input:
            rest = self.create_rest()
            if rest is None:
                is_valid_input = False
            else:
                recipe.rests.append(rest)
                is_valid_input = True

        # Add the hop dosages
        is_valid_input = True
        while is_valid_input:
            hop_dosage = self.create_hop_dosage()
            if hop_dosage is None:
                is_valid_input = False
            else:
                recipe.hop_dosages.append(hop_dosage)
                is_valid_input = True

        return recipe

    def create_rest(self):
        name = input("Enter the name of the rest you wish to add: ")
        if not name:
            return None
        is_valid_input = False
        degrees = 0.0
        while not is_valid_input:
            try:
                degrees = float(input("Enter the degrees of the rest: "))
                is_valid_input = True
            except ValueError:
                print("This was no floating point number. Please try again")
                is_valid_input = False
        
        minutes = 0
        is_valid_input = False
        while not is_valid_input:
            try:
                minutes = int(input("Enter the number of rest"
                    " minutes: "))
                is_valid_input = True
            except ValueError:
                print("This was no integer number. Please try again")
                is_valid_input = False
        
        return Rest(name, degrees, minutes)

    def create_hop_dosage(self):
        name = input("Enter the name of the hop you wish to add: ")
        if not name:
            return None
        
        is_valid_input = False
        gramms = 0.0
        while not is_valid_input:
            try:
                gramms = float(input("Enter the gramms of that hop: "))
                is_valid_input = True
            except ValueError:
                print("This was no floating point number. Please try again")
                is_valid_input = False
        
        minutes = 0
        is_valid_input = False
        while not is_valid_input:
            try:
                minutes = int(input("Enter the number of  minutes after which "
                    "the hop is added: "))
                is_valid_input = True
            except ValueError:
                print("This was no integer number. Please try again")
                is_valid_input = False
        
        return HopDosage(name, gramms, minutes)

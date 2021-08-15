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

class ShoppingList:

    def __init__(self):
        self.recipes = []
        self.reset()

    def reset(self):
        self.malts = {}
        self.hops = {}
        self.additional_ingredients = {}

    def compute(self):
        self.reset()
        for recipe in self.recipes:

            # Add malts
            for malt, weight in recipe.malts.items():
                if malt in self.malts:
                    self.malts[malt] += weight
                else:
                    self.malts[malt] = weight

            # Add hops
            for hop in recipe.hop_dosages:
                hop_name = hop.name
                hop_gramms = hop.gramms
                if hop_name in self.hops:
                    self.hops[hop_name] += hop_gramms
                else:
                    self.hops[hop_name] = hop_gramms

            # Add additional ingredients
            for ingredient in recipe.additional_ingredients:
                name = ingredient.name
                gramms = ingredient.gramms
                if name in self.additional_ingredients:
                    self.additional_ingredients[name] += gramms
                else:
                    self.additional_ingredients[name] = gramms

    def add_recipe(self, recipe):
        self.recipes.append(recipe)
        self.compute()

    def add_recipes(self, recipes):
        self.recipes.extend(recipes)
        self.compute()

    def print(self):
        print("Shopping list")
        
        print("---- Malts:")
        for malt, weight in self.malts.items():
            print(malt + ": " + str(round(weight, 2)))

        print("---- Hops:")
        for hop, weight in self.hops.items():
            print(hop + ": " + str(round(weight, 2)))

        print("---- Additional Ingredients:")
        for ingredient, weight in self.additional_ingredients.items():
            print(ingredient + ": " + str(round(weight, 2)))

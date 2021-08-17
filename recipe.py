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

class HopDosage:
    # TODO: Test
    def __init__(self, name, gramms, minutes, id=0):
        self.name = name
        self.gramms = gramms
        self.minutes = minutes
        self.id = id

class Rest:
    # TODO: Test
    def __init__(self, name, degrees, minutes, id=0):
        self.name = name
        self.degrees = degrees
        self.minutes = minutes
        self.id = id

class AdditionalIngredient:
    # TODO: Test
    def __init__(self, name, gramms, note, id=0):
        self.name = name
        self.gramms = gramms
        self.note = note
        self.id = id

class Recipe:
    def __init__(self, name, style, litres, sugar_gramms_per_litre,
            boiling_minutes=60, correction_factor = 1.0):
        self.name = name
        self.style = style
        self.rests = rests = []
        self.malts = {}
        self.boiling_minutes = boiling_minutes
        self.hop_dosages = []
        self.litres = litres
        self.sugar_gramms_per_litre = sugar_gramms_per_litre
        self.correction_factor = correction_factor
        self.additional_ingredients = []

    # TODO: Test
    def __eq__(self, other):
        return self.name == other.name

    def add_malt(self, name, gramms):
        self.malts[name] = gramms

    # TODO: Test
    def remove_malt(self, name):
        del(self.malts[name])

    def add_rest(self, name, degrees, minutes):
        self.rests.append(Rest(name, degrees, minutes))

    def add_hop_dosage(self, name, gramms, minutes):
        self.hop_dosages.append(HopDosage(name, gramms, minutes))

    # TODO: Test
    def add_additional_ingredient(self, name, gramms, note):
        #self.additional_ingredients.append(AdditionalIngredient(name, gramms, note))
        return

    def get_hop_dosages(self):
        return self.hop_dosages

    # TODO: Test
    def scale_to_litres(self, scaled_litres):
        scaling_factor = scaled_litres / self.litres
        scaled_recipe = Recipe(self.name, self.style, scaled_litres,
                self.sugar_gramms_per_litre, self.boiling_minutes, 
                self.correction_factor)
        
        # Scale the malts
        for malt, weight in self.malts.items():
            scaled_recipe.add_malt(malt, weight * scaling_factor)

        scaled_recipe.rests = self.rests.copy()

        # Scale the hops
        for hop_dosage in self.hop_dosages:
            scaled_recipe.add_hop_dosage(hop_dosage.name, hop_dosage.gramms *
                    scaling_factor, hop_dosage.minutes)

        # Scale the additional ingredients
        for additional_ingredient in self.additional_ingredients:
            scaled_recipe.add_additional_ingredient(additional_ingredient.name,
                    additional_ingredient.gramms * scaling_factor,
                    additional_ingredient.note)

        return scaled_recipe

    # TODO: Test
    def get_sugar_for_carbonation(self):
        return self.litres * self.sugar_gramms_per_litre

    # TODO: Test
    def get_percentage_of_malt(self, malt_name):
        if not malt_name in self.malts:
            return 0.0

        # Compute the total weight of the malts
        total_weight = 0.0
        for malt, weight in self.malts.items():
            total_weight += weight
        return 100.0 * self.malts[malt_name] / total_weight
        
    # TODO: Test
    def print(self):
        print("---- Recipe information")
        print("Name:           ", self.name)
        print("Style:          ", self.style)
        print("Boiling minutes:", round(self.boiling_minutes,2))
        print("Litres:         ", round(self.litres, 2))
        print("Sugar (g/l)     ", round(self.sugar_gramms_per_litre, 2))
        print("Sugar (total)   ", round(self.get_sugar_for_carbonation(), 2))
        print("Malts:")
        maltweight = 0.0
        for malt, weight in self.malts.items():
            maltweight += weight
            print("    " + malt + " : " + str(round(weight * self.correction_factor, 2)) +
                    " (" + str(round(self.get_percentage_of_malt(malt), 2)) + "%)")

        print("    Total malt weight: " + str(round(maltweight,2)))
        print("Rests:")
        for rest in self.rests:
            print("    ", rest.name, ":", rest.degrees, "°C for", rest.minutes,
                    "minutes")

        print("Hop dosages:")
        for hop_dosage in self.hop_dosages:
            print("    ", hop_dosage.name, ":", round(hop_dosage.gramms *
                self.correction_factor, 2),
                    "gramms after", hop_dosage.minutes, "minutes")

        if self.additional_ingredients :
            print("Additional ingredients:")
            for additional_ingredient in self.additional_ingredients:
                print("    ", additional_ingredient.name, ":",
                        round(additional_ingredient.gramms *
                            self.correction_factor, 2), "gramms")
                print("        ", additional_ingredient.note)

        print("----")

    # TODO: Test
    def get_shopping_list(self):
        shopping_list = {}

        # Add malts
        for malt in self.malts:
            if malt in shopping_list:
                shopping_list[malt] += self.malts[malt]
            else:
                shopping_list[malt] = self.malts[malt]

        # Add hops
        for hop_dosage in self.hop_dosages:
            if hop_dosage.name in shopping_list:
                shopping_list[hop_dosage.name] += hop_dosage.gramms
            else:
                shopping_list[hop_dosage.name] = hop_dosage.gramms

        # Add additional ingredients
        for additional_ingredients in self.additional_ingredients:
            if additional_ingredient.name in shopping_list:
                shopping_list[additional_ingredient.name] += \
                additional_ingredient.gramms
            else:
                shopping_list[additional_ingredient.name] = \
                additional_ingredient.gramms

        return shopping_list

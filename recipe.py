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
    def __init__(self, name, gramms, minutes):
        self.name = name
        self.gramms = gramms
        self.minutes = minutes

class Rest:
    def __init__(self, name, degrees, minutes):
        self.name = name
        self.degrees = degrees
        self.minutes = minutes

class Recipe:
    def __init__(self, name, style, litres, boiling_minutes=60, correction_factor = 1.0):
        self.name = name
        self.style = style
        self.rests = rests = []
        self.malts = {}
        self.boiling_minutes = boiling_minutes
        self.hop_dosages = []
        self.litres = litres
        self.correction_factor = correction_factor

    def add_malt(self, name, gramms):
        self.malts[name] = gramms

    def remove_malt(self, name):
        del(self.malts[name])

    def add_rest(self, name, degrees, minutes):
        self.rests.append(Rest(name, degrees, minutes))

    def add_hop_dosage(self, name, gramms, minutes):
        self.hop_dosages.append(HopDosage(name, gramms, minutes))

    def scale_to_litres(self, scaled_litres):
        scaling_factor = scaled_litres / self.litres
        scaled_recipe = Recipe(self.name, self.style, scaled_litres,
                self.boiling_minutes, self.correction_factor)
        
        # Scale the malts
        for malt, weight in self.malts.items():
            scaled_recipe.add_malt(malt, weight * scaling_factor)

        scaled_recipe.rests = self.rests.copy()

        # Scale the hops
        for hop_dosage in self.hop_dosages:
            scaled_recipe.add_hop_dosage(hop_dosage.name, hop_dosage.gramms *
                    scaling_factor, hop_dosage.minutes)

        return scaled_recipe


    def print(self):
        print("---- Recipe information")
        print("Name:           ", self.name)
        print("Style:          ", self.style)
        print("Boiling minutes:", round(self.boiling_minutes,2))
        print("Litres:         ", round(self.litres, 2))
        print("Malts:")
        for malt, weight in self.malts.items():
            print("    ", malt, ":", round(weight * self.correction_factor, 2))

        print("Rests:")
        for rest in self.rests:
            print("    ", rest.name, ":", rest.degrees, "°C for", rest.minutes,
                    "minutes")

        print("Hop dosages:")
        for hop_dosage in self.hop_dosages:
            print("    ", hop_dosage.name, ":", round(hop_dosage.gramms *
                self.correction_factor, 2),
                    "gramms after", hop_dosage.minutes, "minutes")

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

        return shopping_list

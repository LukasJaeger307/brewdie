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

import datetime
from recipe import *

class Brew:
    def __init__ (self, datetime, recipe, note, gravity_initial = 0.0,
            gravity_final = 0.0):
        self.datetime = datetime
        self.recipe = recipe
        self.note = note
        self.gravity_initial = gravity_initial
        self.gravity_final = gravity_final

    def get_weight_percentage(self):
        return (self.gravity_initial - self.gravity_final) * 105

    def get_volume_percentage(self):
        return self.get_weight_percentage() * 1.25

    def print(self):
        print("---- Brew information")
        print("Time:           ", self.datetime)
        print("Recipe name:    ", self.recipe.name)
        print("Note:           ", self.note)
        print("Initial gravity:", self.gravity_initial)
        print("Final gravity:  ", self.gravity_final)
        print("Alcohol content:", round(self.get_volume_percentage(), 2))
        print("----")


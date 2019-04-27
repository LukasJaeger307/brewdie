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
    def __init__ (self, datetime, recipe, note):
        self.datetime = datetime
        self.recipe = recipe
        self.note = note
        self.density_initial = 0
        self.density_final = 0

    def get_weight_percentage(self):
        return (self.density_initial - self.density_final) * 105

    def get_volume_percentage(self):
        return self.get_weight_percentage() * 1.25


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
    def __init__(self, name, style):
        self.name = name
        self.style = style



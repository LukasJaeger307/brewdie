import unittest

from recipe import *

class TestSum(unittest.TestCase):

    def create_example_recipe(self):
        return Recipe("North Star", "American Pale Ale", 4.7, 7.4, 90)
    
    def setup_example_recipe(self):
        recipe = self.create_example_recipe()
        
        recipe.add_malt("Pale Malt", 961.00)
        recipe.add_malt("Carapils", 48.00)
        
        recipe.add_rest("Main rest", 67.0, 60)

        recipe.add_hop_dosage("Cascade", 9.00, 30)
        recipe.add_hop_dosage("Cascade", 4.00, 75)
        recipe.add_hop_dosage("Cascade", 4.00, 85)
        recipe.add_hop_dosage("Cascade", 9.00, 90)

        recipe.add_additional_ingredient("Fairy dust", 5.00, "Add at flame-out")

        return recipe

    def is_example_recipe(self, recipe):
        result = (recipe.name == "North Star")
        result = result and (recipe.style == "American Pale Ale")
        result = result and (recipe.boiling_minutes == 90)
        result = result and (recipe.litres == 4.7)
        result = result and (recipe.sugar_gramms_per_litre == 7.4)
        return result

    def is_initialized_example_recipe(self, recipe):
        result = self.is_example_recipe(recipe)
        result = result and (len(recipe.rests) == 0)
        result = result and (len(recipe.malts) == 0)
        result = result and (len(recipe.get_hop_dosages()) == 0)
        result = result and (len(recipe.additional_ingredients) == 0)
        return result

    def test_recipe_constructor(self):
        recipe = self.create_example_recipe()
        self.assertTrue(self.is_initialized_example_recipe(recipe))

    def check_hop_dosage(self, hop_dosage, name, gramms, minutes):
        return (hop_dosage.name == name) and (hop_dosage.gramms == gramms) and (hop_dosage.minutes == minutes)

    def check_setup_hop_dosages(self, hop_dosages):
        result = len(hop_dosages) == 4
        result = result and self.check_hop_dosage(hop_dosages[0], "Cascade", 9.00, 30)
        result = result and self.check_hop_dosage(hop_dosages[1], "Cascade", 4.00, 75)
        result = result and self.check_hop_dosage(hop_dosages[2], "Cascade", 4.00, 85)
        result = result and self.check_hop_dosage(hop_dosages[3], "Cascade", 9.00, 90)
        return result

    def is_setup_recipe(self, recipe):
        result = self.is_example_recipe(recipe)
        result = result and (len(recipe.rests) == 1)
        if (result):
            main_rest = recipe.rests[0]
            result = result and (main_rest.name == "Main rest")
            result = result and (main_rest.degrees == 67.0)
            result = result and (main_rest.minutes == 60)
        result = result and (len(recipe.malts) == 2)
        if (result):
            result = result and (recipe.malts["Pale Malt"] == 961.00)
            result = result and (recipe.malts["Carapils"] == 48.00)
        result = self.check_setup_hop_dosages(recipe.get_hop_dosages())
        #result = result and (len(recipe.additional_ingredients) == 1)
        
        return result

    def test_recipe_add_methods(self):
        recipe = self.setup_example_recipe()
        self.assertTrue(self.is_setup_recipe(recipe))

if __name__ == '__main__':
    unittest.main()
                                            

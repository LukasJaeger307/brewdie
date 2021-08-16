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

        return recipe

    def is_example_recipe(self, recipe):
        result = (recipe.name == "North Star")
        result = result and (recipe.style == "American Pale Ale")
        result = result and (len(recipe.rests) == 0)
        result = result and (len(recipe.malts) == 0)
        result = result and (recipe.boiling_minutes == 90)
        result = result and (len(recipe.hop_dosages) == 0)
        result = result and (recipe.litres == 4.7)
        result = result and (recipe.sugar_gramms_per_litre == 7.4)
        result = result and (len(recipe.additional_ingredients) == 0)
        return result


    def test_recipe_constructor(self):
        recipe = self.create_example_recipe()
        self.assertTrue(self.is_example_recipe(recipe))
        #self.assertEqual(recipe.name, "North Star")
        #self.assertEqual(recipe.style, "American Pale Ale")
        #self.assertEqual(len(recipe.rests), 0)
        #self.assertEqual(len(recipe.malts), 0)
        #self.assertEqual(recipe.boiling_minutes, 90)
        #self.assertEqual(len(recipe.hop_dosages), 0)
        #self.assertEqual(recipe.litres, 4.7)
        #self.assertEqual(recipe.sugar_gramms_per_litre, 7.4)
        #self.assertEqual(len(recipe.additional_ingredients), 0)
        

if __name__ == '__main__':
    unittest.main()
                                            

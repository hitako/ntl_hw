class CookBook:
    def __init__(self, file_path):
        self.cook_book = {}
        self.file_path = file_path
        self.recipes = []

    def add_recipes_in_cook_book(self):
        if self.recipes:
            for recipe in self.recipes:
                dish = recipe.split('\n')
                dish_name = dish.pop(0)
                self.cook_book[dish_name] = []
                dish.pop(0)
                self.__add_dish_in_cook_book(dish_name, dish)

    def set_recipes_from_file(self):
        with open(self.file_path, "r", encoding="utf-8") as book:
            self.recipes = book.read().split("\n\n")

    def __add_dish_in_cook_book(self, dish_name, dish_composition):
        for ingredient in dish_composition:
            ingredient_parse = ingredient.split("|")
            self.cook_book[dish_name].append(
                {'ingredient_name': ingredient_parse[0], 'quantity': ingredient_parse[1],
                 'measure': ingredient_parse[2]})

    def get_shop_list_by_dishes(self, dishes, person_count):
        shop_list = dict()
        for dish in dishes:
            for cook in self.cook_book[dish]:
                if shop_list.get(cook['ingredient_name']) is None:
                    shop_list[cook['ingredient_name']] = {
                        'measure': cook['measure'], 'quantity': int(cook['quantity']) * person_count
                    }
                else:
                    shop_list[cook['ingredient_name']]['quantity'] *= person_count

        return shop_list


cook_book = CookBook("book.txt")
cook_book.set_recipes_from_file()
cook_book.add_recipes_in_cook_book()
# print(cook_book.cook_book)

print(cook_book.get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))

import recipe_classes
import parser
import transform

def main():
    """This function runs the user interface, prompting the user and calling the necessary functions to resolve their queries"""

    print "Hello, welcome to the recipe transformer!"
    print "To get started, please enter the URL of the recipe you would like to transform. At any point, you may enter \"back\" to return to the previous menu."
    print "You may also enter \"done\" at any point to terminate the program."
    menu = 0
    prompt = ["Enter AllRecipes.com URL:  ", "Enter transformation (enter \"list\" for a list of posible transformations):  ", "Would you like to apply another transformation to this new recipe?  "]
    URL = ""
    again = False

    transformations = ['pescatarian', 'vegetarian', 'east asian', 'italian', 'easy', 'low sodium', 'low carb']


    print "Hello world"

    while(True):
        command = raw_input(prompt[menu]).lower()
        if command == "done":
            return
        if command == "back":
            menu -= 1
            if menu < 0:
                menu = 0
            continue
        if menu == 0:
            if command[:29] == "http://allrecipes.com/recipe/":
                URL = command
                menu += 1
                continue
            print "Invalid URL"
        if menu == 1:
            if command == "list":
                print ", ".join(transformations)
                continue
            if command in transformations:
                if again:
                    print transformed_recipe
                    transformed_recipe[1].transformation = command
                    transformed_recipe = parser.main(transformed_recipe[1])
                else:
                    recipe = recipe_classes.Recipe(URL, "recipe", command)
                    transformed_recipe = parser.main(recipe)

                print transformed_recipe
                menu += 1
                continue
            print "Invalid transformation"
        if menu == 2:
            if command == "yes":
                again = True
                menu = 1
                continue
            if command == "no":
                again = False
                menu = 0
                continue
            print "Invalid response"


if __name__ == '__main__':
    main()
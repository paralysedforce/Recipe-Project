import recipe_classes
import parser
import transform

def main():
    """This function runs the user interface, prompting the user and calling the necessary functions to resolve their queries"""

    print "Hello, welcome to the recipe transformer!"
    print "To get started, please enter the URL of the recipe you would like to transform. At any point, you may enter \"back\" to return to the previous menu."
    print "You may also enter \"done\" at any point to terminate the program."
    menu = 0
    prompt = ["Enter AllRecipes.com URL:  ", "Enter transformation (enter \"list\" for a list of posible transformations):  ", ]
    URL = ""

    transformations = ['pescetarian', 'vegetarian', 'east asian', 'italian', 'easy', 'low sodium', 'low carb']


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
        if menu >= 1:
            if command == "list":
                print ", ".join(transformations)
                continue
            if command in transformations:
                recipe = recipe_classes.Recipe(URL, "recipe", command)
                transformed_recipe = parser.main(recipe)
                print transformed_recipe
                continue
            print "Invalid transformation"


if __name__ == '__main__':
    main()
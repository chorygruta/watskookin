from flask import request, render_template, redirect,url_for, request
from flask_wtf import FlaskForm
from difflib import SequenceMatcher
from app import app
from models import *
from forms import *

######################################################################################################################################################################################
# calculates the similarity ratio of 2 strings returns a ratio number
#@app.route('/test')
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


#@app.route('/catalog/<category>', defaults={'results':''}, methods = ['POST','GET'])
@app.route('/catalog/<category>',methods = ['POST','GET'])
def getCategoryResults(category):

    if request.method != 'POST':
        return render_template('category_results.html', form=form)


#returns a Recipe object
def recipeDetails(recipiID):
    x = Ingredient.query.join(Ingredient.recipes).filter_by(id=recipiID).all()
    r = Recipe.query.get(recipeID)
    return x

#returns a list of categories and returns a list of results for a specifc category
@app.route('/catalog', defaults= {'category':''}, methods = ['POST','GET'])
@app.route('/catalog/<string:category>', methods = ['POST','GET'])
def catalog(category):
    form = CategoryForm()

    if form.validate_on_submit():
        return redirect(url_for('catalog', category = form.category.data))

    if request.method != 'POST' and category == '':
        return render_template('categories.html', form=form)
    else:
        if category == 'cuisines':
            categoryResultsForm = CuisineCategoryForm()
        elif category == 'dish-types':
            category = 'Dish Type'
            categoryResultsForm = DishTypeCategoryForm()
        else:
            categoryResultsForm = DietCategoryForm()

        return render_template('category_results.html', category = category, form=categoryResultsForm)

class searchRecipe(object):
    recipe = Recipe
    missedIngredient = 0
    usedIngredient = 0



######################################################################################################################################################################################
#parses input ingredients and returns a list of recipes
def parseIngredients(ingredientList):

    likeIngredientList = ["%" + i + "%" for i in ingredientList]
    finalIngredientList = []

    counter = 0
    for i in likeIngredientList:
        similarIngredients = Ingredient.query.filter(Ingredient.name.like(i)).all()

        for sis in similarIngredients:
            si = sis.name
            #return str(si) + " " + str(ingredientList[counter]) + " " + str(similar(si, ingredientList[counter]))
            if similar(si, ingredientList[counter]) >= 0.90:
                finalIngredientList.append(si)
                print('90 ' + si )

            elif len(si.split(" ")) == 1:
                if similar(si,ingredientList[counter]) >= 0.80:
                    finalIngredientList.append(si)
                    print('80 ' + si )

            elif len(si.split(" ")) == 2:
                parsedString = si.split(" ")
                if similar(parsedString[0], ingredientList[counter]) >= 0.80:
                    finalIngredientList.append(si)
                    print('80 2 words ' + si )
                elif similar(parsedString[1], ingredientList[counter]) >= 0.80:
                    finalIngredientList.append(si)
                    print('80 2 words ' + si )
                else:
                    pass
            else:
                pass
        counter += 1

    return finalIngredientList

@app.route('/results', methods=['POST'])
@login_required
def results():

    #initializes input with the input values from the form ingredients
    inputIngredients = request.form['ingredients'].lower()
    ingredientList = inputIngredients.replace(", ",",").split(",")
    tempList = []

    for i in ingredientList:
        if i.endswith('es'):
            tempList.append(i[:-2])
        elif i.endswith('s'):
            tempList.append(i[:-1])
        else:
            tempList.append(i)

    ingredientList = tempList
    inputIngredients = ingredientList

    ingredientList = parseIngredients(ingredientList)

    recipes = Recipe.query.filter(Recipe.ingredients.any(Ingredient.name.in_(ingredientList))).all()

    rankedRecipesList = []

    for r in recipes:
        recipeIngredientList = []
        matchedCounter = 0
        missedCounter = 0

        for i in Ingredient.query.filter(Ingredient.recipes.any(id = r.id)):
            recipeIngredientList.append(i.name)
            #print (i.name)

        for input in inputIngredients:
            ifAdded = True
            for ing in recipeIngredientList:
                if ifAdded == True:
                    if similar(input, ing) >= 0.80:
                        matchedCounter += 1
                        ifAdded = False

                    elif len(ing.split(" ")) == 2:
                        parsedString = ing.split(" ")
                        if similar(parsedString[0], input) >= 0.80:
                            matchedCounter +=1
                            ifAdded = False

                        elif similar(parsedString[1], input) >= 0.80:
                            matchedCounter +=1
                            ifAdded = False

                        else:
                            pass
                    else:
                        pass
        missedCounter = len(recipeIngredientList) - matchedCounter
        rankedRecipesObj = (r, matchedCounter, missedCounter)
        rankedRecipesList.append(rankedRecipesObj)

    rankedRecipesList.sort(reverse=True, key=lambda tup: tup[1])

    temp = []
    for i in range(0, len(rankedRecipesList)):
        temp.append(rankedRecipesList[i][0])
    recipes = temp

    return render_template('results.html', recipes = recipes, inputIngredients=inputIngredients)

@app.route('/recipeDetails', methods=['POST'])
@login_required
def recipeDetails():

    searchID = id = request.form['recipeID']

    x = Ingredient.query.join(Ingredient.recipes).filter_by(id=searchID).all()
    r = Recipe.query.get(searchID)

    return render_template('recipeDetail.html', ingredient=x, recipe=r )

@app.route('/search')
@login_required
def search():
    return render_template('search.html')

@app.route('/search/by-ingredients-search')
@login_required
def byIngredientSearch():
    return render_template('byIngredientsSearch.html')

@app.route('/')
def index():
    return render_template('home.html')

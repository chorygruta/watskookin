from flask import request, render_template, redirect,url_for, request, jsonify
from flask_wtf import FlaskForm
from flask_user import current_user
from difflib import SequenceMatcher
from app import app
from models import *
from forms import *
import simplejson as json

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

def addIngredientToUserFunction(userObj, ingredientObj):
    userObj.savedIngredients.append(ingredientObj)
    db.session.commit()

def saveRecipeFunction(userObj, recipeObj):
    userObj.savedRecipes.append(recipeObj)
    db.session.commit()

@app.route('/addIngredient', methods=['GET', 'POST'])
@login_required
def addIngredient():
    user_id = current_user.get_id()
    form = getIngredientForm()

    if form.validate_on_submit():
        ingredientObj = Ingredient.query.filter_by(name=form.name.data).first()
        currentUserObj = User.query.filter_by(id=current_user.get_id()).first()
        addIngredientToUserFunction(currentUserObj, ingredientObj)
        return '<h1>The name of the ingredient is {}.'.format(form.name.data)

    return render_template('addIngredient.html', form=form)

@app.route('/pantry', methods=['GET', 'POST'])
def pantry():
    user_id = current_user.get_id()

    userobj = User.query.filter(User.id == user_id).first()
    x = userobj.savedIngredients

    ingredients = ""
    for i in x:
        ingredients += i.name + ' ' + str(i.id) + ' ' + i.imageUrl
    return ingredients

@app.route('/saveRecipe', methods=['GET', 'POST'])
@login_required
def saveRecipeProcess():
    #get the recipe ID
    recipe_id = request.args.get('recipe', 0, type=str)

    recipeObj = Recipe.query.filter(Recipe.id == recipe_id).first()
    userObj = User.query.filter(User.id == current_user.get_id()).first()

    if recipeObj in userObj.savedRecipes:
        print('Unsaving this recipe!')
        userObj.savedRecipes.remove(recipeObj)
        db.session.commit()
        return jsonify(isSaved=False)
    else:
        print('saving this recipe!')
        saveRecipeFunction(userObj, recipeObj)
        return jsonify(isSaved=True)

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


@app.route('/results', methods=['GET', 'POST'])
@app.route('/results/<int:page>', methods=['GET', 'POST'])
@login_required
def results():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)


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
    recipes = rankedRecipesList

    return render_template('results.html', recipes = recipes, inputIngredients=inputIngredients, pagination=pagination)

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
    ingredients = Ingredient.query.all()
    return render_template('search.html', ingredients = ingredients)

@app.route('/processSearch')
def processSearch():
    a = request.args.get('a', 0, type=str)
    b = request.args.get('b', 0, type=str)

    excludedIngredients = b.lower()
    excludedIngredientList = excludedIngredients.replace(", ",",").split(",")
    excludedTempList = []

    for i in excludedIngredientList:
        if i.endswith('es'):
            excludedTempList.append(i[:-2])
        elif i.endswith('s'):
            excludedTempList.append(i[:-1])
        else:
            excludedTempList.append(i)

    excludedIngredientList = excludedTempList
    excludedIngredientList = parseIngredients(excludedIngredientList)
    excludedRecipes = Recipe.query.filter(Recipe.ingredients.any(Ingredient.name.in_(excludedIngredientList))).all()

    inputIngredients = a.lower()
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

    tempRecipes = []


    for i in recipes:
        if i in excludedRecipes:
            print('remove ' + i.title)
            pass
        else:
            tempRecipes.append(i)

    recipes = tempRecipes

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
    recipes = rankedRecipesList


    #result = json.dumps(r.__dict__)
    return jsonify(temp)
    # jsonify(result=ingredientList, recipes=result)


@app.route('/search/by-ingredients-search')
@login_required
def byIngredientSearch():
    return render_template('byIngredientsSearch.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

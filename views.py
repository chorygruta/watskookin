from flask import request, render_template, redirect,url_for, request
from flask_wtf import FlaskForm
from app import app
from models import *
from forms import *

######################################################################################################################################################################################
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

@app.route('/results', methods=['POST'])
@login_required
def results():

    #initializes input with the input values from the form ingredients
    inputIngredients = request.form['ingredients']
    #puts the input ingredients into a list
    ingredient_list = inputIngredients.replace(", ",",").split(",")
    like_list = ["%" + i + "%" for i in ingredient_list]
    #searches for recipes that has the ingredients in ingredient_list and puts it inside recipes
    recipes = Recipe.query.filter(Recipe.ingredients.any(Ingredient.name.in_(ingredient_list))).all()

    maximizedUsedRecipes = []
    minimizedMissedRecipes = []
    search_list = []

    for i in range(len(ingredient_list), 0, -1):
        print('For match ' + str(i))
        for r in recipes:
            usedIngredient = 0
            for ing in r.ingredients:
                for s in ingredient_list:
                    if s == ing.name:
                        usedIngredient += 1
            missedIngredient = len(r.ingredients) - usedIngredient

            sr = searchRecipe()
            sr.recipe = r
            sr.missedIngredient = missedIngredient
            sr.usedIngredient = usedIngredient
            search_list.append(sr)
            '''
            if usedIngredient == i:
                if r in maximizedUsedRecipes:
                    pass
                else:
                    maximizedUsedRecipes.append(r)
                    print (r.title + '  used: ' +  str(usedIngredient) + ' missed: ' + str(missedIngredient) + ' total: ' + str(len(r.ingredients)))

            '''
    for index in range(0 , len(ingredient_list)):
        for i in search_list:
            if i.missedIngredient == index:
                if i.recipe not in minimizedMissedRecipes:
                    minimizedMissedRecipes.append(i.recipe)
            if i.usedIngredient == (len(ingredient_list)-index):
                if i.recipe not in maximizedUsedRecipes:
                    maximizedUsedRecipes.append(i.recipe)




    #if no recipes found, return message
    if len(recipes) == 0:
        return '<h1>Ingredients do not exist in the database. <br> Please try again. </h1>'

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
    return render_template('index.html')

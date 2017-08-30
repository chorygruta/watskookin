from flask_wtf import FlaskForm
from wtforms import TextField, StringField,RadioField
from models import *

class saveRecipeForm(FlaskForm):
    name = StringField('name')
    
class getIngredientForm(FlaskForm):
    name = StringField('name')

class addIngredientForm(FlaskForm):
    name = StringField('name')


class CategoryForm(FlaskForm):
    category = RadioField('Categories', choices=[('cuisines','Cuisine'),('dish-types','Dish Type'),('diets', 'Diet')])

class CuisineCategoryForm(FlaskForm):
    categoryResults = []

    for i in Cuisine.query.all():
        x = (i.name, i.name)
        categoryResults.append(x)

    results = RadioField('CategoryResults', choices = categoryResults)

class DishTypeCategoryForm(FlaskForm):
    categoryResults = []

    for i in DishType.query.all():
        x = (i.name, i.name)
        categoryResults.append(x)

    results = RadioField('CategoryResults', choices = categoryResults)

class DietCategoryForm(FlaskForm):
    categoryResults = []

    for i in Diet.query.all():
        x = (i.name, i.name)
        categoryResults.append(x)

    results = RadioField('CategoryResults', choices = categoryResults)

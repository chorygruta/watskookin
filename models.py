from app import app, db, admin, ma
from flask_admin.contrib.sqla import ModelView
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, ForeignKey, exists, or_
from flask.json import JSONEncoder



ingredients = db.Table('ingredients',
        db.Column('recipe_id', db.Integer,db.ForeignKey('recipe.id'), primary_key=True),
        db.Column('ingredient_id',db.Integer,db.ForeignKey('ingredient.id'), primary_key=True)
)

savedIngredients = db.Table('myIngredients',
        db.Column('user_id', db.Integer,db.ForeignKey('user.id'), primary_key=True),
        db.Column('ingredient_id',db.Integer,db.ForeignKey('ingredient.id'), primary_key=True)
)

savedRecipes = db.Table('savedRecipes',
        db.Column('user_id', db.Integer,db.ForeignKey('user.id'), primary_key=True),
        db.Column('recipe_id',db.Integer,db.ForeignKey('recipe.id'), primary_key=True)
)

cuisines = db.Table('cuisines',
        db.Column('recipe_id', db.Integer,db.ForeignKey('recipe.id'), primary_key=True),
        db.Column('cuisine_id',db.Integer,db.ForeignKey('cuisine.id'), primary_key=True)
)

dishtypes = db.Table('dishtypes',
        db.Column('recipe_id', db.Integer,db.ForeignKey('recipe.id'), primary_key=True),
        db.Column('dishtype_id',db.Integer,db.ForeignKey('dishtype.id'), primary_key=True)
)

diets = db.Table('diets',
        db.Column('recipe_id', db.Integer,db.ForeignKey('recipe.id'), primary_key=True),
        db.Column('diet_id',db.Integer,db.ForeignKey('diet.id'), primary_key=True)
)

equipments = db.Table('equipments',
        db.Column('recipe_id', db.Integer,db.ForeignKey('recipe.id'), primary_key=True),
        db.Column('equipment_id',db.Integer,db.ForeignKey('equipment.id'), primary_key=True)
)

class Recipe(db.Model):

    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    imageUrl = db.Column(db.String, nullable=False)


    #def __init__(self, **kwargs):
    #    super(Recipe, self).__init__(**kwargs)

    def __init__(self, id, title, imageUrl):
            self.id = id
            self.title = title
            self.imageUrl = imageUrl

    #One-to-One relationship between Recipe and Detail
    detail = relationship("Detail", uselist=False, back_populates="recipe")
    #One-to-One relationship between Recipe and NutritionFact
    nutritionfact = relationship("NutritionFact", uselist=False, back_populates="recipe")
    #One-to-Many relationship between Recipe and SimilarRecipe
    similarrecipes = db.relationship('SimilarRecipe', backref="recipe", cascade="all, delete-orphan" , lazy='dynamic')
    #One-to-Many relationship between Recipe and Instructions
    instructions = db.relationship('Instruction', backref="recipe", cascade="all, delete-orphan" , lazy='dynamic')
    #Many-to-Many relationship between Recipe and Ingredient
    ingredients = db.relationship('Ingredient', secondary=ingredients, lazy='subquery', backref=db.backref('recipes',lazy=True))
    #Many-to-Many relationship between Recipe and Cuisine
    cuisines = db.relationship('Cuisine', secondary=cuisines, lazy='subquery', backref=db.backref('recipes',lazy=True))
    #Many-to-Many relationship between Recipe and DishType
    dishtypes = db.relationship('DishType', secondary=dishtypes, lazy='subquery', backref=db.backref('recipes',lazy=True))
    #Many-to-Many relationship between Recipe and Diet
    diets = db.relationship('Diet', secondary=diets, lazy='subquery', backref=db.backref('recipes',lazy=True))
    #Many-to-Many relationship between Recipe and Equipment
    equipments = db.relationship('Equipment', secondary=equipments, lazy='subquery', backref=db.backref('recipes',lazy=True))

class RecipeJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Recipe):
            return {
                   'id'         : obj.id,
                   'title'      : obj.title,
                   'imageUrl'   : obj.imageUrl
            }
        return super(RecipeJSONEncoder, self).default(obj)

class Detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipeSourceName = db.Column(db.String, nullable=False)
    recipeSourceUrl = db.Column(db.String, nullable=False)
    readyInMinutes = db.Column(db.Integer, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    pricePerServing = db.Column(db.Integer, nullable=False)
    saveCount = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = relationship("Recipe", back_populates="detail")


class Cuisine(db.Model):
    __tablename__ = 'cuisine'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class DishType(db.Model):
    __tablename__ = 'dishtype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Diet(db.Model):
    __tablename__ = 'diet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    imageUrl = db.Column(db.String, nullable=False)

class NutritionFact(db.Model):
    __tablename__ = 'nutritionfact'
    id = db.Column(db.Integer, primary_key=True)
    vegetarian = db.Column(db.Boolean, nullable=False)
    vegan = db.Column(db.Boolean, nullable=False)
    glutenFree = db.Column(db.Boolean, nullable=False)
    dairyFree = db.Column(db.Boolean, nullable=False)
    calories = db.Column(db.String, nullable=False)
    fat = db.Column(db.String, nullable=False)
    saturatedFat = db.Column(db.String, nullable=False)
    carbohydrates = db.Column(db.String, nullable=False)
    sugar = db.Column(db.String, nullable=False)
    cholesterol = db.Column(db.String, nullable=False)
    sodium = db.Column(db.String, nullable=False)
    protein = db.Column(db.String, nullable=False)
    fiber = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = relationship("Recipe", back_populates="nutritionfact")

class SimilarRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    similarRecipe_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255),nullable=False)
    imageUrl = db.Column(db.String, nullable=False)
    readyInMinutes = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'),nullable=False)

class Instruction(db.Model):
    __tablename__ = 'instruction'
    id = db.Column(db.Integer, primary_key=True)
    stepNumber = db.Column(db.Integer, nullable=False)
    stepDescription = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'),nullable=False)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique=True,nullable=False)
    imageUrl = db.Column(db.String, nullable=False)
    #One-to-Many relationship between Ingredient and ingredientAmount
    ingredientamounts = db.relationship('ingredientAmount', backref="ingredient", cascade="all, delete-orphan" , lazy='dynamic')

class ingredientAmount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    originalString = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'),nullable=False)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    savedIngredients = db.relationship('Ingredient', secondary=savedIngredients, lazy='subquery', backref=db.backref('users',lazy=True))
    savedRecipes = db.relationship('Recipe', secondary=savedRecipes, lazy='subquery', backref=db.backref('users',lazy=True))



admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Recipe, db.session))
admin.add_view(ModelView(Ingredient, db.session))
admin.add_view(ModelView(Detail, db.session))
admin.add_view(ModelView(NutritionFact, db.session))
admin.add_view(ModelView(SimilarRecipe, db.session))
admin.add_view(ModelView(Instruction, db.session))
admin.add_view(ModelView(ingredientAmount, db.session))
admin.add_view(ModelView(DishType, db.session))
admin.add_view(ModelView(Cuisine, db.session))
admin.add_view(ModelView(Diet, db.session))
admin.add_view(ModelView(Equipment, db.session))

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)
app.json_encoder = RecipeJSONEncoder

from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
# create a regular expression object that we'll use later   
class Recipe:
    db_name = 'recipes2023'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.dateMade = data['dateMade']
        self.under30 = data['under30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database


    @classmethod
    def get_recipe_by_id(cls, data):
        query = 'SELECT * FROM recipes WHERE id= %(recipe_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def getUserWhoLikedRecipes(cls, data):
        query = "SELECT likes.user_id as id from likes WHERE recipe_id = %(recipe_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likes = []
        if results:
            for like in results:
                likes.append( like['id'] )
            return likes
        return likes

    @classmethod
    def get_all(cls):
        query = "SELECT recipes.id as id, recipes.name as name, recipes.under30 as under30, recipes.user_id as user_id, COUNT(likes.id) as likes FROM recipes LEFT JOIN users on recipes.user_id = users.id LEFT JOIN likes on likes.recipe_id =recipes.id GROUP BY recipes.id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        if results:
            for recipe in results:
                recipes.append( recipe )
            return recipes
        return recipes
    
    # NOT NEEDED
    # @classmethod
    # def get_all_user_post(cls, data):
    #     query = "SELECT * FROM posts LEFT JOIN users on posts.user_id = users.id WHERE posts.user_id = %(user_id)s;"
    #     # make sure to call the connectToMySQL function with the schema you are targeting.
    #     results = connectToMySQL(cls.db_name).query_db(query, data)
    #     # Create an empty list to append our instances of friends
    #     posts = []
    #     # Iterate over the db results and create instances of friends with cls.
    #     if results:
    #         for post in results:
    #             posts.append( post )
    #         return posts
    #     return posts
    
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description,instructions,dateMade, under30, user_id) VALUES ( %(name)s, %(description)s,%(instructions)s, %(dateMade)s,%(under30)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def like(cls, data):
        query = "INSERT INTO likes (user_id, recipe_id) VALUES ( %(user_id)s, %(recipe_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND recipe_id = %(recipe_id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, dateMade = %(dateMade)s, under30 = %(under30)s WHERE id = %(recipe_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    # @classmethod
    # def delete_all_user_posts(cls, data):
    #     query = "DELETE FROM posts WHERE user_id = %(user_id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_recipe(r):
        is_valid = True
        # test whether a field matches the pattern
        
        if len(r['name'])< 2:
            flash('Name must be more than 2 characters', 'name')
            is_valid = False
        if len(r['description'])< 2:
            flash('Description must be more than 2 characters', 'description')
            is_valid = False
        if len(r['instructions'])< 2:
            flash('Instructions must be more than 2 characters', 'instruction')
            is_valid = False
        if not r['dateMade']:
            flash('Created date is required', 'dateMade')
            is_valid= False
        if not r['under30']:
            flash('Is this doable under 30 is required!', 'under30')
            is_valid= False
        return is_valid

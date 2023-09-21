from flask_app import app

from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe



@app.route('/add/recipe')
def addPost():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    }
    return render_template('addRecipe.html',loggedUser = User.get_user_by_id(loggedUserData))


@app.route('/create/recipe', methods = ['POST'])
def createPost():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(request.referrer)
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'dateMade': request.form['dateMade'],
        'under30': request.form['under30'],
        'user_id': session['user_id']
    }   
    Recipe.create_recipe(data)
    return redirect('/')


@app.route('/recipes/<int:id>')
def viewRecipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'recipe_id': id
    }
    loggedUser = User.get_user_by_id(data)
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('recipe.html', recipe = recipe, loggedUser = loggedUser)

@app.route('/recipes/edit/<int:id>')
def editRecipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'recipe_id': id
    }
    loggedUser = User.get_user_by_id(data)
    recipe = Recipe.get_recipe_by_id(data)
    if loggedUser['id'] == recipe['user_id']:
        return render_template('editRecipe.html', recipe = recipe, loggedUser = loggedUser)
    return redirect(request.referrer)

@app.route('/recipes/delete/<int:id>')
def deletePost(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'user_id': session['user_id'],
        'recipe_id': id
    }
    loggedUser = User.get_user_by_id(data)
    recipe = Recipe.get_recipe_by_id(data)
    if loggedUser['id'] == recipe['user_id']:
        Recipe.delete_recipe(data)
        return redirect(request.referrer)
    return redirect(request.referrer)

@app.route('/edit/recipe/<int:id>', methods = ['POST'])
def updateRecipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(request.referrer)
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'dateMade': request.form['dateMade'],
        'under30': request.form['under30'],
        'user_id': session['user_id'],
        'recipe_id': id
    }  
    loggedUser = User.get_user_by_id(data)
    recipe = Recipe.get_recipe_by_id(data) 
    if loggedUser['id'] == recipe['user_id']:
        Recipe.update_recipe(data)
        flash('Update succesfull!', 'updateDone')
        return redirect(request.referrer)
    return redirect('/')

@app.route('/like/<int:id>')
def like(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'recipe_id': id
    }
    usersWhoLikesThisRecipe = Recipe.getUserWhoLikedRecipes(data)
    if session['user_id'] not in usersWhoLikesThisRecipe:
        Recipe.like(data)
    return redirect(request.referrer)


@app.route('/unlike/<int:id>')
def unlike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'recipe_id': id
    }
    usersWhoLikesThisRecipe = Recipe.getUserWhoLikedRecipes(data)
    if session['user_id'] in usersWhoLikesThisRecipe:
        Recipe.unlike(data)
    return redirect(request.referrer)
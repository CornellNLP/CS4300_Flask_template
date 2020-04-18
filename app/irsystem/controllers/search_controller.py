from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from flask import request, jsonify
from sqlalchemy import and_, or_

from app import db
from app.irsystem.models import (
    Recipe, 
    Category,
    RecipeCategorization,
    RecipeSchema
)

recipe_schema = RecipeSchema(many=True)

"""
full_data = None
with open("app/full_format_recipes.json") as f:
    full_data = json.loads(f.readlines()[0])
"""

project_name = "Fitness Dream Team"
net_ids = "Genghis Shyy: gs484, Henri Clarke: hxc2, Alice Hu: ath84, Michael Pinelis: mdp93, Sam Vacura: smv66"

@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = ''
    else:
        query = query.lower()
        query_words = query.split(",")
        query_words = [word.strip() for word in query_words]
        for word in query_words:
            print(word)
        if len(query_words) == 1:
            query_words = query_words[0].split(";")
        recipes = Recipe.query.filter(
            or_(
                or_(Recipe.title.like("%{}%".format(word)) for word in query_words),
                or_(Recipe.description.like("%{}%".format(word)) for word in query_words),
                or_(Recipe.ingredients.like("%{}%".format(word)) for word in query_words),
                or_(Recipe.directions.like("%{}%".format(word)) for word in query_words)
            )
        ).all()
        recipes_out = recipe_schema.dump(recipes)
        output_message = "Your search: " + query
        output_lst = []
        for r in recipes_out:
            output_lst.append(r["title"])
        data = output_lst
    return render_template('search.html', name=project_name, netid=net_ids, output_message=output_message, data=data)
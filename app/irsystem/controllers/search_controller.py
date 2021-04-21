from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import pandas as pd
import csv
import scripts.sim as sim
from scripts.search import run_search
project_name = "Screen to Table"
net_id = "Olivia Zhu(oz28), Daniel Ye(dzy3), Shivank Nayak(sn532), Kassie Wang(klw242), Elizabeth Healy(eah255)"


@irsystem.route('/', methods=['GET'])
def home():
    query = request.args.get('search')
    msg = request.args.get('msg')
    if not query:
        data = []
        output_message = ''
        return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
    else:
        return redirect(url_for('irsystem.get_results', query=query))


@irsystem.route('/results')
def get_results():
    query = request.args.get("query")
    data = run_search(query)

    if data == None:
        # return redirect(url_for('irsystem.home', msg="try again"))
        return "No results :("
    else:
        res = []

        return render_template('results.html', res=res)


@irsystem.route('/recipe')
def get_recipe():
    idx = int(request.args.get("idx"))
    recipe = recipes[idx]
    title = recipe['Recipe Name']
    ingredients = recipe['Ingredients']
    steps = recipe['Directions']
    author = recipe['Author']
    # title = 'Recipe Name'
    # ingredients = 'Ingredients'
    # steps = 'Directions'
    return render_template('recipe.html',
                           title=title,
                           ingredients=ingredients,
                           steps=steps,
                           author=author)

from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import pandas as pd
import csv
import scripts.sim as sim
from scripts.search import run_search, get_recipe, get_closest
project_name = "Screen to Table"
net_id = "Olivia Zhu(oz28), Daniel Ye(dzy3), Shivank Nayak(sn532), Kassie Wang(klw242), Elizabeth Healy(eah255)"


@irsystem.route('/', methods=['GET'])
def home():
    query = request.args.get('search')

    if not query:
        return render_template('search.html', name=project_name, netid=net_id)
    else:
        return redirect(url_for('irsystem.results', query=query))


@irsystem.route('/results')
def results():
    query = request.args.get("query")
    data = run_search(query)

    if data == None:
        return "Did you mean " + get_closest(query)
    else:
        return render_template('results.html', res=data)


@irsystem.route('/recipe')
def recipe():
    idx = int(request.args.get("idx"))
    r = get_recipe(idx)
    # r['Ingredients'] = r['Ingredients']
    # r['Directions'] = r['Directions']
    # ingredients = ",".split(r['Ingredients'])
    # steps = ",".split(r['Directions'])
    # author = r['Author']

    return jsonify(r)
    # return render_template('results.html',
    #                        title=title,
    #                        ingredients=ingredients,
    #                        steps=steps,
    #                        author=author)

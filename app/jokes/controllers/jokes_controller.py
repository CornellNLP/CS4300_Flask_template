from . import *

"""
{
  "text": "hi",
  "categories": [1,2,3],
  "score": 2,
  "maturity": 2
} 
"""

@jokes.route('/', methods=['GET','POST'])
def handle_jokes():
  if request.method == 'POST':
    if request.is_json:
      data = request.get_json()
      new_joke = Joke(text=data['text'], categories=data['categories'], score=data['score'], maturity=data['maturity'])
      db.session.add(new_joke)
      db.session.commit()
      return {"message": "joke {new_joke.id} has been created successfully."}
    else:
      return {"error": "The request payload is not in JSON format"}

  elif request.method == 'GET':
    jokes = Joke.query.all()
    results = [
      {
        "text": joke.text,
        "categories": joke.categories,
        "score": str(joke.score),
        "maturity": joke.maturity,
      } for joke in jokes]

    return {"count": len(results), "jokes": results}
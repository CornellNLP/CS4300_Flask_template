from app.irsystem.models.get_data import data, trail_to_idx
import random


class Result:
    """
    Contains all the data needed to display a query result. 
    Takes in a tuple of (Cosine Similarity Score, Trail Name).

    Attributes include:
        - trail name (string)
        - GPS coordinates (float list)
        - difficulty (string)
        - activity types (list)
        - description (string)
        - reviews (string list)
        - random review (string)
    """

    def __init__(self, sim_tup, **kwargs):
        self.name = sim_tup[1]
        ith_trails = data[self.name]
        self.gps = ith_trails['GPS']
        self.length = ith_trails['Distance']
        self.difficulty = ith_trails['Difficulty']
        self.activity_types = []
        for activity in ith_trails['Trail Attributes']:
            self.activity_types.append(activity)
        self.description = ith_trails['Description']
        self.reviews = []
        for review in ith_trails["Reviews"]:
            if review['comment'] != "":
                self.reviews.append(review["comment"])
        self.review = self.reviews[random.randint(0, len(self.reviews))]
        # self.accessibility_types = kwargs.get('accessibility_types')

        
        
# Test Code
# ---------
# rslt = Result((.25, "Ellis Hollow Yellow trail"))
# print(rslt.name)
# print(rslt.difficulty)
# print(rslt.gps)
# print(rslt.length)
# # print(rslt.description)
# print(rslt.activity_types)
# print(rslt.reviews)




class Result:
    """
    Contains all the data needed to display a query result.
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.length = kwargs.get('length')
        # self.review = kwargs.get('review')
        # self.difficulty = kwargs.get('difficulty')
        # self.activity_types = kwargs.get('activity_types')
        # self.accessibility_types = kwargs.get('accessibility_types')

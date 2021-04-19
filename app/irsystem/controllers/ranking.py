def rank_by_points(reviews, n):
    """
    Returns: top n wine results sorted by highest points
    TODO: should it return scores/percentages to be combined with other measures?
    
    Parameter reviews: a list of dictionaries
    Parameter n: number of top results to return 
    TODO: return all or just top few?
    """
    return



def rank_by_price(reviews, price_range):
    """
    Returns: a list of wine reviews that fall in the inputted price range
    TODO: should it return scores/percentages to be combined with other measures?

    Parameter reviews: a list of dictionaries
    Parameter price_range: a tuple of user's preference on price range
    """
    result = []
    for review in reviews:
        price = reviews['price']
        if price >= price_range[0] and price <= price_range[1]:
            result.append(review)
    return result

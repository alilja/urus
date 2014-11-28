import os

from urus import Urus


class Beer(object):
    def __init__(self, name):
        with open("reviews/%s_reviews.txt" % name) as review_file:
            reviews = review_file.read().decode("utf").encode("ascii", "ignore").lower().split("<split>")
            self.tags = Urus.get_bag(reviews)
            self.name = name

beers = [
    Beer("summit"),
    Beer("tourdefall"),
    Beer("trappist"),
]
#files = os.listdir("reviews")
#for review_file in files:
#    beers.append(Beer(review_file[:review_file.find("_reviews.txt")]))

for beer in beers:
    target_beers = [target_beer for target_beer in beers if target_beer is not beer]
    for target_beer in target_beers:
        print "{0} vs. {1}: {2}".format(
            beer.name,
            target_beer.name,
            Urus.calculate_score(beer.tags, target_beer.tags, 10)
        )
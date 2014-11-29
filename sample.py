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

kmeans = Urus.get_kmeans([beer.tags for beer in beers])
print kmeans.predict(beers[0].tags)


# build k-means dataset
# then find points nearby in that cluster
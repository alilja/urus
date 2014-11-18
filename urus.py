from string import maketrans
from collections import Counter


class Beer(object):
    def _calculate_tag_weight(self, tags):
        total = len(tags)
        # weight everything on a curve, so the most common tags are highly weighted
        # do some normalization too
        return tags


class BeerFromReviews(Beer):
    def __init__(self, beer):
        with open("reviews/%s_reviews.txt" % beer) as review_file:
            reviews = review_file.read().decode("utf").encode("ascii", "ignore").lower().split("<split>")
            self.tags = self._get_bag(reviews)
        super(BeerFromReviews, self).__init__()

    def _get_bag(self, reviews):
        flavors = []
        for review in reviews:
            review = review.translate(maketrans("", ""), '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~')
            words = review.split(" ")
            flavors.extend([word for word in words if word in Urus._FLAVOR_CORPUS])

        bag_of_words = Counter(flavors)
        return bag_of_words


class Urus(object):
    _FLAVOR_CORPUS = []
    with open("flavors.txt") as review_file:
        _FLAVOR_CORPUS = review_file.readlines()
        _FLAVOR_CORPUS = [flavor.strip("\n") for flavor in _FLAVOR_CORPUS]

summit = BeerFromReviews("summit")
for tag in summit.tags:
    print tag

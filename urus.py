from string import maketrans
from collections import Counter
from math import log


class Beer(object):
    def _calculate_tag_weight(self, tags):
        total = sum(tags.values())
        most_common = tags.most_common(10)
        weights = {word: 1.1**(float(freq) / 2) for (word, freq) in tags.items()}
        return weights


class BeerFromReviews(Beer):
    def __init__(self, beer):
        with open("reviews/%s_reviews.txt" % beer) as review_file:
            reviews = review_file.read().decode("utf").encode("ascii", "ignore").lower().split("<split>")
            self.tags = self._calculate_tag_weight(self._get_bag(reviews))
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

    def calculate_score(self, beer_one, beer_two):
        # sum all the shared tags — scores that are
        # close to each other are more likely to be
        #
        for tag, score in beer_one.tags.items():
            if tag in beer_two.tags.keys():
                pass


summit = BeerFromReviews("summit")
tour = BeerFromReviews("tourdefall")
trappist = BeerFromReviews("trappist")

for tag, weight in summit.tags.items():
    print tag, weight

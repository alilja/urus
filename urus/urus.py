from string import maketrans
from collections import Counter

from pyxdameraulevenshtein import damerau_levenshtein_distance
levenshtein = damerau_levenshtein_distance

from sklearn.cluster import KMeans

from . import corpus


class Urus(object):
    _FLAVOR_CORPUS = corpus.flavors

    @classmethod
    def get_bag(cls, reviews):
        flavors = []
        for review in reviews:
            review = review.translate(maketrans("", ""), '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~')
            words = review.split(" ")
            flavors.extend(cls._match_flavor_words(words))

        bag_of_words = Counter(flavors)
        return bag_of_words

    @classmethod
    def _match_flavor_words(cls, words):
        output = []
        for word in words:
            if word in cls._FLAVOR_CORPUS:
                for flavor in cls._FLAVOR_CORPUS:
                    # 3 is arbitrary but seems good for suffixes and prefixes
                    # it should also be fairly useful for capturing typos
                    if levenshtein(word, flavor) < 3:
                        output.append(flavor)
                    else:
                        output.append(word)
        return output

    @staticmethod
    def equalize_dimensions(beers, replacement=0):
        """Ensures that all dicts will have the same keys.

        Args:
            beers: The target list of dicts.
            replacement: If a key doesn't exist in a dictionary, what
                value should be the new value

        Returns:
            A list of equalized dicts."""
        assert len(beers) > 1
        tag_set = set((key for beer in beers for key in beer))
        dimensional_data = []
        for tag in tag_set:
            dimensional_data.append([beer.get(tag, replacement) for beer in beers])
        return dimensional_data

    @staticmethod
    def get_kmeans(beers, clusters=8):
        """expects a list of beer tags"""
        assert len(beers) > 2
        return KMeans(n_clusters=8).fit(Urus.equalize_dimensions(beers))

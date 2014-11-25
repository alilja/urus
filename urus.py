from string import maketrans
from collections import Counter

from pyxdameraulevenshtein import damerau_levenshtein_distance
levenshtein = damerau_levenshtein_distance


class Urus(object):
    _FLAVOR_CORPUS = []
    with open("flavors.txt") as review_file:
        _FLAVOR_CORPUS = review_file.readlines()
        _FLAVOR_CORPUS = [flavor.strip("\n") for flavor in _FLAVOR_CORPUS]

    @staticmethod
    def get_bag(reviews):
        flavors = []
        for review in reviews:
            review = review.translate(maketrans("", ""), '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~')
            words = review.split(" ")
            flavors.extend(Urus._match_flavor_words(words))

        bag_of_words = Counter(flavors)
        return bag_of_words

    @staticmethod
    def _match_flavor_words(words):
        output = []
        for word in words:
            if word in Urus._FLAVOR_CORPUS:
                for flavor in Urus._FLAVOR_CORPUS:
                    # 3 is arbitrary but seems good for suffixes and prefixes
                    if levenshtein(word, flavor) < 3:
                        output.append(flavor)
                    else:
                        output.append(word)
        return output

    @staticmethod
    def calculate_score(self, tags_one, tags_two):
        # sum all the shared tags -- scores that are
        # close to each other are more likely to be
        #
        for tag, score in tags_one.items():
            if tag in tags_two.keys():
                pass

from string import maketrans
from collections import Counter

from pyxdameraulevenshtein import damerau_levenshtein_distance
levenshtein = damerau_levenshtein_distance

import corpus


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
    def calculate_score(base, target, n=10):
        def expected(tags_one, tags_two, word):
            n_one = sum((freq for (key, freq) in tags_one.most_common(n)))
            n_two = sum((freq for (key, freq) in tags_two.most_common(n)))
            return (
                (n_one * (tags_one[word] + tags_two[word])) /
                (n_one + n_two)
            )

        def calculate_chi(tags_one, tags_two, word):
            exp = expected(tags_one, tags_two, word)
            return (tags_one[word] - exp  ** 2) / exp
        chi = 0
        for i in range(n):
            for word, frequency in base.items():
                if word in target.keys():
                    chi += calculate_chi(base, target, word)

        return chi


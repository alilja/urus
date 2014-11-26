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
        """ implementation according to
        http://luthuli.cs.uiuc.edu/~daf/courses/Signals%20AI/Papers/Collocation/kilgarriff98measures.pdf"""
        def rank_tags(tags):
            tupled = map(tuple, enumerate(sorted(tags, key=tags.get, reverse=True)))
            return [(a, b) for (b, a) in tupled]

        base_common = dict(rank_tags(base)[:n])
        target_common = dict(rank_tags(target)[:n])

        differences = []
        for tag, rank in base_common.items():
            if tag in target_common.keys():
                differences.append((target_common[tag] - rank)**2)
            else:
                differences.append(10)
        return 1 - (
            float(6 * sum(differences)) /
            float(n * (n**2 - 1))
        )




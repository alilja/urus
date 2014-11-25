from urus import Urus


class Beer(object):
    def __init__(self, name):
        with open("reviews/%s_reviews.txt" % name) as review_file:
            reviews = review_file.read().decode("utf").encode("ascii", "ignore").lower().split("<split>")
            self.tags = Urus.get_bag(reviews)
            self.name = name


summit = Beer("summit")
tour = Beer("tourdefall")
trappist = Beer("trappist")

print summit.tags.most_common(15)
print "---"
print trappist.tags.most_common(15)
print "---"
print [(key, value) for key, value in summit.tags.items() if key in trappist.tags.keys()]

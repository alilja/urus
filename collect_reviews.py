import os
from string import maketrans

from ratebeer import RateBeer

beers = []
files = os.listdir("reviews")
for review_file in files:
    beers.append(review_file[:review_file.find("_reviews.txt")])

print beers

rb = RateBeer()
styles = rb.beer_style_list()

for style, url in styles.items():
    beers = rb.beer_style(url)
    print style.upper()
    for beer in beers:
        print "On beer " + beer['name']
        name = "".join(beer['name'].lower().split(" "))
        name = name.encode("ascii","ignore")
        name = name.translate(maketrans("", ""), '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~')
        print name
        if name not in beers:
            reviews = rb.reviews(beer['url'], pages=10, review_order="highest score")
            with open("reviews/%s_reviews.txt" % name, "w") as write_file:
                for review in reviews:
                    write_file.write(review['text'].encode('utf-8') + "<split>")

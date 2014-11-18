from ratebeer import RateBeer

filename = "trappist"
url = "/beer/engelszell-gregorius-trappistenbier/171748/"

rb = RateBeer()
reviews = rb.reviews(url, pages=10, review_order="highest score")
with open("%s_reviews.txt" % filename, "w") as write_file:
    for review in reviews:
        write_file.write(review['text'].encode('utf-8') + "<split>")

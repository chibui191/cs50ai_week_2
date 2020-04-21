corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}

damping_factor = 0.85
page = "1.html"

pages_count = len(corpus)
links = corpus[page]
links_count = len(links)
prob_distribution = dict()
output = dict()

# if page has >=1 outgoing link(s) to other pages
if links_count >= 1:
    # probability of landing on current page again:
    # (1-d)/pages_count chance will land on same page
    prob_distribution[page] = (1 - damping_factor) / pages_count

    # probability of other links:
    for link in links:
        prob_distribution[link] = prob_distribution[page] + damping_factor / links_count

# if page doesn't have any outgoing links --> return a {} that chooses randomly among all pages with equal probability including itself
else:
    prob_distribution = {each: (1 / pages_count) for each in corpus.keys()}

probs = list(prob_distribution.values())
prob_factor = 1 / sum(probs)
output = {key: round((prob_factor * p), 4) for (key, p) in prob_distribution.items()}

print(output)

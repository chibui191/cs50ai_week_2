import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print(round(sum(ranks.values()), 4))
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print(round(sum(ranks.values()), 4))


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def normalize(prob_distribution):
    prob_factor = 1 / sum(prob_distribution.values())
    return {page: (prob_factor * prob) for (page, prob) in prob_distribution.items()}


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages_count = len(corpus)
    links = corpus[page]
    links_count = len(links)
    output = dict()

    # if page has >=1 outgoing link(s) to other pages
    if links_count >= 1:
        # (1-d)/pages_count chance will land on same page
        output[page] = (1 - damping_factor) / pages_count

        # probability of following other links:
        for link in links:
            output[link] = output[page] + (damping_factor / links_count)

    # if page doesn't have any outgoing links --> return a {} that has all pages with equal probability including itself
    else:
        output = {pg: float(1 / pages_count) for pg in corpus.keys()}

    return normalize(output)


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_list = list(corpus.keys())
    # initialize samples dictionary, all with count values = 0 to keep track of all samples
    samples = dict()
    for each in page_list:
        samples[each] = 0

    # first sample - choosing a page at random from page_list
    sample = random.choice(page_list)
    samples[sample] += 1

    # remaining (n - 1) samples
    for _ in range(n - 1):
        # pass current sample into transition_model to get distribution probabilities for next pick:
        next_options = transition_model(corpus, sample, damping_factor)
        # replace sample with 1 new value randomly picked from weighted distribution dict
        sample = random.choices(
            list(next_options.keys()),
            list(next_options.values()),
            k=1
        )[0]
        samples[sample] += 1
        
    # output is a dictionary with key = page and value = float(count of that page/n) in samples
    output = {pg: float(pg_count / n) for (pg, pg_count) in samples.items()}

    return normalize(output)

        
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_list = corpus.keys()
    pages_count = len(corpus)
    pages_incoming = dict()

    # first step - initialize prob distribution dict, all with values = 1 / pages_count
    prob_distribution = dict()
    for each in page_list:
        prob_distribution[each] = (1 / pages_count)

    # create another dictionary with key = page and value = its incoming pages for all pages
    for pg1 in page_list:
        incoming_pages = set()
        for pg2 in page_list:
            if len(corpus[pg2]) >= 1:
                if pg1 in corpus[pg2]:
                    incoming_pages.add(pg2) 
                else:
                    continue
            else:
                incoming_pages.add(pg2)

        pages_incoming[pg1] = incoming_pages

    # create a change dictionary to keep track of PR changes for all pages each calculation
    change = dict()
    for each in page_list:
        change[each] = 0.0

    while True:
        # iteration formula
        for (pg, current_pr) in prob_distribution.items():
            # get all inbound pages for pg
            inbounds = pages_incoming[pg]
            # calculate new PR for pg
            new_pr = (1 - damping_factor) / pages_count
            a = 0.0
            for i in inbounds:
                a += prob_distribution[i] / len(corpus[i]) if len(corpus[i]) >= 1 else prob_distribution[i] / pages_count
            new_pr += (a * damping_factor)

            # update PR change for pg
            change[pg] = float(new_pr - current_pr)
            # update PR for pg to new PR
            prob_distribution[pg] = new_pr

        # break out of while loop when change < 0.001 for ALL pages
        if all(abs(x) < 0.001 for x in change.values()):
            break    

    return normalize(prob_distribution)


if __name__ == "__main__":
    main()

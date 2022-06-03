import sys

if len(sys.argv) < 2:
    print("Usage: python search.py <path_to_index>")
    sys.exit(1)

from pyserini.search.lucene import LuceneSearcher
searcher = LuceneSearcher(sys.argv[-1])

import time


def run_query(query):
    t0 = time.time()
    print("QUERY", query)
    hits = searcher.search(query)
    dt = time.time() - t0

    print("TIME", dt)
    for i in range(len(hits)):
        print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')


line = ""

while True:
    line = input(">> ")
    if line in ["stop", "exit", "quit"]: break
    run_query(line)

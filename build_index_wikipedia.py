import json
import gzip

from gensim.models import KeyedVectors
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from joblib import Parallel, delayed

from swem import MeCabTokenizer
from swem import SWEM


def index_batch(docs):
    requests = Parallel(n_jobs=-1)([delayed(get_request)(doc) for doc in docs])
    bulk(client, requests)


def get_request(doc):
    return {"_op_type": "index",
            "_index": INDEX_NAME,
            "text": doc["text"],
            "title": doc["title"],
            "text_vector": swem.average_pooling(doc["text"]).tolist()
            }


# embedding
w2v_path = "jawiki.word_vectors.200d.txt"
w2v = KeyedVectors.load_word2vec_format(w2v_path, binary=False)
tokenizer = MeCabTokenizer("-O wakati")
swem = SWEM(w2v, tokenizer)

# elasticsearch
client = Elasticsearch()
BATCH_SIZE = 1000
INDEX_NAME = "wikipedia"

client.indices.delete(index=INDEX_NAME, ignore=[404])
with open("index.json") as index_file:
    source = index_file.read().strip()
    client.indices.create(index=INDEX_NAME, body=source)


docs = []
count = 0
with gzip.open("jawiki-20190826-cirrussearch-content.json.gz") as f:
    for line in f:
        json_line = json.loads(line)
        if "index" not in json_line:
            doc = json_line

            docs.append(doc)
            count += 1

            if count % BATCH_SIZE == 0:
                index_batch(docs)
                docs = []
                print(f"Indexed {count} documents. {100.0*count/1165654}%")
    if docs:
        index_batch(docs)
        print("Indexed {} documents.".format(count))

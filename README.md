# Text Similarity Search by using Elasticsearch

- [Text similarity search in Elasticsearch using vector fields \| Elastic Blog](https://www.elastic.co/jp/blog/text-similarity-search-with-vectors-in-elasticsearch)
- [jtibshirani/text\-embeddings](https://github.com/jtibshirani/text-embeddings)

## Preparation

```
$ wget https://dumps.wikimedia.org/other/cirrussearch/20190826/jawiki-20190826-cirrussearch-content.json.gz

$ wget https://github.com/singletongue/WikiEntVec/releases/download/20190520/jawiki.word_vectors.200d.txt.bz2
$ bunzip2 jawiki.word_vectors.200d.txt.bz2
```

```
$ docker-compose up
```

```
$ python build_index_wikipedia.py
```

## Text Similarity Search

```
$ python search.py
```

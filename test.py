from elasticsearch import Elasticsearch, RequestsHttpConnection

clusters = {
    "common_2": "https://vpc-poseidon-env2-2-kw7hnzhzzgkqlxznkbqdgvjt7i.us-east-1.es.amazonaws.com"
    }
query_body = {
    "size": 10,
    "query": {
        "match_all": {}
    }
}
for key in clusters:
    host = clusters[key]
    es = Elasticsearch(
        hosts=host,
        use_ssl=False,
        connection_class=RequestsHttpConnection)
    res = es.search(index="poseidon-common-*", body=query_body, request_timeout=3000)
    print(res)
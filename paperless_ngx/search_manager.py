import os
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

class SearchManager:
    def __init__(self, index_dir="indexdir"):
        self.index_dir = index_dir
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
            self.create_index()
        self.index = open_dir(index_dir)

    def create_index(self):
        schema = Schema(
            doc_id=ID(stored=True, unique=True),
            title=TEXT(stored=True),
            content=TEXT(stored=True)
        )
        create_in(self.index_dir, schema)

    def add_document(self, doc_id, title, content):
        with self.index.writer() as writer:
            writer.add_document(doc_id=str(doc_id), title=title, content=content)

    def search(self, query_string):
        parser = QueryParser("content", schema=self.index.schema)
        query = parser.parse(query_string)
        with self.index.searcher() as searcher:
            results = searcher.search(query, limit=10)
            return [
                {"doc_id": hit["doc_id"], "title": hit["title"]}
                for hit in results
            ]

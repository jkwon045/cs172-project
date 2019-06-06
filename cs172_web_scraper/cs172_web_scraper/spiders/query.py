import lucene, os, sys

from java.nio.file import Paths
from java.util import HashMap
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser, QueryParser, QueryParserBase
from org.apache.lucene.search import IndexSearcher, Query, BooleanClause
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer

FILE_DIR = '/pages'
INDEX_DIR = '/indexes'

FIELDS = ["contents", "filename"]
class Searcher:
	def __init__(self, indexDir):
		f = Paths.get(indexDir)
		self._dir = SimpleFSDirectory(f)
		self._indexSearcher = IndexSearcher(DirectoryReader.open(self._dir))
		self._weights = HashMap()
		self._weights.put(FIELDS[0],1)
		self._weights.put(FIELDS[1],0.2 )
	def search(self, query):
		SHOULD = BooleanClause.Occur.SHOULD
		q = MultiFieldQueryParser.parse("white house", FIELDS, [SHOULD, SHOULD], StandardAnalyzer())
		print(q.toString())
		topHits = 100
		scores = self._indexSearcher.search(q, topHits).scoreDocs
		for i in range(3):
			doc = self._indexSearcher.doc(scores[i].doc)
			print(i+1)
			print("Score: ", scores[i].doc)
			print("Title: ", doc.get("filename"))
			print("Contents: ", doc.get("contents"))

if __name__ == '__main__':
	lucene.initVM(vmargs=['-Djava.awt.headless=true'])
	print("lucene", lucene.VERSION)
	testSearcher = Searcher(os.getcwd()+INDEX_DIR)
	testSearcher.search("ABC")

import sys, os, lucene, re, urllib.request
from java.nio.file import Paths
from org.apache.lucene.analysis.core import StopAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer, StandardFilter
from org.apache.lucene.analysis import StopFilter, LowerCaseFilter
from org.apache.lucene.document import Document, Field, FieldType, TextField
#import org.apache.lucene.document
from org.apache.lucene.index import FieldInfo, IndexWriter
from org.apache.lucene.index import IndexOptions, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory



FILE_DIR = '/pages'
INDEX_DIR = '/indexes'

class Indexer(object):
	# Creates index adds it to docs
	# indexDir Directory is where the index is created
	def __init__(self, indexDir):
		f = Paths.get(indexDir)
		self._dir = SimpleFSDirectory(f)
		analyzer = StandardAnalyzer()
		config = IndexWriterConfig(analyzer)
		config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
		self._writer = IndexWriter(self._dir, config)
		
	def close(self):
		self._writer.close()

	def getDoc(self, file):
		try:
			f = open(os.getcwd()+FILE_DIR+'/'+file, "r")
			try:
				c = str(f.read())
			except Exception:
				return
			content = TextField("contents", c, Field.Store.YES)
			filename = TextField("filename",
							 str(Paths.get(file)),
							 Field.Store.YES)
			path = TextField("filepath",
						 str(os.getcwd()+FILE_DIR+'/'+file),
						 Field.Store.YES)
			doc = Document()
			doc.add(content)
			doc.add(filename)
			doc.add(path)
			return doc
		except Exception:
			print(type(Exception).__name__)
			return

	def indexFile(self, file):
		if ( self.getDoc(file) is not None ):
			self._writer.addDocument(self.getDoc(file))
	#pass in absolute path when calling this function
	def createIndex(self, path):
		for file in os.listdir(path):
			print(file)
			if os.path.isfile(path+"/"+file):
				self.indexFile(file)
		return self._writer.numDocs()


if __name__ == '__main__':
	lucene.initVM(vmargs=['-Djava.awt.headless=true'])
	print("lucene", lucene.VERSION)
	testIndexer = Indexer(os.getcwd()+INDEX_DIR)
	testIndexer.createIndex(os.getcwd()+FILE_DIR)
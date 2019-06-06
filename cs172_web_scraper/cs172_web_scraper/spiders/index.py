import sys, os, lucene, re, urllib.request

from java.nio.file import Paths
from org.apache.lucene.analysis.core import StopAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer, StandardFilter
from org.apache.lucene.analysis import StopFilter, LowerCaseFilter
from org.apache.lucene.document import Document, Field, FieldType, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter
from org.apache.lucene.index import IndexOptions, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from bs4 import BeautifulSoup
from bs4.element import Comment
FILE_DIR = '/pages'
INDEX_DIR = '/indexes'

def tag_vis(element):
	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True

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
				c = []
				s = BeautifulSoup(f, 'html.parser')
				text = s.findAll(text=True)
				c = filter(tag_vis, text)
				try:
					c = ' '.join(c)
				except Exception as e:
					c = b' '.join(c)
			except Exception as e:
				print(str(e))
				return
			content = TextField("contents", c, Field.Store.YES)
			fileName = str(Paths.get(file)).split('/')[-1]
			fileName = fileName[:fileName.find(".")]
			filename = TextField("filename",
							 fileName,
							 Field.Store.YES)
			path = TextField("filepath",
						 str(os.getcwd()+FILE_DIR+'/'+file),
						 Field.Store.NO)
			doc = Document()
			doc.add(content)
			doc.add(filename)
			doc.add(path)
			return doc
		except Exception as e:
			print(type(Exception).__name__)
			print(str(e))
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
	def closeWriter(self):
		self._writer.close()

if __name__ == '__main__':
	lucene.initVM(vmargs=['-Djava.awt.headless=true'])
	print("lucene", lucene.VERSION)
	testIndexer = Indexer(os.getcwd()+INDEX_DIR)
	testIndexer.createIndex(os.getcwd()+FILE_DIR)
	testIndexer.closeWriter()
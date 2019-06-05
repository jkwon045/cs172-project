import sys, os, lucene
import re
from java.nio.file import Paths
from org.apache.lucene.util.Constants import 
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer, StandardFilter
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, FileReader
from org.apache.lucene.index import IndexOptions, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory

FILE_DIR = '/pages'
INDEX_DIR = '/indexes'

class Page():
	def __init__(self, title, content):
		self.title = title
		self.content = content

	def getContent(self):
		return self.content

	def getTitle(self):
		return self.title

class Indexer(object):
	# Creates index adds it to docs
	# indexDir Directory is where the index is created
	def __init__(self, indexDir):
		f = File(indexDir)
		self._dir = SimpleFSDirectory(f)
		analyzer = StopFilter(LowerCaseFilter(StandardAnalyzer()), StopAnalyzer.ENGLISH_STOP_WORDS_SET)
		self._writer = IndexWriter(self._dir, analyzer)
		
	def close(self):
		self._writer.close()

	def getDoc(self, file, filename):
		content = Field(LuceneConstants.CONTENTS, FileReader())
		filename = Field(LuceneConstants.FILE_NAME,
						 filename,
						 Field.Store.YES,
						 Field.Index.NOT_ANALYZED)
		path = Field(LuceneConstants.FILE_PATH,
					 str(os.getcwd()+FILE_DIR+'/'+file),
					 Field.Store.YES,
					 Field.Index.NOT_ANALYZED)
		doc = Document()
		doc.add(content)
		doc.add(filename)
		doc.add(path)
		return doc
	def indexFile(self, file):
		self._writer.addDocument(getDoc(file))
	#pass in absolute path when calling this function
	def createIndex(self, path, filter):
		for file in os.listdir(path):
			if os.path.isfile(path+"/"+file):
				self.indexFile(file)
		return self._writer.numDocs()


if __name == '__main__':
	lucene.initVM(vmargs=['-Djava.awt.headless=true'])
	print("lucene", lucene.VERSION)
	testIndexer = Indexer(os.getcwd()+FILE_DIR)
	'''
	initJVM()
	global FILE_DIR
	global INDEX_DIR
	fd = os.getcwd()+FILE_DIR
	indexdir = os.getcwd()+INDEX_DIR
	allPages = []
	for file in os.listdir(fd):
		content = []
		filename = file[:file.find('.html')]
		f = open(fd+'/'+file, 'r')
		try:
			for line in f:
				if ( line != '' ):
					content.append(line)
		except UnicodeDecodeError:
			p = Page(filename, '\n'.join(content))
			allPages.append(p)
			f.close()
			continue
		p = Page(filename, '\n'.join(content))
		allPages.append(p)
		print(filename)'''
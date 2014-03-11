import web
from web import form
import datetime
from random import randint
import os
import time

render = web.template.render('templates/')
urls = ('/', 'index', '/link/(.*)', 'Link', '/rm/(.*)', 'rm')
linkDict = {}

class index:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self):
		form = '<form method="POST" enctype="multipart/form-data" action=""><input type="file" name="myfile" /><input type="submit" /></form>'
		return self.render.index(form)

	def POST(self):
		x = web.input(myfile={})
		filename = (x['myfile'].filename)
		what = (x['myfile'].file.read()) 
		submittedFile = open('static/store/' + filename, 'wb')
		submittedFile.write(what)
		submittedFile.close()
		return self.linkGen(filename)

	def linkGen(self, filename):
		i = datetime.datetime.now()

		link = i.hour * i.minute * i.second
		if link != 0:
			link = link * randint(2,500)
		else:
			link = randint(2,500) * len(filename)

		linkDict[link] = filename
		httpLink = 'http://localhost:8080/link/' + str(link)
		return self.render.index(httpLink)

class Link:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, link):
		if os.path.isfile('static/store/' + linkDict[int(str(link))]):
			link = link.strip('link/')
			request = '../static/store/' + linkDict[int(str(link))]
			#f = open(request, 'rb').read()
			return self.render.link(link=request, linkNum=link)
			#os.remove(request)
			#del linkDict[int(str(link))]
		else:
			return self.render.index('Nothing here...')

class rm:
	def __init__(self, linkURL):
		print 'called'
		print linkURL

if __name__ == "__main__":
	app = web.application(urls, globals()) 
	app.run()
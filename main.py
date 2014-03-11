import web
from web import form
import datetime
from random import randint
import os
import time

render = web.template.render('templates/')
urls = ('/', 'index', '/link/(.*)', 'Link', '/a/(.*)', 'a', '/about', 'about')
linkDict = {}

class index:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self):
		form = '<form method="POST" enctype="multipart/form-data" action=""><input type="file" name="myfile" onchange="this.form.submit();"/>'
		return self.render.index(form)

	def POST(self):
		x = web.input(myfile={})
		filename = (x['myfile'].filename)
		what = (x['myfile'].file.read()) 
		submittedFile = open('store/' + filename, 'wb')
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
		raise web.seeother('/a/' + str(link))

class Link:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, link):
		link = link.strip('link/')
		if int(str(link)) in linkDict.keys():
			request = 'store/' + linkDict[int(str(link))]
			f = open(request, 'rb')
			web.header('Content-Type','application/binary')
			web.header('Content-Disposition','attachment; filename="' + linkDict[int(str(link))] + '"')
			while True:
				buf = f.read(1024)
				if len(buf) == 0:
					break
				yield buf
			f.close()
			os.remove(request)
			del linkDict[int(str(link))]
		else:
			yield self.render.index('Nothing here...')

class a:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, value):
		return self.render.link('http://localhost:8080/link/' + str(value))

class about:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self):
		return self.render.about()

if __name__ == "__main__":
	app = web.application(urls, globals()) 
	app.run()
import web
from web import form
import datetime
from random import randint
import os
import time
import MySQLdb

configFile = open('config', 'r')
config = {}
for line in configFile:
	line = line.split(':')
	config[line[0]] = line[1].strip('\n')

db = MySQLdb.connect(host=config['dbHost'], user=config['dbUser'], passwd=config['dbPass'], db=config['db'])

render = web.template.render('templates/')
urls = ('/', 'index', '/link/(.*)', 'Link', '/a/(.*)', 'a', '/about', 'about', '/download/(.*)', 'Download')

class index:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self):
		#form = '<form method="POST" enctype="multipart/form-data" action=""><input type="file" name="myfile" onchange="this.form.submit();"/>'
		form = '<form id="uploadForm" method="POST" enctype="multipart/form-data" action=""><input type="file" id="uploadedFile" name="myfile" /><input type="submit" /><br><em>Max upload size: 10mb</em>'
		return self.render.index(form)

	def POST(self):
		x = web.input(myfile={})
		filename = (x['myfile'].filename)
		what = (x['myfile'].file.read())
		if len(what) < 10485760: 
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

		with db:
			cur = db.cursor()
			cur.execute("INSERT INTO files VALUES (%s, %s)", (filename, link))
		raise web.seeother('/a/' + str(link))

class Link:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, link):
		link = link.strip('link/')
		return self.render.download(link)

class a:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, value):
		return self.render.link('http://deadrop.cc/link/' + str(value))

class about:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self):
		return self.render.about()

class Download:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, link):
		link = link.strip('link/')
		link = int(link)
		with db:
			cur = db.cursor()

			if cur.execute("SELECT filename FROM files WHERE link={0}".format(link)):
				row = cur.fetchone()
				filename = row[0]
				request = 'store/' + filename
				
				f = open(request, 'rb')
				
				web.header('Content-Type','application/binary')
				web.header('Content-Disposition','attachment; filename="' + filename + '"')
				
				while True:
					buf = f.read(1024)
					if len(buf) == 0:
						break
					yield buf
				f.close()
				os.remove(request)
				cur.execute("DELETE FROM files WHERE link={0}".format(link))
			else:
				yield self.render.index('Nothing here...')

if __name__ == "__main__":
	app = web.application(urls, globals()) 
	app.run()

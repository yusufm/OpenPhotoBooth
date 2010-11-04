# -*- coding: utf-8 -*-

"""
Copyright (c) 2009 John Hobbs, Little Filament

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import web
import Image
import base64
import time

web.config.debug = False

urls = (
	'/', 'main',
	'/set/open', 'open_set',
	'/set/close', 'close_set',
	'/photo', 'save_photo',
	'/set/print', 'print_set',
  '/favicon.ico', 'favicon_serve'
)

# Need a render engine for the core template files
core_render = web.template.render( 'static/core/' )
# Now make that available to the template engine as a global
web.template.Template.globals['core'] = core_render

# A configuration object to pass information to themes
opb = {
	'core_path': '/static/core/',
	'vendor_path': '/static/vendor/',
	'theme_path': '/static/themes/default/',
  'thumb_path': '/static/thumbs/'
}

theme_render = None
set_id = False
set_photos = []

# Sets everything required for properly rendering a theme
def SetTheme ( theme_name ):
	global theme_render
	global opb
	opb['theme_path'] = '/static/themes/%s/' % ( theme_name )
	theme_render = web.template.render( 'static/themes/%s/' % ( theme_name ) )

# Create the application
app = web.application( urls, globals() )

class main:
	def GET( self ):
		return theme_render.index( opb )

class save_photo:
	def POST( self ):
		global set_id
		global set_photos
		web.header( 'Content-type', 'application/json; charset=utf-8' )

		""" Save the photo data, thumbnail it and move on. """
		i = web.input( image=None )

		if False != set_id:
			filename = "%s_%s.jpg" % ( set_id, int( time.time() ) )
		else:
			filename = "NOSET_%s.jpg" % ( int( time.time() ) )

		set_photos.append(filename)
		fullsize = open( './static/photos/' + filename, 'wb' )
		fullsize.write( base64.standard_b64decode( i.image ) )
		fullsize.close()

		size = 160, 120
		im = Image.open( './static/photos/' + filename )
		im.thumbnail( size )
		im.save( './static/thumbs/' + filename, "JPEG" )
		return '{ "saved": true, "thumbnail": "%s" }' % ( filename )

class print_set:
	def GET ( self ):
		global set_photos
		self.printout( self.construct_print( 'background.jpg' ) )
	
	def construct_print ( self, backgroundfile ):
		global set_id
		global set_photos
		background = Image.open( "./" + opb['theme_path'] + '/%s' % ( backgroundfile ) )
		placement = open( "./" + opb['theme_path'] + '/%s.cfg' % ( backgroundfile ) )
		for count, line in enumerate( placement ):
			pos, size = eval( line )
			i1 = set_photos[ (count % len( set_photos ) )]
			background.paste( Image.open('./static/photos/' + i1).resize(size), pos )
		if False != set_id:
                        outfile = "./static/photos/%s_%s_print.jpg" % ( set_id, int( time.time() ) )
                else:
                        outfile = "./static/photos/NOSET_%s_print.jpg" % ( int( time.time() ) )
		print_output = background.save( outfile )
		return outfile

	def printout( self , filename ):
		try:
			import win32api
			win32api.ShellExecute ( 0, "print", filename, None, ".", 0 )
		except ImportError:
			# Probably not Win, try printing via lpr
			import subprocess
			subprocess.Popen(['lpr', filename])

class open_set:
	def GET ( self ):
		global set_id
		global set_photos
		set_id = "%s" % int( time.time() )
		set_photos = []
		return '{ "set": "%s" }' % set_id

class close_set:
	def GET ( self ):
		global set_id
		global set_photos
		set_id = False
		set_photos = []
		return '{ "set": false }'

class favicon_serve:
	def GET ( self ):
		raise web.redirect( '/static/favicon.ico' )

if __name__ == "__main__" :
	SetTheme( 'default' )
	app.run()

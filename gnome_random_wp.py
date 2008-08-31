#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Gnome random wallpaper changer

By Sunny Ripert <negatif@gmail.com> <http://sunfox.org>
Who revamped a script by Maximilien Cuony <maxi_the_glu@bluewin.ch> <http://theglu.tuxfamily.org>
Which was based on a script by guix77 <http://linuxfr.org/comments/465267.html#465267>
"""
 
import os, re, time, random, commands, sys
from getopt import gnu_getopt, GetoptError
 
 
# defaults 
seconds = 60
images_path = '.'
images_re = re.compile('\.(png|jpg|jpeg|svg|gif)$')
 
 
# functions
 def images_in_dir(images_path):
	"""Returns list of paths to all images found recursively in given folder path"""
	images = []
	for path, dirs, files in os.walk(images_path):
		for filename in files:
			if images_re.match(filename):
				images.append(os.path.join(path, filename))
	return images
 
 
def set_random_background_image(images):
	"""Sets a random background choosing from given list of filenames"""
	filename = random.choice(images)
	guix = "gconftool-2 -t string -s /desktop/gnome/background/picture_filename '%s'" % str(filename)
	commands.getstatusoutput(guix)
 
 
def main():
	"""Main program loop"""
	try: images = images_in_dir(images_path) # look for images
	except OSError, e:
		print >> sys.stderr,  e
		sys.exit(2)
 
	if len(images) == 0:
		print >> sys.stderr, "Error: no images found in '%s'" % images_path
		sys.exit(2)
 
	# main loop
	try:
		while True:
			set_random_background_image(images)
			time.sleep(seconds)
	except KeyboardInterrupt: # intercept ctrl-c
		sys.exit(0)
 
 
if __name__ == '__main__':
	try: options, args = gnu_getopt(sys.argv[1:], 'hs:p:', ['sec=', 'help', 'path='])
	except GetoptError, e:
		print >> sys.stderr, 'Error: %s.' % e
		print >> sys.stderr, 'Type "%s --help" for more information.' % sys.argv[0]
		sys.exit(1)
	for option, value in options:
		if option in ["-s", "--sec"]:
			seconds = int(value)
		elif option in ["-p", "--path"]:
			images_path = value
		elif option in ["-h", "--help"]:
			print "Usage: %s [options]" % sys.argv[0]
			print "Modifies your Gnome desktop background periodically."
			print ""
			print "Options:"
			print "-h, --help                 shows this help"
			print '-p, --path=PATH            sets the path where it will look for images (defaults to "%s")' % images_path
			print '-s, --sec=SECONDS          sets the period between each background change (defaults to %ss)' % seconds
			sys.exit(0)
 
	# start main loop
	main()
 

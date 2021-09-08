#!/usr/bin/python

# License for any modification to the original (linked below):
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Sebastiano Poggi and Daniele Conti wrote this file. As long as you retain
# this notice you can do whatever you want with this stuff. If we meet some day,
# and you think this stuff is worth it, you can buy us a beer in return.

import argparse, sys, subprocess, tempfile
from os.path import splitext
from distutils.spawn import find_executable

def look_for_ffmpeg_or_abort():
	ffmpeg_path = find_executable('ffmpeg')
	if ffmpeg_path == None:
	  print("** ComputerSaysNoError **")
	  print("You need to have ffmpeg installed on your system and on the path for Giffify to work")
	  exit(1)

def parse_cli_arguments():
	parser = argparse.ArgumentParser(description='Processes a video into a gif.')
	parser.add_argument('video', type=str, help='The video to be processed')
	parser.add_argument('-o', '--outfile', type=str, help='Target path')
	parser.add_argument('-dw', '--desired-width', type=int, default=-1)
	parser.add_argument('-dh', '--desired-height', type=int, default=-1)
	parser.add_argument('-f', '--fps', type=int, default=15, help='Output frames per second. Default: 15 fps')
	parser.add_argument('-s', '--start-time', type=int, default=-1, help='Start timestamp, as [-][HH:]MM:SS[.m...] or [-]S+[.m...]')
	parser.add_argument('-e', '--end-time', type=int, default=-1, help='End timestamp, as [-][HH:]MM:SS[.m...] or [-]S+[.m...]. Overridden by -d')
	parser.add_argument('-d', '--duration', type=int, default=-1, help='Duration, as [-][HH:]MM:SS[.m...] or [-]S+[.m...]. Overrides -e')
	parser.add_argument('-c', '--crop', type=str, help='Output crop, as per ffmpeg\'s crop filter specs (i.e., out_w:out_h:x:y)')
	parser.add_argument('-r', '--rotate', dest='rotate', action='store_true', help='Rotate output 270 degrees clockwise (useful for Genymotion)')

	return parser.parse_args()

def gif_path(path):
  return splitext(path)[0] + '.gif'

def get_palette_path():
    try:
        palette_file = tempfile.NamedTemporaryFile()
        return palette_file.name + '.png'
    finally:
        palette_file.close()

def insert_before_output_path(args, elements):
	index = args.index('-y')
	return args[:index] + elements + args[index:]

look_for_ffmpeg_or_abort()

args = parse_cli_arguments()

input_path = args.video
output_path = gif_path(input_path) if args.outfile is None else args.outfile

fps = args.fps

dw = args.desired_width
dh = args.desired_height

s = args.start_time
e = args.end_time
d = args.duration
c = args.crop

if args.rotate:
	rotate_filters = 'transpose=2,'
else:
    rotate_filters = ""

if c is not None:
	crop_filter = "crop={crop},".format(crop = c)
else:
	crop_filter = ""

filters = "{rotate}{crop}fps={fps},scale={dw}:{dh}:flags=lanczos".format(rotate = rotate_filters, crop = crop_filter, fps = fps, dw = dw, dh = dh)

palette_filters = "{filters},palettegen".format(filters = filters)
palette_path = get_palette_path()

output_filters = "{filters} [x]; [x][1:v] paletteuse".format(filters = filters)

ffmpeg_args_palette = ['ffmpeg',
		'-v', 'warning',
		'-i', input_path,
		'-vf', palette_filters,
		'-y', palette_path]
ffmpeg_args_gif = ['ffmpeg',
		'-v', 'warning',
		'-i', input_path,
		'-i', palette_path,
		'-lavfi', output_filters,
		'-y', output_path]

if s != -1:
	ffmpeg_args_gif = insert_before_output_path(ffmpeg_args_gif, ["-ss", str(s)])

if e != -1:
	ffmpeg_args_gif = insert_before_output_path(ffmpeg_args_gif, ["-to", str(e)])

if d != -1:
	ffmpeg_args_gif = insert_before_output_path(ffmpeg_args_gif, ["-t", str(d)])

print("First pass: extracting colour palette, hang tight...")
subprocess.call(ffmpeg_args_palette)

print("Second pass: converting that nice video into a sweet, high quality gif...")
subprocess.call(ffmpeg_args_gif)

print("Done! Now go and show off to your friends and colleagues")

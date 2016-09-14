"""
Copyright (c) 2016, Gavin Greene
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project.

This script generates 1 of several formats:
Cue foramt
see: https://en.wikipedia.org/wiki/Cue_sheet_(computing)

audacity label format:

The format looks like this:
0.450000	0.450000	point label
1.400000	3.100000	region label
4.150000	4.150000	Question 1

The first column has the start time in seconds, the second column has the end time, and the third column has the name of the label. Start time and end time are identical for a point label. Values are separated by tab characters (which will often appear as an arrow in text editors, as shown above).

from
http://manual.audacityteam.org/man/importing_and_exporting_labels.html


"""
import sys, os
import datetime

OVERWRITE_OUT_FILE = True


#
# helper functions
#
def parse_track_time(time_str):
	"""
	accepts a: time in "HH:MM:SS" format
	returns total seconds
	"""
	h, m, s = time_str.split(':')
	return int(h) * 3600 + int(m) * 60 + int(s)


#
# audaicty format ( default ) 
#
def audacity_track_format(track_start_seconds, track_end_seconds, track_name):
	join_data = []
	join_data.append(str(float(track_start_seconds)))
	join_data.append(str(float(track_end_seconds)))
	join_data.append(track_name)
	ret_str = '\t'.join(join_data)
	return ret_str

def generate_audacity_file(in_file_path, out_file_path):
	print "parsing file {}".format(in_file_path)
	last_track_start_time = None
	track_start_time = None
	last_track_name = None
	track_name = None
	
	with open(in_file_path, 'r') as in_file, open(out_file_path, 'w') as out_file:
		for idx, line in enumerate(in_file):
			#first 8 are time, ex: 04:02:21
			track_time = line[:8]
			# 10 - EOL is track name, ex: Above & Beyon - Counting Down The Days (Faux Tales Remix)
			last_track_name = track_name
			track_name = line[9:].strip(' ').strip('\n')
			
			last_track_start_time = track_start_time
			track_start_time = parse_track_time(track_time)
			
			if last_track_start_time is not None:
				# current start time is the last track's end time
				# write out last entry
				out_file.write((audacity_track_format(last_track_start_time, track_start_time ,last_track_name)))
				out_file.write('\n')
	print "output file written to {}".format(out_file_path)

#
# Main & arg handling
#
def main(in_file_path, out_file_path):
	if not os.path.isfile(in_file_path):
		print "Error! path: {} is not a file!".format(in_file_path)
		sys.exit(1)	
	if os.path.isfile(out_file_path):
		if OVERWRITE_OUT_FILE:
			os.remove(out_file_path)
		else:		
			print "Error! output file already exists, please remove"
			print out_file_path
			sys.exit(1)
	generate_audacity_file(in_file_path, out_file_path)



if __name__ == "__main__":
	usage_str = "invalid usage:\nmp3_split_parse.py <in_file> <out_file>"
	usage_str += "\nin_file should look like this:\n"
	usage_str += "<time> <name of song>\n"
	usage_str += "Example:\n"
	usage_str += "00:17:14 Konec - The Void (ft. Anna Yvette)"
	
	if len(sys.argv) < 2:
		print usage_str
		sys.exit(1)
	in_file_path = sys.argv[1]

	if len(sys.argv) == 2:
		out_file_path = sys.argv[1] + ".txt"
	else:
		out_file_path = sys.argv[2]
		# XXX Hack
		if "--force" in sys.argv:
			OVERWRITE_OUT_FILE = True

	main(in_file_path, out_file_path)
	
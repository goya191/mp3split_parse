# mp3split_parse
Simple script to generate a splitpoint file from a different format

requires python 2.x

format:

HH:MM:SS <track name>
or
MM:SS <track name>

Steps:
save track information in one of the above formats
run mp3split_parse against track file, which will generate a out.txt file

open up audacity
file->import->audio
	specify audio file
file->import->labels
	specify generated out.txt file

file->export multiple
	specify output directory and format.

resulting tracks will be split by label

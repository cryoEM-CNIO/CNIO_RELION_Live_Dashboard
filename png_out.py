#!/usr/bin/env python

import sys
import argparse
import os
import starfile

"""VARIABLES >>>"""
print('running ...')


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output" , "--o", help = "output folder")
parser.add_argument("-i", "--in_mics", help = "input CTF micrograph starfile")
args, unknown = parser.parse_known_args()

inargs=args.in_mics
outargs=args.output

# Parse corrected_micrographs.star
print('parsing STAR file...')

starf_df = starfile.read(inargs)
apix = float(starf_df['optics']['rlnMicrographPixelSize'])
micrographs = starf_df['micrographs']
motion = micrographs['rlnMicrographName']
ctf = micrographs['rlnCtfImage']

print('writing pngs...')

# Launching relion_image_handler to produce PNG files
for i in motion:
    os.system(str('if test -f \"'+i[:-3]+'png\"; then continue; else `which relion_image_handler` --i '+i+ ' --o '+i[:-3]+'png --angpix '+str(apix)+' --rescale_angpix '+str(apix*5)+' --sigma_contrast 6 --lowpass 10; fi'))

for i in ctf:
    os.system(str('if test -f \"'+i[:-7]+'png\"; then continue; else `which relion_image_handler` --i '+i+' --o '+i[:-7]+'png; fi'))
#   os.system(str('if test -f \"'+i[:-7]+'png\"; then continue; else `which relion_image_handler` --i '+i+ ' --o '+i[:-7]+'png --angpix '+str(apix)+' --rescale_angpix '+str(apix*1)+'; fi'))

print('done!')

f=open(outargs+"RELION_JOB_EXIT_SUCCESS","w+")
f.close()

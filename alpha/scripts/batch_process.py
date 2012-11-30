"""
script to batch process youtube videos from an input file
"""

"""
usage:
    python batch_process.py <input_filename>

example:
    python batch_process.py ../assets/youtube_vids.txt
"""
import sys
import os
def main(input_filename):
    urlsFile = open(input_filename,"r")
    for url in urlsFile:
        os.system("python ./get_vid.py {}".format(url))


if __name__ =='__main__':
    try:
        filename = sys.argv[1]
    except:
        print usage
        sys.exit(-1)
    main(filename)


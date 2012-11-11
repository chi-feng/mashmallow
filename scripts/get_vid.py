"""
Script to download youtube video, analyze and export beat/bar info, and other analysis
Saves video as "<output_name>.mpg"
Saves beat/bar analysis as "<output_name>_slices.json"
Saves track analysis as "<output_name>_info.json"
"""

usage = """
Usage:
    python get_vid.py <video_url>

Example:
    python get_vid.py http://www.youtube.com/watch?v=FGBhQbmPwH8

Output:
    in directory ../assets/FGBhQbmPwH8
    FGBhQbmPwH8.mpg
    FGBhQbmPwH8.mp3
    FGBhQbmPwH8_slices.json
    FGBhQbmPwH8_info.json
"""
import sys
import echonest.audio as audio
import echonest.video as video
import os
import errno

def mkdir(directory):
    """
    Makes directory if not already created
    """
    try:
        os.makedirs(directory)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

def main(input_filename):
    output_filename = input_filename.split("=",1)[1]
    output_dir = "../assets/{}/".format(output_filename)
    mkdir(output_dir)

    #Download youtube video
    youtube_seq = video.loadavfromyoutube(input_filename)

    #Save video
    #youtube_seq.save(output_dir+output_filename+".mpg")

    #Save audio
    youtube_seq.audio.encode(output_dir+output_filename+".mp3")

    #Make output json for slices
    filename = output_dir + output_filename + "_slices.json"
    slices = open(filename, "w")
    slices.write('{ \n\t "bars":[ \n')
    #only get the audio part
    av_audio = youtube_seq.audio
    #write bars
    for bar in av_audio.analysis.bars:
        slices.write('\t\t{\n')
        slices.write('\t\t\t"start:"{},\n'.format(bar.start))
        slices.write('\t\t\t"duration:"{},\n'.format(bar.duration))
        slices.write('\t\t}\n')
    slices.write('\t]\n')
    slices.write('\t "beats":[ \n')

    #Write beats
    for beat in av_audio.analysis.beats:
        slices.write('\t\t{\n')
        slices.write('\t\t\t\"start:\":{},\n'.format(beat.start))
        slices.write('\t\t\t\"duration:\":{},\n'.format(beat.duration))
        slices.write('\t\t}\n')
    slices.write('\t]\n')
    slices.write('};\n')
    slices.close()

    #write info
    filename = output_dir + output_filename + "_info.json"
    info = open(filename, "w")
    key = av_audio.analysis.key['value']
    tempo = av_audio.analysis.tempo['value']
    duration = av_audio.analysis.duration
    time_signature = av_audio.analysis.time_signature['value']
    info.write('{"info":{\n\t')
    info.write('"key":{0}, \n\t"tempo":{1},\n\t"duration":{2},\n\t"time_signature":{3}'
                    .format(key, tempo, duration, time_signature))
    info.write('\n}\n}')
    info.close()


if __name__ == '__main__':
    try:
        input_filename = sys.argv[1]
    except:
        print usage
        sys.exit(-1)
    main(input_filename)

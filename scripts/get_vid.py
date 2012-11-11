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
import json

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
    #only get the audio part
    av_audio = youtube_seq.audio
    #make list of bars
    bars = []
    for bar in av_audio.analysis.bars:
        bars.append({'start':bar.start, 'duration':bar.duration})
    beats = []
    for beat in av_audio.analysis.beats:
        beats.append({'start':beat.start, 'duration':beat.duration})
    json.dump({"bars":bars,"beats":beats}, slices, sort_keys=True, indent=4)
    slices.close()

    #write info
    filename = output_dir + output_filename + "_info.json"
    info = open(filename, "w")
    key = av_audio.analysis.key['value']
    tempo = av_audio.analysis.tempo['value']
    duration = av_audio.analysis.duration
    time_signature = av_audio.analysis.time_signature['value']
    json.dump({"key":key, "tempo":tempo,
                "duration":duration, "time_signature":time_signature}, info,
                sort_keys = True, indent=4)
    info.close()


if __name__ == '__main__':
    try:
        input_filename = sys.argv[1]
    except:
        print usage
        sys.exit(-1)
    main(input_filename)

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
from PIL import Image

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

    #Save audio
    youtube_seq.audio.encode(output_dir+output_filename+".mp3")

    #Make output json for slices
    filename = output_dir + output_filename + "_slices.json"
    slices = open(filename, "w")
    #separate variables for video and audio part
    av_video = video.ImageSequence(youtube_seq.video)
    av_audio = youtube_seq.audio

    beats = []
    frameLocs = []
    masterWidth = 10000
    masterHeight = 10000
    for beat in av_audio.analysis.beats:
        #pull thumbnail for beat beginning and halfway through beat
        index1 = av_video.indexvoodo(beat)
        #index2 = av_video.indexvoodo(beat.start+0.5*beat.duration)
        #av_video.renderframe(index1,output_dir+"frames/")
        frameLoc = av_video.files[int(index1.start*av_video.settings.fps)]
        frame = Image.open(frameLoc)
        frame.load()
        frameLocs.append(frameLoc)
        beats.append({'start':beat.start, 'duration':beat.duration})
    json.dump({"beats":beats}, slices, sort_keys=True, indent=4)
    slices.close()
    final_image = Image.new("RGB", (10000, 10000))
    xOffset = 0
    yOffset = 0
    width = 0
    height = 0
    for frameLoc in frameLocs:
        temp_frame = Image.open(frameLoc)
        temp_frame.thumbnail((145,145))
        temp_frame.load()
        final_image.paste(temp_frame,(xOffset,yOffset))
        width = temp_frame.size[0]
        xOffset += width
        if xOffset > masterWidth:
            xOffset = 0
            height = temp_frame.size[1]
            yOffset += height
        if yOffset > masterHeight:
            raise IndexError("Too many images to fit on canvas")
    final_image.save(output_dir+output_filename+".jpg")

    majDict = {0:"C",1:"C#",2:"D",3:"D#",4:"E",5:"F",
            6:"F#",7:"G",8:"G#",9:"A",10:"A#",11:"B"}
    minDict = {0:"cm",1:"c#m",2:"dm",3:"d#m",4:"em",5:"fm",
            6:"f#m",7:"gm",8:"g#m",9:"am",10:"a#m",11:"bm"}

    #write info
    filename = output_dir + output_filename + "_info.json"
    info = open(filename, "w")
    keycode = av_audio.analysis.key['value']
    mode = av_audio.analysis.mode['value']
    try:
        if mode == 0:
            key = minDict[keycode]
        elif mode == 1:
            key = majDict[keycode]
        else:
            raise
    except:
        key = "unknown"
    tempo = av_audio.analysis.tempo['value']
    duration = av_audio.analysis.duration
    time_signature = av_audio.analysis.time_signature['value']
    json.dump({ "width":width, "height":height, "key":key, "tempo":tempo,
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

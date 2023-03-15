"""
Getting YT videos
"""

import os

from urllib.error import URLError
from pytube import YouTube

import vesputils as vu
from settings import DIRNAME, FFMPEGARGS
from scenecutter import cut_videos


links, iflag = None, None
while not iflag:
    user_input = input("Enter link or list of links divided by whitespace: ")
    links = [i for i in user_input.split() if "youtu" in i]

    if not links:
        vu.msg("Links are invalid. Please try again...")
    else:
        iflag = True

vu.dircheck(DIRNAME)

videos = []

for idx, link in enumerate(links, 1):
    vu.msg(f"Trying to download video {idx} of {len(links)}...")

    yt_streams, sflag = None, None
    while not sflag:
        try:
            yt_streams = YouTube(link).streams
            sflag = True
        except URLError:
            vu.msg("Internet connection problems...")
            vu.msg("Trying again in 5 seconds...")
            vu.countdown(5)

    vurl = yt_streams.filter(adaptive=True).order_by("resolution")[-1].url
    aurl = yt_streams.get_by_itag(18).url
    path = f"./{DIRNAME}/{vu.clear_name(yt_streams[0].title)}.mp4"
    videos.append(path)
    os.system(f'ffmpeg -i "{vurl}" -i "{aurl}" {FFMPEGARGS} "{path}"')

    vu.msg(f"Video {idx} of {len(links)} is done!")

vu.msg("All downloads is done!")
action = input("Do you want to cut videos by scenes? (y/n): ")
if action in "yY":
    cut_videos(videos)

vu.msg("Job is done!")
input("Press any key to exit...")

#!/usr/bin/env python3
# encoding: utf-8
"""
encode mp3 chapter
"""
import eyed3
import sys


def add_next_time(data, musicfile):
    maxlen = len(data) - 1
    for i, line in enumerate(data):
        if i == maxlen:
            data[i][0] = eyed3.id3.frames.StartEndTuple(
                start=data[i][0], end=musicfile.info.time_secs)
        else:
            data[i][0] = eyed3.id3.frames.StartEndTuple(
                start=data[i][0], end=data[i + 1][0])
    return data


def parse_chapters_file(fname):
    chaps = []
    with open(fname, "r") as f:
        for line in f.readlines():
            time, title = line.split()[0], " ".join(line.split()[1:])
            chaps.append([to_millisecs(time), title.strip()])

    return chaps


def add_chapters(fname, chapterfile):
    audio = eyed3.load(fname)
    tag = audio.tag

    chaps = parse_chapters_file(chapterfile)
    chaps = add_next_time(chaps, audio)
    # total_length = int(tag.getTextFrame('TLEN'))

    child_ids = []
    list_of_chapters = []
    for i, c in enumerate(chaps):
        chaptername = "chp{}".format(i).encode("utf-8")
        list_of_chapters.append(chaptername)
        new_chapter = tag.chapters.set(chaptername, c[0])
        new_chapter.sub_frames.setTextFrame(b"TIT2", c[1])
    # print(tag.table_of_contents.get(b"toc"))
    tag.table_of_contents.set(b"toc", child_ids=list_of_chapters)
    tag.save()


def to_millisecs(time):
    h, m, s = [float(x) for x in time.split(":")]
    return int(1000 * (s + m * 60 + h * 60 * 60))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert Ultraschall chaptermarks to srt format
"""


class entries():
    def __init__(self, total_length):
        self.total_length = total_length
        self.data = []

    def add(self, entry):
        self.data.append(entry)

    def calculate(self):
        for i in range(0, len(self.data) - 1):
            self.data[i].end = self.data[i + 1].start.replace(".", ",")
        self.data[-1].end = self.total_length.replace(".", ",")

    def write_srt(self, open_file):
        self.calculate()
        for i, e in enumerate(self.data):
            open_file.write("{}\n".format(i + 1))
            open_file.write("{} --> {}\n".format(e.start, e.end))
            open_file.write("{}\n".format(e.text))
            open_file.write("\n")


class entry():
    def __init__(self, text, start, end=None):
        self.text = text
        self.start = start
        self.end = end


def convert_file(from_file, to_file, length_of_file):
    e = entries(length_of_file)
    with open(from_file, "r") as source_file:
        for line in source_file:
            time, text = line.split(" ", 1)
            time = time.replace(".", ",")
            en = entry(text.strip(), time.strip())
            e.add(en)
    with open(to_file, "w") as target_file:
        e.write_srt(target_file)


# if __name__ == '__main__':
#     # Calculate total length:
#     #   MP4Box -info good.m4a 2>&1| grep -i "track duration is"
#     #   We get the result: "02:22:52.731"
#     convertfile(sys.argv[1], sys.argv[2], "02:22:52,731")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tagcroft is a cli to put tags into podcast audio files
"""

import click
import subprocess
import shutil
import dinsort
import yaml as yml
import mp3chapter


def convert_to_m4a_via_ffmpeg(input_filename, output_filename):
    command = [
        'ffmpeg', '-loglevel', 'warning', '-nostdin', '-i', input_filename,
        '-c:a', 'libfdk_aac', '-b:a', '192k', output_filename
    ]
    subprocess.check_output(command)


def convert_to_m4a(input_filename, output_filename):
    convert_to_m4a_via_ffmpeg(input_filename, output_filename)


def convert_to_mp3_via_ffmpeg(input_filename, output_filename):
    command = [
        'ffmpeg', '-loglevel', 'warning', '-nostdin', '-i', input_filename,
        '-b:a', '128k', '-write_xing', '0', output_filename
    ]
    subprocess.check_output(command)


def convert_to_mp3_via_lame(input_filename, output_filename):
    command = [
        'lame', '-h', '-b', '128', '--add-id3v2', input_filename,
        output_filename
    ]
    subprocess.check_output(command)


def convert_to_mp3(input_filename, output_filename):
    convert_to_mp3_via_ffmpeg(input_filename, output_filename)


def write_chapters_mp3(filename_mp3, filename_chapters):
    mp3chapter.add_chapters(filename_mp3, filename_chapters)


def write_chapters_m4a(filename_m4a, filename_chapters):
    command = [
        'SublerCLI', '-source', filename_m4a, '-dest', "temp.m4a", '-chapters',
        filename_chapters
    ]
    rg = subprocess.check_output(command)
    assert rg == b''
    shutil.move("temp.m4a", filename_m4a)


def set_tag(filename, tag, value):
    command = ['kid3-cli', '-c', 'set "{}" "{}"'.format(tag, value), filename]
    rg = subprocess.check_output(command)
    assert rg == b''


def set_picture(filename, picture_filename):
    command = [
        'kid3-cli', '-c', 'set "Picture:{}" ""'.format(picture_filename),
        filename
    ]
    rg = subprocess.check_output(command)
    assert rg == b''


def load_yaml(file):
    data = yml.load(file)
    data['title'] = data['title'].strip()
    data['artist'] = data['artist'].strip()
    data['description'] = data['description'].replace('\n', ' ').strip()
    data['subtitle'] = data['subtitle'].replace('\n', ' ').strip()
    data['url'] = data['url'].strip()
    return data


def generate_output_filename(data):
    name = "{}-{}".format(data['track_number'],
                          dinsort.normalize(
                              data['title'].replace(' ', '-').replace(',', ''),
                              variant=dinsort.VARIANT2))
    return name


@click.command()
@click.option('--m4a/--no-m4a', default=True, help='should a m4a be generated')
@click.option('--mp3/--no-mp3', default=True, help='should a mp3 be generated')
@click.option(
    '--flac/--no-flac',
    default=True,
    help='should a flac be generated (not implemented yet)')
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('yaml_file', type=click.File('r'))
def tag(yaml_file, input_file, m4a=True, mp3=True, flac=True):
    tags = load_yaml(yaml_file)
    output_filename = generate_output_filename(tags)

    if m4a:
        output_filename_m4a = "{}.m4a".format(output_filename)
        m4a = output_filename_m4a
        click.echo("Generating m4a: {}".format(output_filename_m4a))
        convert_to_m4a(input_file, output_filename_m4a)
        click.echo("Writing chapters for {}".format(output_filename_m4a))
        write_chapters_m4a(output_filename_m4a, tags['chapters'])
        click.echo("Writing tags for {}".format(output_filename_m4a))
        set_tag(m4a, "Album Artist", tags['artist'])
        set_tag(m4a, "Artist", tags['artist'])
        set_tag(m4a, "Comment", tags["subtitle"])
        set_tag(m4a, "Date", tags['date'])
        set_tag(m4a, "Description", tags["subtitle"])
        set_tag(m4a, "Genre", "Podcast")
        set_tag(m4a, "Keyword", ", ".join(tags["keywords"]))
        set_tag(m4a, "Long Description", tags["description"])
        set_tag(m4a, "Lyrics", tags["description"])
        set_tag(m4a, "Publisher", tags['artist'])
        set_tag(m4a, "Title", "{} - {}".format(tags['track_number'],
                                               tags['title']))
        set_tag(m4a, "Track Number", tags['track_number'])
        set_tag(m4a, "iTunSMPB", tags["iTunSMPB"])
        set_tag(m4a, "purl", tags["url"])
        set_picture(m4a, tags["picture"])
    if mp3:
        output_filename_mp3 = "{}.mp3".format(output_filename)
        click.echo("Generating mp3: {}".format(output_filename_mp3))
        convert_to_mp3(input_file, output_filename_mp3)
        click.echo("Writing chapters for {}".format(output_filename_mp3))
        write_chapters_mp3(output_filename_mp3, tags['chapters'])
        click.echo("Writing tags for {}".format(output_filename_mp3))
        set_tag(output_filename_mp3, "Artist", tags['artist'])
        set_tag(output_filename_mp3, "Comment", tags["subtitle"])
        set_tag(output_filename_mp3, "Date", tags['date'])
        set_tag(output_filename_mp3, "Genre", "Podcast")
        set_tag(output_filename_mp3, "Lyrics", tags["description"])
        set_tag(output_filename_mp3, "Official Publisher", tags['url'])
        set_tag(output_filename_mp3, "Publisher", tags['artist'])
        set_tag(output_filename_mp3, "Subtitle", tags["subtitle"])
        set_tag(output_filename_mp3, "Title", "{} - {}".format(
            tags['track_number'], tags['title']))
        set_tag(output_filename_mp3, "Track Number", tags['track_number'])
        set_picture(output_filename_mp3, tags["picture"])


if __name__ == '__main__':
    tag()

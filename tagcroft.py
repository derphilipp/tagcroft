#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tagcroft is a cli to put tags into podcast audio files
"""

import click
import subprocess
import yaml as yml


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


@click.group()
def tagcroft():
    pass


def load_yaml(file):
    data = yml.load(file)
    data['title'] = data['title'].strip()
    data['artist'] = data['artist'].strip()
    data['description'] = data['description'].replace('\n', ' ').strip()
    data['subtitle'] = data['subtitle'].replace('\n', ' ').strip()
    data['url'] = data['url'].strip()
    return data


@tagcroft.command()
@click.option(
    '--yaml',
    default='input.yaml',
    type=click.File('r'),
    help='yaml file containing tag infos')
@click.option(
    '--m4a', type=click.Path(exists=True), help='m4a file to be tagged')
@click.option(
    '--mp3', type=click.Path(exists=True), help='mp3 file to be tagged')
def tag(yaml, m4a, mp3):
    tags = load_yaml(yaml)

    if m4a:
        click.echo(m4a)
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
        click.echo(m4a)
        set_tag(mp3, "Artist", tags['artist'])
        set_tag(mp3, "Comment", tags["subtitle"])
        set_tag(mp3, "Date", tags['date'])
        set_tag(mp3, "Genre", "Podcast")
        set_tag(mp3, "Lyrics", tags["description"])
        set_tag(mp3, "Official Publisher", tags['url'])
        set_tag(mp3, "Publisher", tags['artist'])
        set_tag(mp3, "Subtitle", tags["subtitle"])
        set_tag(mp3, "Title", "{} - {}".format(tags['track_number'],
                                               tags['title']))
        set_tag(mp3, "Track Number", tags['track_number'])
        set_picture(mp3, tags["picture"])


if __name__ == '__main__':
    tagcroft()

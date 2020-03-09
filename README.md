# tagcroft
[![Build Status](https://travis-ci.org/derphilipp/tagcroft.svg?branch=master)](https://travis-ci.org/derphilipp/tagcroft)

tagcroft is a cli to put tags into podcast audio files

## Basic setup

Install the application requirements:

- kid3-cli ('kid3' on homebrew)
- lame (for mp3 encoding)
- ffmpeg (for m4a encoding)
- MP4Box (for m4a chapters)

macOS:
```
$ brew cask install kid3
$ brew install MP4Box
$ brew install lame
$ brew tap homebrew-ffmpeg/ffmpeg
$ brew install homebrew-ffmpeg/ffmpeg/ffmpeg --with-fdk-aac
```

Ubuntu Linux:
```
$ sudo apt install python3 lame gpac kid3-cli ffmpeg
```

Install poetry for requirements management:
https://github.com/python-poetry/poetry

Install the required libraries for the project
```
$ poetry install
```

Run the application:
```
$ poetry run ./tagcroft.py AUDIO.wav METADATA.yaml
```

## Name
The tools name comes from "tag" and [Maurice Flitcroft](https://en.wikipedia.org/wiki/Maurice_Flitcroft), the "world's worst golfer" - but played the game anyway.


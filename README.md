# tagcroft
[![Build Status](https://travis-ci.org/derphilipp/tagcroft.svg?branch=master)](https://travis-ci.org/derphilipp/tagcroft)

tagcroft is a cli to put tags into podcast audio files

## Basic setup

Install the application requirements:

- kid3-cli ('kid3' on homebrew)
- lame (for mp3 encoding)
- ffmpeg (for m4a encoding)
- sublercli (for m4a chapters)

macOS:
```
$ brew cask install kid3
$ brew install derphilipp/homebrew-sublercli/sublercli
$ brew install lame
$ brew install ffmpeg --with-fdk-aac
```

Install the python requirements:
```
$ pip install -r requirements.txt
```

Run the application:
```
$ python tagcroft.py AUDIO.wav METADATA.yaml
```


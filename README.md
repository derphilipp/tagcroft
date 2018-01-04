# tagcroft

tagcroft is a cli to put tags into podcast audio files

## Basic setup

Install the application requirements:

- kid3-cli ('kid3' on homebrew)
- sublercli

macOS:
```
$ brew cask install kid3
$ brew install derphilipp/homebrew-sublercli/sublercli
```

Install the python requirements:
```
$ pip install -r requirements.txt
```


Run the application:
```
$ python -m tagcroft --help
```

To run the tests:
```
    $ pytest
```

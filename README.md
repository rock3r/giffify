# giffify

>Life is too short for crappy GIFs

A two-pass, high quality video-to-animated-GIF converter script that harnesses `ffmpeg` to do the dirty work.
Works on both Linux and macOS.

## Setup and usage

1. Copy the version you prefer (Python or Bash) to your computer, and make it executable. For example:

  ```bash
  $ chmod a+x giffify.py
  ```
2. Make sure you have installed `ffmpeg` and you have it on your `PATH`. Easiest way is to use a package manager. On macOS, for example, using [Homebrew](http://brew.sh/):

  ```bash
  $ brew install ffmpeg
  ```

3. Then simply use it to convert movies. It can be as simple as:

  ```bash
  $ giffify.py my-video.mp4
  ```

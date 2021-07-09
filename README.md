# SharkTop

A Python Curses-based UI for GstShark

FPS Panel                  | QueueLevel Panel
:-------------------------:|:-------------------------:
![](image/fps.png)         | ![](image/queue.png)

## Notice

This is a personal project in the development phase. I'll be happy to read your bug-reports, issues, suggestions, or feature requests in the issues section.

## How to install

1. Install GStreamer and GstShark

Use dockerfile or refer to the instructions inside dockerfile for standalone installation

```bash
docker build -f dockerfile_gstreamer_gstshark_x86 -t sharktop .

docker run -it --rm -v $(pwd):/src sharktop bash
```

2. Install sharktop

install by cloning:
```bash
git clone https://github.com/sandstorm12/SharkTop.git sharktop
cd sharktop
python3 -m pip install sharktop
```

install directly using pip:
```bash
python3 -m pip install git+https://github.com/sandstorm12/SharkTop.git
```

## How to use

```bash
sharktop [pipeline or pipeline launching code]

sharktop gst-launch-1.0 videotestsrc ! fakesink sync=True

sharktop gst-launch-1.0 uridecodebin uri="rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov" ! queue ! videoconvert ! fakesink sync=True

sharktop gst-launch-1.0 uridecodebin uri="rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov" ! queue ! videoconvert ! fakesink sync=True -p "queue|videoconvert"

sharktop python run_pipeline.py
```

## Issues and future work
1. Install sharktop inside the dockerfile by default
2. A serious refactor is required
3. Scrollable pipeline description
4. Add more tracers
5. Add images to the readme
6. Sort the lists
7. Upload to pypi

## Contributors
1. Hamid Mohammadi <sandstormeatwo@gmail.com>

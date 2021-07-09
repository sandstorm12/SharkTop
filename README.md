# SharkTop

A Python Curses-based UI for GstShark

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
git clone https://github.com/sandstorm12/GstShark_Curses_UI.git sharktop
cd sharktop
python3 -m pip install sharktop
```

install directly using pip:
```bash
python3 -m pip install git+https://github.com/sandstorm12/GstShark_Curses_UI.git
```

## How to use

```bash
sharktop [pipeline]

sharktop gst-launch-1.0 videotestsrc ! fakesink sync=True

sharktop gst-launch-1.0 videotestsrc ! videoconvert ! autovideosink sync=True

sharktop gst-launch-1.0 videotestsrc ! queue ! videoconvert ! videoscale ! autovideosink sync=True -p "queue|videoscale"
```


## Issues and future work
1. Install sharktop inside the dockerfile by default
2. A serious refactor is required
3. Scrollable pipeline discription
4. Add more tracers
5. Add images to the readme
6. Sort the lists

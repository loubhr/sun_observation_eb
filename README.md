# Sun Observation with an Event-based Camera - WIP

This project is still in progress (I am in the last six months of my PhD, so I have much less time for side projects!)

## Why this is interesting

Several works have shown the potential of event-based cameras for space applications. Cladera et al., for example,
recorded a total solar eclipse and showed that event-based cameras can be very useful for this kind of observation.

Here, I mounted an event-based camera on an amateur telescope and recorded some data. Unfortunately, the telescope was not stabilized, so the solar disk is not very clear,
and it is difficult to draw strong conclusions. These measurements should be taken again more carefully.

However, many unidentified objects, which look like space objects, are moving in front of the solar disk. One could try to estimate their trajectory and speed,
or maybe identify them by checking the recording date and time. The value of event-based cameras for object tracking and space situational awareness has already
been shown, for example by Afshar et al.


## Project Overview

This work in progress does not lead to many conclusions yet. At the moment, it mainly reconstructs a time-based map of events.

**Warning:** this project uses the *Prophesee SDK* (*Metavision*). The open-source version is called *OpenEB*. More information is available here:
[OpenEB installation guide](https://docs.prophesee.ai/stable/installation/linux_openeb_with_packages.html#chapter-installation-linux-openeb-with-packages)

## Usage

Example command:

```bash
python3 python/2D_map_fct_time.py -r data/observation_sun_1.raw -o data/
```

## References

```bibtex
@InProceedings{Cladera_2025_CVPRW,
	author    = {Cladera*, Fernando and Chaney*, Kenneth and Pritchard, Caroline and Hsieh, M. Ani and Kumar, Vijay and Taylor, Camillo J. and Daniilidis, Kostas},
	title     = {Looking into the Shadow: Recording a Total Solar Eclipse with High-resolution Event Cameras},
	booktitle = {Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR) Workshops},
	month     = {June},
	year      = {2025},
	pages     = {4979-4983}
}

@ARTICLE{Afshar_IEEE_Sensors_Journal,
	author  = {Afshar, Saeed and Nicholson, Andrew Peter and van Schaik, Andre and Cohen, Gregory},
	title   = {Event-Based Object Detection and Tracking for Space Situational Awareness},
	journal = {IEEE Sensors Journal},
    month   = {December},
    year    = {2020}
}
```



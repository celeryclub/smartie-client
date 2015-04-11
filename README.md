# musicbox-lcd

## Additions to the excellent [Pi MusicBox](http://pimusicbox.com/)

This project is intended to work with a [Sure Electronics LCD display](http://store.sure-electronics.com/led/led-display/de-lp14112). Tested on Raspbian.

### Requirements
Additional requirements for Pi MusicBox 0.6 users:
tcl, [github.com/celeryclub/smartie-utils](https://github.com/celeryclub/smartie-utils), and an upgrade to Shairport Sync version 2.3.

### Arguments
-f --format '%title\n%artist\n%album\n'
-e --endscreen '\n\n\n'
-c --clock '     %I:%M:%S %p\n\n\n'

### Example usage
The -u switch runs Python in unbuffered mode in order to flush the output of print() immediately.

```sh
# These examples assume a screen with a height of 4 characters

# Clear the screen when playback ends
python -u ~/musicbox-lcd/ssnc-metadata.py -f '%title\n%artist\n%album\n' -e '\n\n\n' ~/shairport-sync-metadata | tclsh ~/smartie-utils/smartie-tail.tcl -tty /dev/ttyUSB0 -buffer 4

# Show a clock when playback ends
python -u ~/musicbox-lcd/ssnc-metadata.py -f '%title\n%artist\n%album\n' -c '     %I:%M:%S %p\n\n\n' ~/shairport-sync-metadata | tclsh ~/smartie-utils/smartie-tail.tcl -tty /dev/ttyUSB0 -buffer 4
```


On Pi MusicBox 0.6, the default version of Shairport Sync is 2.2. In order to install Shairport Sync 2.3 on MusicBox, run these:

```sh
sudo apt-get update
sudo apt-get install git build-essential libconfig-dev automake
```

Then follow the instructions [here](https://github.com/mikebrady/shairport-sync/tree/2.3). Make sure to switch to the 2.3 branch before configuring and making.

## TODO
* Mpc idle loop for current meta
* If a line is >width, wrap it (only do this for one line)

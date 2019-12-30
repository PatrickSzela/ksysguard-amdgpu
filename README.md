# AMDGPU Monitor for KSysGuard

A Python 3 script that allows user to monitor AMD GPUs in KSysGuard (**AMDGPU driver only**)

![Screenshot](/screenshot.png)

Features:

-   calculates average values of every sensor (looking at you `gpu_busy_percent`)
-   supports multiple GPUs
-   doesn't require any special dependencies
-   no root needed
-   respects `Update interval` set in `Tab properties` in KSysGuard

**NOTE:** Some sensors require `amdgpu.ppfeaturemask=0xffffffff` boot parameter - [more info](https://wiki.archlinux.org/index.php/AMDGPU#Overclocking)

### Requirements

-   AMD GPU using AMDGPU driver
-   Python 3 (tested with 3.8)
-   lm-sensors
-   read permission for files in `/sys/bus/pci/drivers/amdgpu/<PCI ID>/*`

### Available sensors

| Sensor       | Unit |
| ------------ | ---- |
| GPU Usage    | %    |
| GPU Clock    | MHz  |
| GPU Voltage  | mV   |
| VRAM Usage   | MiB  |
| VRAM Clock   | MHz  |
| VRAM Voltage | mV   |
| GTT Usage    | MiB  |
| Temperature  | °C   |
| Power        | W    |
| Fan          | RPM  |
| Fan PWM      |      |

### Available arguments

| Argument | Type  | Description                                                 |
| -------- | ----- | ----------------------------------------------------------- |
| --tick   | float | Time (in sec) how often should the sensor data be collected |

### Usage

After cloning the repository:

1. Add executable permission to `sensor.py` file
2. Open KSysGuard
3. Open `File` -> `Monitor Remote Machine...` and fill the window appropriately:
    1. Host: `AMDGPU` (or whatever you want - it just can't contain any special character or spaces)
    2. Connection type: `Custom command`
    3. Command: `<PATH TO sensor.py> [arguments]`

If everything went OK, new sensors should be available in the [Sensor Browser](https://docs.kde.org/trunk5/en/kde-workspace/ksysguard/the-workspace.html#the-sensor-browser). Then just grab the sensor from the list and drop it in a desired place.

### Issues

Project is still not finished and has only been fully tested on only one machine (Arch Linux, Linux 5.4, 1x RX 580, Python 3.8).

-   If you have a GPU from Vega 20 series, some sensors (or min/max values) might be missing - with these GPUs the driver reports some data in a different way and I don't know (yet) how it should be parsed.
-   If the sensor is missing it's possible that the required file which script reads is missing - please create an Issue.
-   If nothing happens after adding the script in KSysGuard, make sure that the `Host` in `Monitor Remote Machine...` doesn't contains any spaces or special characters.

It's possible to test the script manually by executing it in terminal. Running it should print out:

```
ksysguardd 1.2.0
ksysguardd>
```

1. Now type `monitors` to get list of all available monitors (in `CARD_ID/SENSOR type` format)

```
ksysguardd> monitors
0000:01:00.0/gpu_usage  integer
0000:01:00.0/gpu_clock  integer
[...]
```

2. Now type `CARD_ID/SENSOR?` to get info about specific sensor - it should print out monitor info in `name min max unit` format

```
ksysguardd> 0000:01:00.0/gpu_usage?
GPU Usage       0       100     %
```

3. Now type `CARD_ID/SENSOR` to get current value of the sensor

```
ksysguardd> 0000:01:00.0/gpu_usage
8
```

4. Now repeat steps 2-3 with every other sensors from `monitors` command.

If everything went OK the script is working fine and most likely the problem lies somewhere else. If something went wrong, please create an Issue and describe what's not working.

#### TODO

-   Test with other GPUs
-   Test with more than one GPU
-   Add support for Vega 20 series
-   Add support for Northbridge voltages
-   Add support for non-average values (as separate sensors)
-   Add support for multiple temperature sensors and fans
-   Improve performance and code quality (any pointers are welcome)
-   Add support for more units (if requested)

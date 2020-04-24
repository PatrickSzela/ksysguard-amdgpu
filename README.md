# AMDGPU Monitor for KSysGuard

Python 3 script that allows user to monitor AMD GPUs in KSysGuard (**AMDGPU driver only**)

![Screenshot](/screenshot.png)

### Features

-   calculates average values of every sensor (looking at you `gpu_busy_percent`)
-   supports multiple GPUs
-   detects min and max values of sensors automatically
-   doesn't require any special dependencies
-   no root needed
-   respects `Update interval` set in `Tab properties` in KSysGuard

**NOTE:** Some sensors (notably GPU & VRAM Voltages) require `amdgpu.ppfeaturemask=0xfffd7fff` boot parameter - [more info](https://wiki.archlinux.org/index.php/AMDGPU#Overclocking)

### Requirements

-   AMD GPU using AMDGPU driver
-   Python 3 (tested with 3.8)
-   read permission for files in `/sys/bus/pci/drivers/amdgpu/<PCI_SLOT>/*`

### Available sensors

Based on [Linux Kernel Documentation](https://dri.freedesktop.org/docs/drm/gpu/amdgpu.html#gpu-power-thermal-controls-and-monitoring):

| Sensor                 | Unit |
| ---------------------- | ---- |
| GPU Usage              | %    |
| GPU Clock              | MHz  |
| GPU Voltage            | mV   |
| VRAM Usage             | MiB  |
| VRAM Clock             | MHz  |
| VRAM Voltage           | mV   |
| GTT Usage              | MiB  |
| Temperature            | °C   |
| Power                  | W    |
| Fan                    | RPM  |
| Fan PWM                |      |
| SoC Clock (>= Vega10)  | MHz  |
| DCEF Clock (>= Vega10) | MHz  |
| F Clock (>= Vega20)    | MHz  |

### Available arguments

| Argument  | Type  | Description                                                                                                          |
| --------- | ----- | -------------------------------------------------------------------------------------------------------------------- |
| --tick    | float | Time (in sec) how often should the sensor data be collected                                                          |
| --logging | bool  | Enables logging - use it when something isn't working. Do not use this argument when adding the script to KSysGuard! |

### Usage

1. Make sure the `sensor.py` file has an executable permission
2. Open KSysGuard
3. Open `File` -> `Monitor Remote Machine...` and fill the window appropriately:
    1. Host: `AMDGPU` (or whatever you want)
    2. Connection type: `Custom command`
    3. Command: `<PATH TO sensor.py> [arguments]`

If everything went OK, new sensors should be available in the [Sensor Browser](https://docs.kde.org/trunk5/en/kde-workspace/ksysguard/the-workspace.html#the-sensor-browser). Then just grab the sensor from the list and drop it in a desired place.

_HINT:_ If the `Monitor Remote Machine...` is missing, create new tab.

### Issues

-   If you have a GPU from Vega 20 series or later, `VRAM Voltage` sensor and `GPU Voltage` min and max values might be missing - with these GPUs the driver reports some data (`pp_od_clk_voltage` to be exact) in a different way and I haven't figured out (yet) a way how to detect them. Check [Issue](https://github.com/PatrickSzela/ksysguard-amdgpu/issues/1) if you would like to help!
-   If a sensor is missing or its values are `-1` or `0`, it means that the script failed to read and/or parse a file - please read [Testing](#Testing) and include the output (with errors from `--logging` argument) when creating an Issue.

### Testing

It's possible to test the script manually by executing it in the terminal. If you do it with a `--logging` argument, you might see some errors get printed out after running it. Include them when creating an Issue!

Either way, the script now should print out:

```
ksysguardd 1.2.0
ksysguardd>
```

1. Type `monitors` to get list of all available monitors (in `PCI_SLOT/SENSOR` format)

```
ksysguardd> monitors
0000:01:00.0/gpu_usage  integer
0000:01:00.0/gpu_clock  integer
[...]
```

2. Now type `PCI_SLOT/SENSOR?` to get info about a specific sensor - it should print out monitor info in a `name min max unit` format. This command is required for the one from next step to work!

```
ksysguardd> 0000:01:00.0/gpu_usage?
GPU Usage       0       100     %
```

3. Now type `PCI_SLOT/SENSOR` to get current value of the sensor

```
ksysguardd> 0000:01:00.0/gpu_usage
8
```

### TODO

-   Add support for Vega 20 series ([Issue](https://github.com/PatrickSzela/ksysguard-amdgpu/issues/1))
-   Add support for Northbridge voltages ([Issue](https://github.com/PatrickSzela/ksysguard-amdgpu/issues/2))
-   Add support for non-average values
-   Add support for multiple temperature and fan sensors
-   Add support for multiple hwmons (I'm not sure if it's even needed)
-   Improve performance and code quality (any pointers are welcome)
-   Add support for more units (if requested)

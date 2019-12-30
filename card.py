import threading
import os
import io
from typing import Mapping, Any
from monitor import Monitor
from monitor.gpu_clock import GPUClockMonitor
from monitor.gpu_voltage import GPUVoltageMonitor
from monitor.vram_clock import VRAMClockMonitor
from monitor.vram_voltage import VRAMVoltageMonitor

# TODO: automatically detect multiple fans and temperature sensors
# TODO: add average option to monitor (which should be collected by Collector)
# TODO: figure out voltage_northbridge min and max
# TODO: Fan PWM swap to %?
# TODO: add power_dpm_force_performance_level?

# Info about sensors: https://dri.freedesktop.org/docs/drm/gpu/amdgpu.html#gpu-power-thermal-controls-and-monitoring
monitors = {
    "gpu_usage": {"nice_name": "GPU Usage", "min": 0, "max": 100, "value": "./gpu_busy_percent", "unit": "%"},
    "gpu_clock": {"nice_name": "GPU Clock", "min": "./pp_dpm_sclk", "max": "./pp_dpm_sclk", "value": "./hwmon/hwmon0/freq1_input", "unit": "MHz", "class": GPUClockMonitor},
    "gpu_voltage": {"nice_name": "GPU Voltage", "min": "./pp_od_clk_voltage", "max": "./pp_od_clk_voltage", "value": "./hwmon/hwmon0/in0_input", "unit": "mV", "class": GPUVoltageMonitor},
    "vram_usage": {"nice_name": "VRAM Usage", "min": 0, "max": "./mem_info_vram_total", "value": "./mem_info_vram_used", "unit": "MiB"},
    "vram_clock": {"nice_name": "VRAM Clock", "min": "./pp_dpm_mclk", "max": "./pp_dpm_mclk", "value": "./hwmon/hwmon0/freq2_input", "unit": "MHz", "class": VRAMClockMonitor},
    "vram_voltage": {"nice_name": "VRAM Voltage", "min": "./pp_od_clk_voltage", "max": "./pp_od_clk_voltage", "value": "./pp_dpm_mclk", "unit": "mV", "class": VRAMVoltageMonitor},
    "gtt_usage": {"nice_name": "GTT Usage", "min": 0, "max": "./mem_info_gtt_total", "value": "./mem_info_gtt_used", "unit": "MiB"},
    "temperature": {"nice_name": "Temperature", "min": 0, "max": "./hwmon/hwmon0/temp1_crit", "value": "./hwmon/hwmon0/temp1_input", "unit": "°C"},
    "power": {"nice_name": "Power", "min": "./hwmon/hwmon0/power1_cap_min", "max": "./hwmon/hwmon0/power1_cap_max", "value": "./hwmon/hwmon0/power1_average", "unit": "W"},
    "fan": {"nice_name": "Fan", "min": "./hwmon/hwmon0/fan1_min", "max": "./hwmon/hwmon0/fan1_max", "value": "./hwmon/hwmon0/fan1_input", "unit": "RPM"},
    "fan_pwm": {"nice_name": "Fan PWM", "min": "./hwmon/hwmon0/pwm1_min", "max": "./hwmon/hwmon0/pwm1_max", "value": "./hwmon/hwmon0/pwm1", "unit": ""},
}


class Card:
    """Class containing everything related to cards"""

    def __init__(self, path: str):
        self.path = path
        self.monitors: Mapping[str, Monitor] = self.detect_monitors()

    def detect_monitors(self) -> Mapping[str, Monitor]:
        """Detect possible monitors """
        detected_monitors: Mapping[str, Monitor] = {}

        for monitor_name, monitor_data in monitors.items():
            if not monitor_name in detected_monitors.keys():
                try:
                    monitor_class = monitor_data["class"] if "class" in monitor_data else Monitor
                    monitor = monitor_class(
                        monitor_name, monitor_data["nice_name"], monitor_data["min"], monitor_data["max"], monitor_data["value"], monitor_data["unit"], self.path)
                except:
                    continue
                else:
                    detected_monitors[monitor_name] = monitor

        return detected_monitors

    def get_value(self, monitor_name: str) -> int:
        """Returns current value of monitor `monitor_name`"""
        if monitor_name in self.monitors:
            return self.monitors[monitor_name].get_value()

    def get_info(self, monitor_name: str) -> str:
        """Returns info about monitor `monitor_name`"""
        if monitor_name in self.monitors:
            return self.monitors[monitor_name].get_info()

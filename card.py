import threading
import os
import io
import logging
from typing import Mapping, Any
from monitor import Monitor
from monitor.list import monitor_list

# TODO: automatically detect multiple fans and temperature sensors
# TODO: add average option to monitor (which should be collected by Collector)
# TODO: figure out voltage_northbridge min and max
# TODO: Fan PWM swap to %?
# TODO: add power_dpm_force_performance_level?


class Card:
    """Class containing everything related to cards"""

    def __init__(self, pci_slot: str, path: str):
        self.pci_slot = pci_slot
        self.path = path
        self.monitors: Mapping[str, Monitor] = self.detect_monitors()

    def detect_monitors(self) -> Mapping[str, Monitor]:
        """Detect possible monitors"""
        detected_monitors: Mapping[str, Monitor] = {}

        for monitor_name, monitor_data in monitor_list.items():
            if not monitor_name in detected_monitors.keys():
                try:
                    monitor_class = monitor_data["class"] if "class" in monitor_data else Monitor
                    monitor = monitor_class(self.pci_slot,
                                            monitor_name, self.path, monitor_data)
                except Exception:
                    logging.warning(
                        f"{self.pci_slot}/{monitor_name}:Failed to create monitor:\n", exc_info=True)
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

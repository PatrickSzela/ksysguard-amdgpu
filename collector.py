import threading
from typing import List, Mapping
from card import Card


class Collector(threading.Thread):
    """Class used to collect data over time"""

    def __init__(self, card: Card, tick: float, stop_event: threading.Event):
        threading.Thread.__init__(self)
        self.card = card
        self.tick = tick
        self.stop_event = stop_event
        self.lock = threading.Lock()
        self.data: Mapping[str, Mapping[str, int]] = {}
        self.requested_monitors: List[str] = []

    def run(self) -> None:
        """Starts the loop"""
        self.loop()

    def loop(self) -> None:
        """Collector's loop that collects monitors value over time"""
        while not self.stop_event.wait(self.tick):
            with self.lock:
                for monitor in self.requested_monitors:
                    self.data[monitor]["counter"] += 1
                    self.data[monitor]["value"] += self.card.get_value(monitor)

    def get_value(self, monitor_name: str) -> int:
        """Returns average of collected values (and resets it)"""
        if not monitor_name in self.requested_monitors:
            return -1

        self.lock.acquire()

        count = self.data[monitor_name]["counter"]
        value = self.data[monitor_name]["value"]
        self.data[monitor_name]["counter"] = 0
        self.data[monitor_name]["value"] = 0

        self.lock.release()

        # In case if the same command is called when collector can't collect enough data, return prev value
        if count == 0:
            return self.data[monitor_name]["prev_value"]

        calculated = int(round(value / count))
        self.data[monitor_name]["prev_value"] = calculated
        return calculated

    def stop(self) -> None:
        """Stops the loop"""
        self.stop_event.set()

    def request_monitor(self, monitor_name: str) -> None:
        """Adds monitor `monitor_name` to the collector to be collected over time"""
        if not monitor_name in self.requested_monitors and monitor_name in self.card.monitors:
            self.requested_monitors.append(monitor_name)
            self.data[monitor_name] = {}
            self.data[monitor_name]["counter"] = 0
            self.data[monitor_name]["value"] = 0
            self.data[monitor_name]["prev_value"] = 0

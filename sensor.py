#!/usr/bin/env python3

import threading
import os
import argparse
import logging
from typing import Mapping
from card import Card
from monitor import Monitor
from collector import Collector

amdgpu_dir = "/sys/bus/pci/drivers/amdgpu"
pci_dir = "/sys/devices/pci"
tick = 0.01
cards: Mapping[str, Card] = {}
collectors: Mapping[str, Collector] = {}


def detect_cards(driver_path: str, pci_path: str) -> Mapping[str, str]:
    """Returns dictionary (`PCI slot`, `real path`) of all detected cards by walking through every device registered to the driver (directories in `driver_path`) and checking whether it's a PCI device (target of these directories starts with `pci_path`).
    """
    cards = {}

    if os.path.isdir(driver_path):
        for directory in next(os.walk(driver_path))[1]:
            target = os.path.realpath(os.path.join(driver_path, directory))
            if target and target.startswith(pci_path):
                cards[directory] = target

    return cards


def print_monitors():
    """Prints all detected monitors of every card"""
    for pci_slot, card_data in cards.items():
        for monitor in card_data.monitors:
            print(f"{pci_slot}/{monitor}\tinteger")


def print_info(pci_slot: str, monitor_name: str) -> None:
    """Prints info about monitor named `monitor_name` running on a card with `pci_slot`"""
    if pci_slot in cards:
        print(cards[pci_slot].get_info(monitor_name))


def print_value(pci_slot: str, monitor_name: str) -> None:
    """Prints current value of a monitor named `monitor_name` running on a card with `pci_slot`"""
    if pci_slot in cards:
        print(cards[pci_slot].get_value(monitor_name))


def print_collector_value(collector: Collector, monitor: str) -> None:
    """Prints average value (collected by `collector`) of a `monitor`"""
    print(collector.get_value(monitor))


def on_exit(collectors: Mapping[str, Collector]):
    """Stuff to do when exiting"""
    for collector in collectors.values():
        collector.stop()
        collector.join()


def main() -> int:
    """Main loop"""
    detected_cards = detect_cards(amdgpu_dir, pci_dir)
    for pci_slot, card in detected_cards.items():
        cards[pci_slot] = Card(pci_slot, card)

    stop = threading.Event()

    print("ksysguardd 1.2.0")

    while True:
        try:
            command = input("ksysguardd> ").strip()
        except KeyboardInterrupt:
            on_exit(collectors)
            return 0
        else:
            if command == "monitors":
                print_monitors()
            elif command == "quit":
                on_exit(collectors)
                return 0
            else:
                try:
                    info = command.endswith("?")
                    command = command.split("/")
                    pci_slot = command[0]
                    monitor = command[1][:-1] if info else command[1]
                except:
                    logging.warning("Unrecognized command")
                else:
                    if not pci_slot in cards:
                        logging.warning(f"Card \"{pci_slot}\" not found")
                        continue

                    if not monitor in cards[pci_slot].monitors:
                        logging.warning(
                            f"Monitor \"{monitor}\" not found in card \"{pci_slot}\"")
                        continue

                    if not pci_slot in collectors:
                        collectors[pci_slot] = Collector(
                            cards[pci_slot], tick, stop)
                        collectors[pci_slot].start()

                    if info:
                        collectors[pci_slot].request_monitor(monitor)
                        print_info(pci_slot, monitor)
                    else:
                        print_collector_value(collectors[pci_slot], monitor)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AMDGPU sensor for KSysGuard")
    parser.add_argument("--tick", dest="tick", type=float, default=tick,
                        help="time (in sec) how often should the sensor data be collected")
    parser.add_argument("--logging", dest="logging", action="store_true",
                        help="enables logging - use when something isn't working. Do not use this argument when adding the script to KSysGuard!")
    arguments = parser.parse_args()
    tick = arguments.tick

    if not arguments.logging:
        # disable logging when running in KSysGuard
        logging.disable(logging.CRITICAL)

    main()

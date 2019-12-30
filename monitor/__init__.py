import os
import io
from typing import Union

# TODO: set min, max and value when monitor is requested
# TODO: instead of reading file directly use watch?


class Monitor:
    """Class containing everything related to monitoring"""

    def __init__(self, name: str, nice_name: str, min: Union[str, int], max: Union[str, int], value: Union[str, int], unit: str, path: str):
        self.name = name
        self.path = path
        self.unit = unit
        self.nice_name = nice_name

        # min and max won't be changing on runtime so no need to constantly reread them
        self.min = self.parse_unit(self.parse_value(
            self.handle_file(min), "min"), unit)
        self.max = self.parse_unit(self.parse_value(
            self.handle_file(max), "max"), unit)

        # open file so current value can be continously read. If failed the monitor will be deleted
        try:
            self.value = self.open_file(value)
        except FileNotFoundError as e:
            self.value = None
            # pass exception upward
            raise

    def __del__(self):
        self.close_file(self.min)
        self.close_file(self.max)
        self.close_file(self.value)

    def open_file(self, file: str) -> io.IOBase:
        """Opens `file` for reading"""
        return open(os.path.join(self.path, file), "r")

    def read_file(self, file: io.IOBase) -> str:
        """Reads content of the `file`"""
        if isinstance(file, io.IOBase) and not file.closed:
            file.seek(0, 0)
            return file.read()

    def close_file(self, file: io.IOBase) -> None:
        """Closes `file`"""
        if isinstance(file, io.IOBase) and not file.closed:
            file.close()

    def handle_file(self, file) -> Union[int, str]:
        """Reads content of the `file`, automatically handling opening and closing it. If the file is not a path, returns it. If file doesn't exists, returns `-1`."""
        try:
            f = self.open_file(file)
            value = self.read_file(f)
            self.close_file(f)
            return value
        except FileNotFoundError:
            # do not fail when file doesn't exists - min and max values aren't required for monitor to work
            return -1
        except:
            return file

    def parse_value(self, value: str, type: str) -> int:
        """Parses the `value` depending on `type`"""
        try:
            return int(value)
        except:
            return -1

    # TODO: figure a better way to handle unit
    def parse_unit(self, value: int, unit: str) -> int:
        """Converts `value` to specified `unit`"""
        if unit == "°C":
            value = round(value / 1000)
        elif unit == "MiB":
            value = round(value / 1048576)
        elif unit == "MHz":
            value = round(value / 1000000)
        elif unit == "W":
            value = round(value / 1000000)
        return value

    def get_value(self) -> int:
        """Returns (already parsed) current value"""
        return self.parse_unit(self.parse_value(self.read_file(self.value), "value"), self.unit)

    def get_info(self) -> str:
        """Returns info about monitor (name, min, max, unit)"""
        return f"{self.nice_name}\t{self.min}\t{self.max}\t{self.unit}"

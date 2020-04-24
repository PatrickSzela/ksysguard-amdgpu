import os
import io
import logging

# TODO: instead of reading file directly use watch?


class Monitor:
    """Class containing everything related to monitoring"""

    def __init__(self, card_pci_slot: str, name: str, path: str, data: object):
        self.card_pci_slot = card_pci_slot
        self.name = name
        self.path = path
        self.nice_name = data["nice_name"]
        self.data = data
        self.min = data["min"]
        self.max = data["max"]
        self.value = data["value"]
        self.unit = data["unit"]

        self.file_value = self.open_file(data["value"])

        # test time
        self.get_info()
        self.try_get_value("value")

    def __del__(self):
        if isinstance(self.value, io.IOBase):
            self.close_file(self.value)

    def open_file(self, file: str) -> io.IOBase:
        """Opens `file` for reading"""
        # TODO: and add support for multiple HWMONs and handle them in a better way
        if "hwmon" in file:
            for directory in next(os.walk(os.path.join(self.path, "hwmon")))[1]:
                if directory.startswith("hwmon"):
                    path = os.path.join(f"hwmon/{directory}", file["hwmon"])
                    break
        else:
            path = file["path"]

        return open(os.path.join(self.path, path), "r")

    def read_file(self, file: io.IOBase) -> str:
        """Reads content of the `file`"""
        file.seek(0, 0)
        return file.read()

    def close_file(self, file: io.IOBase) -> None:
        """Closes `file`"""
        file.close()

    def handle_file(self, file: object) -> str:
        """Reads content of the `file`, automatically handling opening and closing it"""
        f = self.open_file(file)
        value = self.read_file(f)
        self.close_file(f)
        return value

    def parse_value(self, value: str, type: str) -> int:
        """Parses the `value` depending on `type`"""
        return int(value)

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

    def get_value(self, type: str = "value") -> int:
        """Returns (already parsed) value of `type`"""
        if type == "value":
            # "value" can contain only path and the file was already opened in __init__, so just read its contents
            value = self.read_file(self.file_value)
        else:
            value = self.handle_file(
                self.data[type]) if not "value" in self.data[type] else self.data[type]["value"]

        return self.parse_unit(self.parse_value(value, type), self.unit)

    def get_info(self) -> str:
        """Returns info about monitor (name, min, max, unit). If any values fails, it will be set to -1, or if it's required, will throw an exception"""
        min = self.try_get_value("min")
        max = self.try_get_value("max")

        return f"{self.nice_name}\t{min}\t{max}\t{self.unit}"

    def try_get_value(self, type: str):
        """Tries to get a value of `type`. If it fails, will throw an excpetion if the value is required, otherwise returns `0` and prints a warning (if logging is enabled)"""
        try:
            value = self.get_value(type)
            if value == -1:
                file = self.data[type]["path"]
                raise Exception(f"Failed to parse file: {self.path}/{file}")
            return value

        except Exception as e:
            if "required" in self.data[type]:
                raise e
            else:
                logging.warning(
                    f"{self.card_pci_slot}/{self.name}:Failed to get {type} value:\n", exc_info=True)
                return 0

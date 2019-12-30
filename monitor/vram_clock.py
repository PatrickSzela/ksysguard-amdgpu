from monitor import Monitor


class VRAMClockMonitor(Monitor):
    def parse_value(self, value: str, type: str) -> int:
        try:
            if type == "min" or type == "max":
                # Get all performance modes - first line contains min VRAM Clock value (in Mhz) and the last one max value
                idx = -1 if type == "max" else 0
                return int(value.splitlines()[idx].strip().split()[1][:-3]) * 1000000

            return Monitor.parse_value(self, value, type)
        except:
            return -1

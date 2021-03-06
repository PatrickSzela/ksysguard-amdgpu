from monitor import Monitor


class SoCClockMonitor(Monitor):
    def parse_value(self, value: str, type: str) -> int:
        try:
            if type == "min" or type == "max" or type == "value":
                if type == "min":
                    # First line contains min SoC Clock value (in Mhz)
                    idx = 0
                elif type == "max":
                    # Last line contains max SoC Clock value (in Mhz)
                    idx = -1
                elif type == "value":
                    # Get clock based on current SoC state (marked with *)
                    idx = [idx for idx, line in enumerate(
                        value.splitlines()) if "*" in line][0]

                return int(value.splitlines()[idx].strip().split()[1][:-3]) * 1000000

            return Monitor.parse_value(self, value, type)
        except:
            return -1

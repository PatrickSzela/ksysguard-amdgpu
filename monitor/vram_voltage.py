from monitor import Monitor


class VRAMVoltageMonitor(Monitor):
    def parse_value(self, value: str, type: str) -> int:
        try:
            if type == "min" or type == "max":
                idx = -1 if type == "max" else 0

                # split file by OD_
                ods = [line for line in value.split("OD_") if line != '']

                # get values of OD_MCLK
                od_mclk = [line for line in ods if line.startswith("MCLK")][0].splitlines()[
                    1:]

                # extract possible voltages sorted by states
                self.values = [line.split()[-1][:-2] for line in od_mclk]

                return int(self.values[idx])
            elif type == "value":
                # get voltage based on current VRAM state (marked with *)
                idx = [idx for idx, line in enumerate(
                    value.splitlines()) if "*" in line][0]
                return int(self.values[idx])

            return Monitor.parse_value(self, value, type)
        except:
            return -1

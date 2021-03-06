from monitor import Monitor


class GPUVoltageMonitor(Monitor):
    def parse_value(self, value: str, type: str) -> int:
        try:
            if type == "min" or type == "max":
                idx = -1 if type == "max" else 0

                # split file by OD_
                ods = [line for line in value.split("OD_") if line != '']

                # if using >=Vega20
                if "OD_VDDC_CURVE" in value:
                    # get values of OD_VDDC_CURVE
                    od_vddc_curve = [line for line in ods if line.startswith("VDDC_CURVE")][0].splitlines()[
                        1:]

                    # extract possible voltages sorted by states
                    values = [line.split()[-1][:-2] for line in od_vddc_curve]
                else:
                    # get values of OD_SCLK
                    od_sclk = [line for line in ods if line.startswith("SCLK")][0].splitlines()[
                        1:]

                    # extract possible voltages sorted by states
                    values = [line.split()[-1][:-2] for line in od_sclk]

                return int(values[idx])

            return Monitor.parse_value(self, value, type)
        except:
            return -1

from monitor.gpu_clock import GPUClockMonitor
from monitor.gpu_voltage import GPUVoltageMonitor
from monitor.vram_clock import VRAMClockMonitor
from monitor.vram_voltage import VRAMVoltageMonitor
from monitor.soc_clock import SoCClockMonitor
from monitor.dcef_clock import DCEFClockMonitor
from monitor.f_clock import FClockMonitor

# Info about sensors: https://dri.freedesktop.org/docs/drm/gpu/amdgpu.html#gpu-power-thermal-controls-and-monitoring
monitor_list = {
    "gpu_usage": {
        "nice_name": "GPU Usage",
        "min": {"value": 0},
        "max": {"value": 100},
        "value": {
            "path": "gpu_busy_percent",
            "required": True
        },
        "unit": "%"},
    "gpu_clock": {
        "nice_name": "GPU Clock",
        "min": {"path": "pp_dpm_sclk"},
        "max": {"path": "pp_dpm_sclk"},
        "value": {
            "hwmon": "freq1_input",
            "required": True
        },
        "unit": "MHz",
        "class": GPUClockMonitor
    },
    "gpu_voltage": {
        "nice_name": "GPU Voltage",
        "min": {"path": "pp_od_clk_voltage"},
        "max": {"path": "pp_od_clk_voltage"},
        "value": {
            "hwmon": "in0_input",
            "required": True
        },
        "unit": "mV",
        "class": GPUVoltageMonitor
    },
    "vram_usage": {
        "nice_name": "VRAM Usage",
        "min": {"value": 0},
        "max": {"path": "mem_info_vram_total"},
        "value": {
            "path": "mem_info_vram_used",
            "required": True
        },
        "unit": "MiB"
    },
    "vram_clock": {
        "nice_name": "VRAM Clock",
        "min": {"path": "pp_dpm_mclk"},
        "max": {"path": "pp_dpm_mclk"},
        "value": {
            "hwmon": "freq2_input",
            "required": True
        },
        "unit": "MHz",
        "class": VRAMClockMonitor
    },
    "vram_voltage": {
        "nice_name": "VRAM Voltage",
        "min": {
            "path": "pp_od_clk_voltage",
            "required": True
        },
        "max": {
            "path": "pp_od_clk_voltage",
            "required": True
        },
        "value": {
            "path": "pp_dpm_mclk",
            "required": True
        },
        "unit": "mV",
        "class": VRAMVoltageMonitor
    },
    "gtt_usage": {
        "nice_name": "GTT Usage",
        "min": {"value": 0},
        "max": {"path": "mem_info_gtt_total"},
        "value": {
            "path": "mem_info_gtt_used",
            "required": True
        },
        "unit": "MiB"
    },
    "temperature": {
        "nice_name": "Temperature",
        "min": {"value": 0},
        "max": {"hwmon": "temp1_crit"},
        "value": {
            "hwmon": "temp1_input",
            "required": True
        },
        "unit": "°C"
    },
    "power": {
        "nice_name": "Power",
        "min": {"hwmon": "power1_cap_min"},
        "max": {"hwmon": "power1_cap_max"},
        "value": {
            "hwmon": "power1_average",
            "required": True
        },
        "unit": "W"
    },
    "fan": {
        "nice_name": "Fan",
        "min": {"hwmon": "fan1_min"},
        "max": {"hwmon": "fan1_max"},
        "value": {
            "hwmon": "fan1_input",
            "required": True
        },
        "unit": "RPM"
    },
    "fan_pwm": {
        "nice_name": "Fan PWM",
        "min": {"hwmon": "pwm1_min"},
        "max": {"hwmon": "pwm1_max"},
        "value": {
            "hwmon": "pwm1",
            "required": True
        },
        "unit": ""
    },
    "soc_clock": {
        "nice_name": "SoC Clock",
        "min": {"path": "pp_dpm_socclk"},
        "max": {"path": "pp_dpm_socclk"},
        "value": {
            "path": "pp_dpm_socclk",
            "required": True
        },
        "unit": "MHz",
        "class": SoCClockMonitor
    },
    "dcef_clock": {
        "nice_name": "DCEF Clock",
        "min": {"path": "pp_dpm_dcefclk"},
        "max": {"path": "pp_dpm_dcefclk"},
        "value": {
            "path": "pp_dpm_dcefclk",
            "required": True
        },
        "unit": "MHz",
        "class": DCEFClockMonitor
    },
    "f_clock": {
        "nice_name": "F Clock",
        "min": {"path": "pp_dpm_fclk"},
        "max": {"path": "pp_dpm_fclk"},
        "value": {
            "path": "pp_dpm_fclk",
            "required": True
        },
        "unit": "MHz",
        "class": FClockMonitor
    }
}


import platform
import psutil


def get_battery_status():
    """Get the Mac's current battery information."""
    battery = psutil.sensors_battery()

    if battery is None:
        return {"error": "Battery information unavailable"}

    return {
        "percentage": round(battery.percent, 1),
        "charging": battery.power_plugged
    }


def get_system_performance():
    """Get current CPU and RAM usage."""
    memory = psutil.virtual_memory()

    return {
        "cpu_usage_percent": psutil.cpu_percent(interval=0.5),
        "ram_usage_percent": memory.percent,
        "ram_available_gb": round(
            memory.available / (1024 ** 3), 2
        )
    }


def get_system_info():
    """Get basic information about the Mac."""
    return {
        "operating_system": platform.system(),
        "macos_version": platform.mac_ver()[0],
        "architecture": platform.machine(),
        "processor": platform.processor()
    }

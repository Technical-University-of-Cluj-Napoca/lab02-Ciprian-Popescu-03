import datetime
import os

def smart_log(*args, **kargs) -> None:
    COLORS = {
        "info": "\033[94m",   
        "debug": "\033[90m",   
        "warning": "\033[93m", 
        "error": "\033[91m"   
    }
    RESET = "\033[0m"

    level = kargs.get("level", "info").lower()
    colored = kargs.get("colored", True)
    timestamp = kargs.get("timestamp", False)
    date = kargs.get("date", False)
    save_to = kargs.get("save_to", None)

    message = " ".join(str(arg) for arg in args)

    prefix_parts = []
    if date:
        prefix_parts.append(datetime.datetime.now().strftime("%Y-%m-%d"))
    if timestamp:
        prefix_parts.append(datetime.datetime.now().strftime("%H:%M:%S"))
    prefix = " ".join(prefix_parts)
    if prefix:
        message = f"[{prefix}] {message}"

    if colored and level in COLORS:
        output = f"{COLORS[level]}{message}{RESET}"
    else:
        output = message

    print(output)

    if save_to:
        try:
            os.makedirs(os.path.dirname(save_to), exist_ok=True)
            with open(save_to, "a", encoding="utf-8") as f:
                f.write(f"[{level.upper()}] {message}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")


if __name__ == "__main__":
    username = "Alice"  

    smart_log("System started successfully", level="info", timestamp=True)
    smart_log("User", username, "logged in", level="debug", timestamp=True)
    smart_log("Low disk space detected", level="warning", timestamp=True, save_to="logs/system.log")
    smart_log("Model", "training", "failed", level="error", timestamp=True, colored=False, save_to="logs/errors.log")
    smart_log("Process end", level="info", colored=False, timestamp=True, save_to="logs/errors.log")

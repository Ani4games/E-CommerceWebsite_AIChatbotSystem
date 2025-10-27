import os
import traceback
from datetime import datetime

# Ensure the logs directory exists
LOG_DIR = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(LOG_DIR, exist_ok=True)

ERROR_LOG_PATH = os.path.join(LOG_DIR, "error_logs.txt")

def log_error(error: Exception, context: str = ""):
    """
    Logs exceptions with timestamp and optional context info.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_type = type(error).__name__
    stack_trace = traceback.format_exc()

    log_entry = (
        f"\n[{timestamp}] ⚠️ ERROR in {context or 'General Context'}:\n"
        f"Type: {error_type}\n"
        f"Message: {str(error)}\n"
        f"Traceback:\n{stack_trace}\n"
        f"{'-'*80}\n"
    )

    with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_entry)

    print(f"⚠️ Logged {error_type} in {ERROR_LOG_PATH}")


def safe_execute(func):
    """
    Decorator for wrapping risky functions — logs any raised exceptions.
    Usage:
        @safe_execute
        def risky_function(...):
            ...
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error(e, context=func.__name__)
            return None  # or return a fallback value
    return wrapper


# Optional quick test
if __name__ == "__main__":
    try:
        1 / 0
    except Exception as e:
        log_error(e, "manual_test")

import datetime
import logging
import zoneinfo
from logging.handlers import RotatingFileHandler

# Logging levels:
# - DEBUG = 10, e.g. “Connecting to database with config X”
# - INFO = 20, e.g. “User logged in successfully”
# - WARNING = 30, e.g. “Disk space is running low” (default)
# - ERROR = 40, e.g. “Database connection failed”
# - CRITICAL = 50, e.g. “System outage - service unavailable”
# Setting logging config to a given level does not record messages from lower levels
# This help to focus on only the most important logging messages


def main() -> None:
    # logging.basicConfig(
    #     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    # )

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # associate a logger with this file to differentiate between loggers from different files
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # make it log information to the terminal
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # make it log information to the disk file
    file = logging.FileHandler("loggingdates.log", mode="w")
    file.setLevel(logging.DEBUG)
    file.setFormatter(formatter)
    logger.addHandler(file)

    # or more flexibly, log to a set of files and switch between them
    # set max size (5MB) and backup count (3)
    file_flexible = RotatingFileHandler("loggingdatesrotating.log", maxBytes=1500, backupCount=3)
    file_flexible.setLevel(logging.DEBUG)
    file_flexible.setFormatter(formatter)
    logger.addHandler(file_flexible)

    logger.debug("Debug :)")
    logger.info("Info :)")
    logger.warning("Warning :)")
    logger.error("Error :)")
    logger.critical("Critical :)")

    logger.warning(datetime.datetime.now(tz=datetime.UTC))
    logger.warning(datetime.datetime(2026, 9, 8, 18, 16, 59, tzinfo=datetime.UTC).strftime("%H:%M:%S   %Y:%m:%d"))
    logger.warning(datetime.datetime.strptime("06-06-2006 06:06:06", "%d-%m-%Y %H:%M:%S").astimezone(datetime.UTC).year)
    logger.warning(datetime.date(2002, 5, 4))
    logger.warning(datetime.time(0, 40, 59))

    now = datetime.datetime.now(tz=datetime.UTC)
    birth = datetime.datetime(2002, 5, 4, 0, 40, 59, tzinfo=datetime.UTC)
    days_since_birth = now - birth
    logger.warning("I was born %d days ago", days_since_birth.days)

    tomorrow = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(days=1, seconds=60)
    logger.warning(tomorrow)

    deadline = tomorrow
    screwed_up = deadline <= now
    logger.warning(screwed_up)

    in_calgary = now.astimezone(zoneinfo.ZoneInfo("Canada/Mountain"))
    logger.warning(in_calgary)

    try:
        print(1 / 0)
    except ZeroDivisionError:
        logger.exception("Division by 0 :p")


if __name__ == "__main__":
    main()

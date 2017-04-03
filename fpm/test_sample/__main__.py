import argparse
import logging
import logging.config
from pkg_resources import resource_filename
import gi
from gi.repository import GLib
from pipeline import Pipeline

LOG_CONFIG_PATH = resource_filename(__name__, "/data/logging.conf")

def main():
    # Load logger
    logging.config.fileConfig(LOG_CONFIG_PATH)

    # Create logger
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dot", help="generate dot (you have to export GST_DEBUG_DUMP_DOT_DIR)", action="store_true", default = False)
    args = parser.parse_args()

    export_dot = args.dot

    # Create mainloop
    mainloop = GLib.MainLoop()

    # Create pipeline
    p = Pipeline(export_dot, mainloop)
    logger.info("GStreamer pipeline created.")

    # Start pipeline
    p.run()
    logger.info("Pipeline running.")
    mainloop.run()

if __name__ == "__main__":
    main()

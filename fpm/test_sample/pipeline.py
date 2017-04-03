import sys
import logging
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib

Gst.init(None)

class Pipeline:
    def __init__(self, export_dot, mainloop):
        self.mainloop = mainloop
        self.logger = logging.getLogger(__name__)
        self.pipeline = Gst.Pipeline("pipeline")

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()

        if export_dot:
            self.pipelinename = self.pipeline.get_name()
            self.bus.connect("message::stream-status", self.export_dot)
            self.bus.connect("message::state-changed", self.export_dot)
            self.bus.connect("message::warning", self.export_dot)
            self.bus.connect("message::info", self.export_dot)
            self.bus.connect("message::eos", self.export_dot)
            self.bus.connect("message::error", self.export_dot)

        self.bus.connect("message::eos", self.on_eos)
        self.bus.connect("message::error", self.on_error)

        # Create pipeline
        self.videosrc = Gst.ElementFactory.make("videotestsrc", None)
        self.videosrc.set_property("pattern", 18)
        self.pipeline.add(self.videosrc)

        self.videocaps = Gst.ElementFactory.make("capsfilter",None)
        self.videocaps.set_property("caps", Gst.Caps.from_string("video/x-raw,width=800,height=600"))
        self.pipeline.add(self.videocaps)
        self.videosrc.link(self.videocaps)

        self.timeoverlay = Gst.ElementFactory.make("timeoverlay", None)
        self.pipeline.add(self.timeoverlay)
        self.videocaps.link(self.timeoverlay)

        self.videosink = Gst.ElementFactory.make("autovideosink", None)
        self.pipeline.add(self.videosink)
        self.timeoverlay.link(self.videosink)

    def export_dot(self, bus, message):
        if message.src.name != self.pipelinename:
            return
        elif message.type == Gst.MessageType.ERROR:
            Gst.debug_bin_to_dot_file_with_ts(self.pipeline, Gst.DebugGraphDetails.ALL, "error")
        elif message.type == Gst.MessageType.WARNING:
            Gst.debug_bin_to_dot_file_with_ts(self.pipeline, Gst.DebugGraphDetails.ALL, "warning")
        elif message.type == Gst.MessageType.INFO:
            Gst.debug_bin_to_dot_file_with_ts(self.pipeline, Gst.DebugGraphDetails.ALL, "info")
        elif message.type == Gst.MessageType.STREAM_STATUS:
            status, _ = message.parse_stream_status()
            Gst.debug_bin_to_dot_file_with_ts(self.pipeline, Gst.DebugGraphDetails.ALL, status.value_nick)
        elif message.type == Gst.MessageType.STATE_CHANGED:
            old, new, pending = message.parse_state_changed()
            Gst.debug_bin_to_dot_file_with_ts(self.pipeline, Gst.DebugGraphDetails.ALL, old.value_nick + "_" + new.value_nick)
        self.logger.info("New dot file exported.")

    def on_eos(self, bus, msg):
        self.logger.info("EOS, exit application.")
        self.bus.remove_signal_watch()
        self.pipeline.set_state(Gst.State.NULL)
        self.pipeline = None
        self.mainloop.quit()

    def on_error(self, bus, message):
        self.logger.error("error detected, quit application.")
        err, _=message.parse_error()
        Gst.error("error detected, quit application: {}".format(err.message))
        self.mainloop.quit()

    def run(self):
        self.pipeline.set_state(Gst.State.READY)
        self.pipeline.set_state(Gst.State.PLAYING)

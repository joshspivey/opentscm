#!/usr/bin/env python
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Live Signal Detection
# Generated: Sun Sep 23 22:52:50 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        # try:
        x11 = ctypes.cdll.LoadLibrary('libX11.so')
        x11.XInitThreads()
    else:
        x11 = ctypes.cdll.LoadLibrary('/opt/X11/lib/libX11.dylib')
        x11.XInitThreads()
        # except:
        #     print "Warning: failed to XInitThreads()"


from PyQt5 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import qa_signal_detector_cvf
import osmosdr
import sip
import sys


class live_signal_detection(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Live Signal Detection")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Live Signal Detection")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "live_signal_detection")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.thres = thres = -65
        self.samp_rate = samp_rate = 500000

        ##################################################
        # Blocks
        ##################################################
        self._thres_range = Range(-120, 50, 1, -65, 200)
        self._thres_win = RangeWidget(self._thres_range, self.set_thres, 'Threshold', "counter_slider", float)
        self.top_layout.addWidget(self._thres_win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(100e6, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.inspector_signal_detector_cvf_0 = signal_detector_cvf(samp_rate, 4096, firdes.WIN_BLACKMAN_hARRIS,
            thres,  0.2, False, 0.2, 0.001, 10000, '')
        self.inspector_qtgui_sink_vf_0 = inspector.qtgui_inspector_sink_vf(samp_rate, 4096, 101669000, 1000000, 1, False)
        self._inspector_qtgui_sink_vf_0_win = sip.wrapinstance(self.inspector_qtgui_sink_vf_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._inspector_qtgui_sink_vf_0_win)
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.inspector_qtgui_sink_vf_0, 'map_out'), (self.blocks_message_debug_0, 'print'))    
        self.msg_connect((self.inspector_signal_detector_cvf_0, 'map_out'), (self.inspector_qtgui_sink_vf_0, 'map_in'))    
        self.connect((self.inspector_signal_detector_cvf_0, 0), (self.inspector_qtgui_sink_vf_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.inspector_signal_detector_cvf_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "live_signal_detection")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_thres(self):
        return self.thres

    def set_thres(self, thres):
        self.thres = thres
        self.inspector_signal_detector_cvf_0.set_threshold(self.thres)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.inspector_signal_detector_cvf_0.set_samp_rate(self.samp_rate)
        self.inspector_qtgui_sink_vf_0.set_samp_rate(self.samp_rate)


def main(top_block_cls=live_signal_detection, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()

#!/usr/bin/python
"""
Created on Sept 7, 2015
@author: dashesy
Purpose: Access AVFoundation as a Cython class

format:
    python capture_video.py <video_name> [-duration <seconds>]
options:
    <video_name>: name of the video to record
    -duration <seconds>: how many seconds to record
    -qthread: run recording in a QThread
"""

import sys
import pyavfcam

threaded = False
duration = 10
video_name = None

parg = None
for arg_idx, arg in enumerate(sys.argv):
    if arg_idx == 0:
        continue
    if parg == '-duration':
        duration = float(arg)
    if parg:
        parg = None
        continue
    if arg == '-duration':
        parg = arg
    elif arg == '-qthread':
        threaded = True
    elif video_name is None:
        video_name = arg
    else:
        raise ValueError('Unknow argument %s' % arg)

if video_name is None:
    raise ValueError('capture_video.py <video_name> [-duration <seconds>]')


if threaded:
    try:
        # noinspection PyPackageRequirements
        from PySide import QtCore
    except ImportError:
        # noinspection PyPackageRequirements
        from PyQt4 import QtCore
        # noinspection PyUnresolvedReferences
        QtCore.Signal = QtCore.pyqtSignal
        # noinspection PyUnresolvedReferences
        QtCore.Slot = QtCore.pyqtSlot

    class Worker(QtCore.QObject):

        done = QtCore.Signal()

        def __init__(self, _app):
            """run an app job in a thread
            """
            super(Worker, self).__init__()

            self.t = QtCore.QThread(objectName='record_thread')
            self.moveToThread(self.t)
            # noinspection PyUnresolvedReferences
            self.t.started.connect(self.task)
            self.done.connect(self.t.quit)
            self.done.connect(_app.quit)

            self.t.start()

        def task(self):
            thread_name = QtCore.QThread.currentThread().objectName()
            print '[%s] recording' % thread_name
            record()
            print '[%s] done' % thread_name
            self.done.emit()

    import traceback
    import signal
    app = QtCore.QCoreApplication([])
    # ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    def excepthook(exc_type, exc_val, tracebackobj):
        print ''.join(traceback.format_exception(exc_type, exc_val, tracebackobj))
        # quit on exception
        app.quit()
    sys.excepthook = excepthook
    timer = QtCore.QTimer()
    timer.start(200)
    timer.timeout.connect(lambda: None)

    w = Worker(app)
    sys.exit(app.exec_())


def record():
    # Open the default video source and record
    cam = pyavfcam.AVFCam()
    if not duration:
        return
    cam.record(video_name, duration=duration)
    print "Saved " + video_name + " (Size: " + str(cam.shape[0]) + " x " + str(cam.shape[1]) + ")"


if not threaded:
    record()

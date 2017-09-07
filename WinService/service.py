#!/usr/bin/python
# -*- coding: utf-8 -*-

import win32service
import win32event
import win32serviceutil
import servicemanager
import sys
import socket
from threading import Thread
import dirwatch


class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "WindowsDenemeMonitorxx"
    _svc_display_name_ = "Windows Deneme Monitorxx"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)


    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.__startService()

    def __startService(self):
        dirwatch.directoryWatcher()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AppServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)
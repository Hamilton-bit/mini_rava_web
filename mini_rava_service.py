import win32serviceutil
import win32service
import win32event
import servicemanager
from app import app  # Make sure app.py is in the same folder

class RavaService(win32serviceutil.ServiceFramework):
    _svc_name_= "MiniRavaService"
    _svc_display_name_= "Mini Rava Assistant Service"

    def _init_(self, args):
        win32serviceutil.ServiceFramework._init_(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self.svc_name, ""))
        app.run(host="127.0.0.1", port=5000)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(RavaService)
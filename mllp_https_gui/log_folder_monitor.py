### Added feature: HTTPS to MLLP
### By Tiago Rodrigues
### Sectra Iberia, Dec 2022

# Looks and deletes old
import datetime
import os
import sys
from time import sleep


class LogMonitor:

    def __init__(self, number_of_days_check, folder_path):
        self.folder_path = folder_path
        self.number_of_days_check = number_of_days_check

    # task that runs at a fixed interval
    def background_task(self):
        interval_days = self.number_of_days_check
        interval_sec = interval_days * 24 * 60 * 60  # Days to sec

        # run forever
        while True:
            # block for the interval
            sleep(interval_sec)

            # perform the task
            N = interval_days
            if not os.path.exists(self.folder_path):
                print("Please provide valid path")
                sys.exit(1)
            if os.path.isfile(self.folder_path):
                print("Please provide dictionary path")
                sys.exit(2)
            today = datetime.datetime.now()
            for each_file in os.listdir(self.folder_path):
                if each_file[len(each_file) - 4:len(each_file)] != ".log":
                    each_file_path = os.path.join(self.folder_path, each_file)
                    if os.path.isfile(each_file_path):
                        datetime_str = each_file[len(each_file) - 19:len(each_file)]

                        file_cre_date = datetime.datetime.strptime(datetime_str, '%Y-%m-%d_%H-%M-%S')
                        # file_cre_date = datetime.datetime.fromtimestamp(os.path.getctime(each_file_path))

                        dif_days = (today - file_cre_date).days
                        if dif_days > N:
                            os.remove(each_file_path)
                            print(each_file_path, dif_days)

    def start(self):
        self.background_task()



# import servicemanager
# import win32event
# import win32service
# import win32serviceutil
#
#
# class LogMonitor(win32serviceutil.ServiceFramework):
#     '''Base class to create winservice in Python'''
#     # https://thepythoncorner.com/posts/2018-08-01-how-to-create-a-windows-service-in-python/
#
#     _svc_name_ = 'SECTRA_MLLP_HTTPS_Log_Monitor'
#     _svc_display_name_ = 'SECTRA - MLLP2HTTPS - Log Monitor'
#     _svc_description_ = 'Log Monitor'
#
#     @classmethod
#     def parse_command_line(cls):
#         '''
#         ClassMethod to parse the command line
#         '''
#
#         win32serviceutil.HandleCommandLine(cls)
#
#     def __init__(self, args):
#         '''
#         Constructor of the winservice
#         '''
#         win32serviceutil.ServiceFramework.__init__(self, args)
#         self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
#         socket.setdefaulttimeout(60)
#
#
#     def SvcStop(self):
#         '''
#         Called when the service is asked to stop
#         '''
#         self.stop()
#         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#         win32event.SetEvent(self.hWaitStop)
#
#     def SvcDoRun(self):
#         '''
#         Called when the service is asked to start
#         '''
#         self.start()
#         servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
#                               servicemanager.PYS_SERVICE_STARTED,
#                               (self._svc_name_, ''))
#         self.main()
#
#     def define(self,number_of_days_check, folder_path):
#         self.folder_path = folder_path
#         self.number_of_days_check = number_of_days_check
#
#     def start(self):
#         self.isrunning = True
#
#     def stop(self):
#         self.isrunning = False
#
#     def main(self):
#         interval_days = self.number_of_days_check
#         interval_sec = interval_days * 24 * 60 * 60  # Days to sec
#
#         # run forever
#         while self.isrunning:
#             # block for the interval
#             sleep(interval_sec)
#
#             # perform the task
#             N = interval_days
#             if not os.path.exists(self.folder_path):
#                 print("Please provide valid path")
#                 sys.exit(1)
#             if os.path.isfile(self.folder_path):
#                 print("Please provide dictionary path")
#                 sys.exit(2)
#             today = datetime.datetime.now()
#             for each_file in os.listdir(self.folder_path):
#                 if each_file[len(each_file) - 4:len(each_file)] != ".log":
#                     each_file_path = os.path.join(self.folder_path, each_file)
#                     if os.path.isfile(each_file_path):
#                         datetime_str = each_file[len(each_file) - 19:len(each_file)]
#
#                         file_cre_date = datetime.datetime.strptime(datetime_str, '%Y-%m-%d_%H-%M-%S')
#                         # file_cre_date = datetime.datetime.fromtimestamp(os.path.getctime(each_file_path))
#
#                         dif_days = (today - file_cre_date).days
#                         if dif_days > N:
#                             os.remove(each_file_path)
#                             print(each_file_path, dif_days)






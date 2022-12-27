### Added feature: HTTPS to MLLP
### By Tiago Rodrigues
### Sectra Iberia, Dec 2022
import argparse

from mllp_https_gui.gui import Gui
from mllp_https_gui.loading_window import LoadingWindow


class ArgumentFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def gui():
    Gui()

# def log_monitor():
#     parser = argparse.ArgumentParser(
#         "mllp2https",
#         description="MLLP server that proxies an HTTPS client. Sends back the HTTPS response.",
#         formatter_class=ArgumentFormatter,
#     )
#
#     parser.add_argument(
#         "log_folder",
#         help="Log folder path",
#     )
#     parser.add_argument(
#         "-D",
#         "--days_to_check",
#         help="Maximum log age",
#         default=30,
#         type=int,
#     )
#
#     args = parser.parse_args()
#
#     log_monitor = LogMonitor(
#         number_of_days_check=args.days_to_check,
#         folder_path=args.log_folder,
#     )
#     log_monitor.start()




# Loading Window
loading_window = LoadingWindow()
loading_window.open()

# gui()
#sys.stdout.close()

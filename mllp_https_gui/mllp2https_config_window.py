### Added feature: HTTPS to MLLP
### By Tiago Rodrigues
### Sectra Iberia, Dec 2022
import os
import subprocess
import sys
import sysconfig
from time import sleep

import PySimpleGUI as sg
import inspect


class MLLPHTTPSConfigWindow:
    def __init__(self):
        sg.theme('SystemDefault1')
        # Layout

        layout_header = [
            [sg.Text('Windows Service Configuration for MLLP to HTTPS parser:')],
        ]

        layout_configurations = [
            [sg.Frame('HTTPS client Configurations',
                      [
                          [sg.Text('HTTPS URL and Port:'),
                           sg.InputText(
                               key='https_url',
                               default_text='https://localhost:8000', )
                           ],
                          [sg.Text('HTTPS Content-Type header:'),
                           sg.Text('application/hl7-v2; charset=utf-8')
                           # sg.InputText(
                           #     key='--content-type',
                           #     default_text='application/hl7-v2; charset=utf-8')
                           ],
                          [sg.Text('Session Timeout (Milliseconds):'),
                           sg.InputText(
                               key='--timeout',
                               default_text='0')
                           ],
                          [
                              sg.Checkbox('Verify SSL certificate on server side', default=False, key='--verify')
                              # Missing: Validate if user provides path
                          ],
                          [sg.Text('Path to CA_BUNDLE file or directory with certificates of trusted CAs:'),
                           sg.In(enable_events=True, key='-CA_FOLDER-', disabled=True),
                           sg.FolderBrowse(
                               initial_folder='C:\\mllp-https\\log',
                               key='-verifyCA-', )  # Missing: If a path to CAs is given, ignore checkbox
                           ],
                      ], expand_x=True, )
             ],
            [sg.Frame('MLLP Listenner Configurations',
                      [
                          [sg.Text('MLLP IPv4 host:'),
                           sg.InputText(
                               key='--host',
                               default_text='0.0.0.0')
                           ],
                          [sg.Text('MLLP Port:'),
                           sg.InputText(
                               key='--port',
                               default_text='2575')
                           ],
                          [sg.Text('MLLP release version:'),
                           sg.InputText(
                               key='--mllp-release',
                               default_text='1')
                           ],
                      ], expand_x=True, )
             ],
            [sg.Frame('HTTPS User authentication (Optional)',
                      [
                          [
                              sg.Checkbox('User Authentication', default=False, key='user_authentication')
                              # Missing: Validate if user provides username and password
                          ],
                          [sg.Text('Username:'),
                           sg.InputText(
                               key='--username', )
                           ],
                          [sg.Text('Password:'),
                           sg.InputText(
                               key='--password',
                               password_char='*',
                           )
                           ]
                      ], expand_x=True, )
             ],
            [sg.Frame('Logging to File (Optional)',
                      [
                          [
                              sg.Checkbox('Log to folder ->', default=False, key='log_to_folder'),
                              sg.Text('Path to folder (Cannot have spaces):'),
                              sg.In(enable_events=True, key='-LOG_FOLDER-', disabled=True),
                              sg.FolderBrowse(
                                  initial_folder='C:\\',
                                  key='--log-folder', )
                              # Missing: Validate if user provides path
                          ],
                          # [sg.Text('Path to folder:'),
                          #  sg.In(enable_events=True, key='-LOG_FOLDER-'),
                          #  sg.FolderBrowse(
                          #      initial_folder='C:\\mllp-https\\log',
                          #      key='--log-folder', )
                          #  ],
                          [sg.Text('Log level:'),
                           sg.Combo(
                               values=['info', 'warn', 'error'],
                               default_value='info',
                               key='--log-level',
                           )
                           ]
                      ], expand_x=True, )
             ],
            [sg.Frame('Windows Service',
                      [
                          [sg.Text('Path to NSSM.exe folder:',
                                   text_color='orange red',
                                   key='-NSSM_TEXT-',),
                           sg.In(enable_events=True, key='-NSSM_FOLDER-', disabled=True),
                           sg.FolderBrowse(
                               initial_folder='.\\doc',
                               key='-NSSM-folder-', )
                           ],
                          [
                              sg.Checkbox('Define Windows Admin User', default=False, key='use_winservice_user')
                          ],
                          [sg.Text('Windows Username (Username@Domain):'),
                           sg.InputText(
                               key='-win_user-', )
                           ],
                          [sg.Text('Password:'),
                           sg.InputText(
                               key='-win-password-',
                               password_char='*',
                           )
                           ],
                      ], expand_x=True, )
             ],
            [sg.VSeparator(pad=(0, 15))],
            [
                sg.Button('Create Windows Service',
                          key='-CreateWinService-',
                          disabled=True),
                sg.Button('Delete Windows Service',
                          key='-DeleteWinService-',
                          disabled=True),
            ],
        ]

        layout_footer = [
            [sg.Stretch(), sg.Image(os.path.abspath('../lib/site-packages/mllp_https_gui/doc/logo_mllp2https.png')), sg.Stretch(), sg.Image(os.path.abspath('../lib/site-packages/mllp_https_gui/doc/sectra.png'))],
        ]

        layout = [
            [sg.Column(layout_header,
                       k='layout_header',
                       element_justification='c',
                       expand_x=True, )],
            [sg.Column(layout_configurations,
                       k='layout_configurations',
                       element_justification='c',
                       expand_x=True, )],
            [sg.VSeparator(pad=(0, 15))],
            [sg.Stretch(), sg.Column(layout_footer,
                                     k='layout_footer',
                                     element_justification='center',
                                     vertical_alignment='b',
                                     expand_x=True, )]
        ]

        # Window
        self.window = sg.Window(
            'MLLP 2 HTTPS Config',
            element_justification='c',
            icon=os.path.abspath('../lib/site-packages/mllp_https_gui/doc/icon.ico'),
        ).layout(layout)

    def open(self):
        # Update folder and Info on window
        while True:
            # Get values from window
            self.event, self.values = self.window.Read()
            if self.event in (sg.WIN_CLOSED, 'Exit'):
                break
            if self.values['-NSSM-folder-'] is not None:
                self.checkservice()
            if self.event == '-LOG_FOLDER-':
                # print(self.event)
                self.folder = self.values['-LOG_FOLDER-']
            if self.event == '-CA_FOLDER-':
                # print(self.event)
                self.CA_folder = self.values['-CA_FOLDER-']
            if self.event == '-CreateWinService-':
                #print("Configuration values", self.values)

                # Validate the arguments
                if not self.values['user_authentication']:
                    self.values['--username'] = ''
                    self.values['--password'] = ''

                if not self.values['-verifyCA-'] == '':
                    if self.values['--verify']:
                        self.values['--verify'] = self.values['-verifyCA-']

                if not self.values['log_to_folder']:
                    self.values['--log-folder'] = ''

                # Create the service:
                self.winservice()
                sleep(1)
                self.checkservice()

            if self.event == '-DeleteWinService-':
                self.deleteService()
                sleep(1)
                self.checkservice()

    def checkservice(self):
        self.window['-NSSM_TEXT-'].update(text_color='black')
        # Check if there is already a service
        path_to_nssm = self.values['-NSSM-folder-']
        cmd = '"' + path_to_nssm + '\\nssm.exe"'
        cmd += ' status SECTRA_MLLP_HTTPS'
        # subprocess.call()
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
            #print(output)
            self.window['-CreateWinService-'].update(disabled=True)
            self.window['-DeleteWinService-'].update(disabled=False)
        except subprocess.CalledProcessError as e:
            self.window['-CreateWinService-'].update(disabled=False)
            self.window['-DeleteWinService-'].update(disabled=True)
            #print(e)


    def winservice(self):

        # Validate and construct the arguments
        program = 'mllp2https.exe'
        arguments = ''
        arguments += ' ' + self.values['https_url']

        for valuekey in self.values.keys():
            if valuekey[0:2] == '--':
                if not self.values[valuekey] == '':
                    # print(valuekey, self.values[valuekey])
                    arguments += ' ' + str(valuekey) + ' "' + str(self.values[valuekey]) + '"'

        # print('Running Command: ', binpath)

        # Create the service:
        # Path were mllp-https and GUI are when installed with pip:
        user_scripts_path = sysconfig.get_path('scripts')

        # Construct the command
        # cmd = 'sc create SECTRA_MLLP_HTTPS displayname= "SECTRA - MLLP2HTTPS" error= severe'
        # https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/sc-create
        # SC create and SC Start does not work since it is not possible to import mllp2https arguments on creating
        # the service. NSSM will be used instead: https://nssm.cc/commands

        path_to_nssm = self.values['-NSSM-folder-']
        cmd = '"' + path_to_nssm + '\\nssm.exe"'
        cmd += ' install SECTRA_MLLP_HTTPS'

        cmd += ' "' + str(user_scripts_path) + '\\' + program + '"' + arguments
        # cmd += ' start= auto'

        print('Running Command: ', cmd)

        subprocess.call(cmd, shell=True)

        # Edit Service Parameters
        cmd_name = '"' + path_to_nssm + '\\nssm.exe" set SECTRA_MLLP_HTTPS DisplayName "SECTRA - MLLP2HTTPS"'
        subprocess.call(cmd_name)

        if self.values['use_winservice_user']:
            winuser = self.values['-win_user-']
            winpass = self.values['-win-password-']
            if winuser != '' and winpass != '':
                subprocess.call('"' + path_to_nssm + '/nssm.exe" set SECTRA_MLLP_HTTPS ObjectName ' +
                                winuser + '' + winpass)

        subprocess.call('"' + path_to_nssm + '\\nssm.exe" set SECTRA_MLLP_HTTPS Start "SERVICE_AUTO_START"')
        # print('"' + path_to_nssm + '\\nssm.exe" set SECTRA_MLLP_HTTPS Start "SERVICE_AUTO_START"')
        subprocess.call('"' + path_to_nssm + '\\nssm.exe" set SECTRA_MLLP_HTTPS AppStdout '
                        + str(self.values['--log-folder']).replace('_svc_gui', '') + '\\servive.log')
        subprocess.call('"' + path_to_nssm + '\\nssm.exe" set SECTRA_MLLP_HTTPS AppStderr ' +
                        str(self.values['--log-folder']).replace('_svc_gui', '') + '\\error.log')

        # Start the service
        # os.system('sc start SECTRA_MLLP_HTTPS')
        cmd_start = '"' + path_to_nssm + '\\nssm.exe" start SECTRA_MLLP_HTTPS'
        # print('"' + path_to_nssm + '\\nssm.exe" start SECTRA_MLLP_HTTPS')

        subprocess.call(cmd_start)

    def deleteService(self):

        # Stop the service
        path_to_nssm = self.values['-NSSM-folder-']
        cmd = '"' + path_to_nssm + '\\nssm.exe"'
        cmd += ' stop SECTRA_MLLP_HTTPS'
        subprocess.call(cmd, shell=True)

        # Delete the service
        cmd = '"' + path_to_nssm + '\\nssm.exe"'
        cmd += ' remove SECTRA_MLLP_HTTPS confirm'
        subprocess.call(cmd)

    # def logmonitor(self):
    #     # Start the monitor service
    #     # self.values['--log-folder']
    #
    #     path_to_nssm = self.values['-NSSM-folder-']
    #     cmd = '"' + path_to_nssm + '\\nssm.exe"'
    #     cmd += ' install SECTRA_MLLP_HTTPS_LOG_MONITOR'
    #
    #     user_scripts_path = sysconfig.get_path('scripts')
    #     program = 'mllp_https_log_monitor.exe'
    #     arguments = str(self.values['--log-folder']) + ' --days_to_check ' + '30'
    #     cmd += ' "' + str(user_scripts_path) + '\\' + program + '" ' + arguments
    #
    #     subprocess.call(cmd, shell=True)
    #
    #     # Edit Service Parameters
    #     cmd_name = '"' + path_to_nssm \
    #                + '\\nssm.exe" set SECTRA_MLLP_HTTPS_LOG_MONITOR DisplayName "SECTRA - MLLP2HTTPS - LOG MONITOR"'
    #     subprocess.call(cmd_name, shell=True)
    #
    #     if self.values['use_winservice_user']:
    #         winuser = self.values['-win_user-']
    #         winpass = self.values['-win-password-']
    #         if winuser != '' and winpass != '':
    #             subprocess.call('"' + path_to_nssm + '/nssm.exe" set SECTRA_MLLP_HTTPS_LOG_MONITOR ObjectName ' +
    #                             winuser + '' + winpass, shell=True)
    #
    #     subprocess.call('"' + path_to_nssm + '\\nssm.exe" set SECTRA_MLLP_HTTPS_LOG_MONITOR Start "SERVICE_AUTO_START"',
    #                     shell=True)
    #
    #     # Start the service
    #     # os.system('sc start SECTRA_MLLP_HTTPS')
    #     cmd_start = '"' + path_to_nssm + '\\nssm.exe" start SECTRA_MLLP_HTTPS_LOG_MONITOR'
    #
    #     subprocess.call(cmd_start, shell=True)

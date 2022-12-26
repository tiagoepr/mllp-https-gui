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


class HTTPSMLLPConfigWindow:
    def __init__(self):
        sg.theme('SystemDefault1')
        # Layout

        layout_header = [
            [sg.Text('Windows Service Configuration for HTTPS to MLLP parser:')],
        ]

        layout_configurations = [
            [sg.Frame('MLLP Client Configurations',
                       [
                           [sg.Text('MLLP Host:'),
                            sg.InputText(
                                key='mllp_url',
                                default_text='localhost'),
                            sg.VSeparator(pad=(20, 0)),
                            sg.Checkbox('MLLP Parser to Simple Text',
                                         default=True,
                                         key='--mllp_parser'),
                            ],
                           [sg.Text('MLLP Port:'),
                            sg.InputText(
                                key='--mllp_port ',
                                default_text='2575')
                            ],

                           [sg.Text('MLLP keep-alive (milliseconds) (-1 for unlimited):'),
                            sg.InputText(
                                key='--mllp-keep-alive',
                                default_text='10000')
                            ],
                           [sg.Text('Maximum number of messages per connection (-1 for unlimited):'),
                            sg.InputText(
                                key='--mllp-max-messages',
                                default_text='-1')
                            ],
                           [sg.Text('MLLP release version:'),
                            sg.InputText(
                                key='--mllp-release',
                                default_text='1')
                            ],
                       ], expand_x=True, )
              ],
            [sg.Frame('HTTPS Server Configurations',
                      [
                          [sg.Text('HTTPS IPv4 Host:'),
                           sg.InputText(
                               key='--host',
                               default_text='0.0.0.0', )
                           ],
                          [sg.Text('HTTPS Port:'),
                           sg.InputText(
                               key='--port',
                               default_text='8000', )
                           ],
                          [sg.Text('Path to Server SSL/TLS certificate:', key='cert', text_color='orange red'),
                           sg.In(enable_events=True, key='-CERTIFICATE-', disabled=True),
                           sg.FileBrowse(
                               initial_folder='C:\\mllp-https\\',
                               key='--certfile',
                               file_types=(('CRT Files', '*.crt'),))
                           ],
                          [sg.Text('Path to Server SSL/TLS Private Key:', key='key', text_color='orange red'),
                           sg.In(enable_events=True, key='-KEYFILE-', disabled=True),
                           sg.FileBrowse(
                               initial_folder='C:\\mllp-https\\',
                               key='--keyfile',
                               file_types=(('Private Key files', '*.key'), ))
                           ],
                          [sg.Text('HTTPS Content-Type header:'),
                           sg.Text('application/hl7-v2; charset=utf-8')
                           ],
                          [sg.Text('Session Timeout (Milliseconds):'),
                           sg.InputText(
                               key='--timeout',
                               default_text='0',),
                           ],
                           [sg.Text('Session Keep-Alive time (Milliseconds):'),
                           sg.InputText(
                               key='--keep-alive',
                               default_text='0')
                           ],

                      ], expand_x=True, )
             ],
            [sg.Frame('HTTPS Server authentication (Optional)',
                      [
                          [
                              sg.Checkbox('Server Authentication', default=False, key='user_authentication')
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
            'HTTPS 2 MLLP Config',
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
            if self.values['-NSSM-folder-'] is not None and self.values['-NSSM-folder-'] != '':
                self.window['-NSSM_TEXT-'].update(text_color='black')
                if self.values['--certfile'] is not None and self.values['--certfile'] != '':
                    if self.values['--keyfile'] is not None and self.values['--keyfile'] != '':
                        self.checkservice()
            if self.values['--certfile'] is not None and self.values['--certfile'] != '':
                self.window['cert'].update(text_color='black')
            if self.values['--keyfile'] is not None and self.values['--keyfile'] != '':
                self.window['key'].update(text_color='black')


            if self.event == '-CreateWinService-':
                #print("Configuration values", self.values)

                # Validate the arguments
                if not self.values['user_authentication']:
                    self.values['--username'] = ''
                    self.values['--password'] = ''

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

        # Check if there is already a service
        path_to_nssm = self.values['-NSSM-folder-']
        cmd = '"' + path_to_nssm + '\\nssm.exe"'
        cmd += ' status SECTRA_HTTPS_MLLP'
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
        program = 'https2mllp.exe'
        arguments = ''
        arguments += ' ' + self.values['mllp_url']

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
        # cmd = 'sc create SECTRA_HTTPS_MLLP displayname= "SECTRA - MLLP2HTTPS" error= severe'
        # https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/sc-create
        # SC create and SC Start does not work since it is not possible to import mllp2https arguments on creating
        # the service. NSSM will be used instead: https://nssm.cc/commands

        path_to_nssm = self.values['-NSSM-folder-']
        cmd = '"' + path_to_nssm + '\\nssm.exe"'
        cmd += ' install SECTRA_HTTPS_MLLP'

        cmd += ' "' + str(user_scripts_path) + '\\' + program + '"' + arguments
        # cmd += ' start= auto'

        print('Running Command: ', cmd)

        subprocess.call(cmd, shell=True)

        # Edit Service Parameters
        cmd_name = '"' + path_to_nssm + '\\nssm.exe" set SECTRA_HTTPS_MLLP DisplayName "SECTRA - MLLP2HTTPS"'
        subprocess.call(cmd_name)

        if self.values['use_winservice_user']:
            winuser = self.values['-win_user-']
            winpass = self.values['-win-password-']
            if winuser != '' and winpass != '':
                subprocess.call('"' + path_to_nssm + '/nssm.exe" set SECTRA_HTTPS_MLLP ObjectName ' +
                                winuser + ' ' + winpass)

        subprocess.call('"' + path_to_nssm + '\\nssm.exe" set SECTRA_HTTPS_MLLP Start "SERVICE_AUTO_START"')
        # print('"' + path_to_nssm + '\\nssm.exe" set SECTRA_HTTPS_MLLP Start "SERVICE_AUTO_START"')
        subprocess.call('"' + path_to_nssm + '\\nssm.exe" set SECTRA_HTTPS_MLLP AppStdout '
                        + str(self.values['--log-folder']).replace('_svc_gui', '') + '\\servive.log')
        subprocess.call('"' + path_to_nssm + '\\nssm.exe" set SECTRA_HTTPS_MLLP AppStderr ' +
                        str(self.values['--log-folder']).replace('_svc_gui', '') + '\\error.log')

        # Start the service
        # os.system('sc start SECTRA_HTTPS_MLLP')
        cmd_start = '"' + path_to_nssm + '\\nssm.exe" start SECTRA_HTTPS_MLLP'
        # print('"' + path_to_nssm + '\\nssm.exe" start SECTRA_HTTPS_MLLP')

        subprocess.call(cmd_start)

    def deleteService(self):

        # Stop the service
        path_to_nssm = self.values['-NSSM-folder-']
        cmd = '"' + path_to_nssm + '\\nssm.exe"'
        cmd += ' stop SECTRA_HTTPS_MLLP'
        subprocess.call(cmd, shell=True)

        # Delete the service
        cmd = '"' + path_to_nssm + '\\nssm.exe"'
        cmd += ' remove SECTRA_HTTPS_MLLP confirm'
        subprocess.call(cmd)

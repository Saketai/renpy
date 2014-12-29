﻿# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init python:
    IOS_NO_RENIOS = 0
    IOS_NO_DIRECTORY = 1
    IOS_NO_PROJECT = 2
    IOS_OK = 3

    IOS_NO_RENIOS_TEXT = _("To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher.")
    IOS_NO_DIRECTORY_TEXT = _("The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it.")
    IOS_NO_PROJECT_TEXT = _("There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one.")
    IOS_OK_TEXT = _("An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it.")

    IPHONE_TEXT = _("Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down.")
    IPAD_TEXT = _("Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down.")

    IOS_SELECT_DIRECTORY_TEXT = _("Selects the directory where Xcode projects will be placed.")
    IOS_CREATE_PROJECT_TEXT = _("Creates an Xcode project corresponding to the current Ren'Py project.")
    IOS_UPDATE_PROJECT_TEXT = _("Updates the Xcode project with files from the current Ren'Py project.")
    IOS_XCODE_TEXT = _("Opens the Xcode project in Xcode.")

    def find_renios():

        global RENIOS_PATH

        candidates = [ ]

        RENIOS_PATH = os.path.join(config.renpy_base, "renios")

        if os.path.isdir(RENIOS_PATH):
            import sys
            sys.path.insert(0, os.path.join(RENIOS_PATH, "buildlib"))
        else:
            RENIOS_PATH = None

    find_renios()


    def IOSState():
        return IOS_NO_RENIOS

    def IOSStateText(state):
        if state == IOS_NO_RENIOS:
            return IOS_NO_RENIOS_TEXT
        elif state == IOS_NO_DIRECTORY:
            return IOS_NO_DIRECTORY_TEXT
        elif state == IOS_NO_PROJECT:
            return IOS_NO_PROJECT_TEXT
        else:
            return IOS_OK_TEXT


screen ios:

    default tt = Tooltip(None)
    $ state = IOSState()

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("iOS: [project.current.name!q]")

            add HALF_SPACER

            hbox:

                # Left side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Emulation:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has hbox:
                                spacing 15

                            textbutton _("iPhone"):
                                action LaunchEmulator("ios-touch", "small phone touch ios")
                                hovered tt.Action(IPHONE_TEXT)

                            textbutton _("iPad"):
                                action LaunchEmulator("ios-touch", "medium tablet touch ios")
                                hovered tt.Action(IPAD_TEXT)


                    add SPACER
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Build:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has vbox

                            text "This space for rent."

#                             textbutton _("Install SDK & Create Keys"):
#                                 action AndroidIfState(state, ANDROID_NO_SDK, Jump("android_installsdk"))
#                                 hovered tt.Action(INSTALL_SDK_TEXT)
#
#                             textbutton _("Configure"):
#                                 action AndroidIfState(state, ANDROID_NO_CONFIG, Jump("android_configure"))
#                                 hovered tt.Action(CONFIGURE_TEXT)
#
#                             textbutton _("Build Package"):
#                                 action AndroidIfState(state, ANDROID_OK, AndroidBuild("android_build"))
#                                 hovered tt.Action(BUILD_TEXT)
#
#                             textbutton _("Build & Install"):
#                                 action AndroidIfState(state, ANDROID_OK, AndroidBuild("android_build_and_install"))
#                                 hovered tt.Action(BUILD_AND_INSTALL_TEXT)
#
#                             textbutton _("Build, Install & Launch"):
#                                 action AndroidIfState(state, ANDROID_OK, AndroidBuild("android_build_install_and_launch"))
#                                 hovered tt.Action(BUILD_INSTALL_AND_LAUNCH_TEXT)


                # Right side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        add SPACER

                        if tt.value:
                            text tt.value
                        else:
                            text IOSStateText(state)


    textbutton _("Back") action Jump("front_page") style "l_left_button"


label ios:

    if RENIOS_PATH is None:
        $ interface.yesno(_("Before packaging Android apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"), no=Jump("front_page"))
        $ add_dlc("renios", restart=True)

    call screen ios


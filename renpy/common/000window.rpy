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

# This file contains the definition and implementation of the window show,
# window hide, and window auto statements.

init -1200 python:

    config.window_show_transition = None
    config.window_hide_transition = None

    def _window_show(trans=None):
        if store._window:
            return

        if _preferences.show_empty_window:
            renpy.with_statement(None)
            store._window = True
            renpy.with_statement(trans)
        else:
            store._window = True

    def _window_hide(trans=None):
        if not store._window:
            return

        if _preferences.show_empty_window:
            renpy.with_statement(None)
            store._window = False
            renpy.with_statement(trans)
        else:
            store._window = False

python early hide:
    ##########################################################################
    # "window show" and "window hide" statements.

    def parse_window(l):
        p = l.simple_expression()
        if not l.eol():
            renpy.error('expected end of line')

        return p

    def lint_window(p):
        if p is not None:
            _try_eval(p, 'window transition')

    def execute_window_show(p):

        if p is not None:
            trans = eval(p)
        else:
            trans = config.window_show_transition

        _window_show(trans)

    def execute_window_hide(p):

        if p is not None:
            trans = eval(p)
        else:
            trans = config.window_hide_transition

        _window_hide(trans)

    renpy.register_statement('window show',
                              parse=parse_window,
                              execute=execute_window_show,
                              lint=lint_window)

    renpy.register_statement('window hide',
                              parse=parse_window,
                              execute=execute_window_hide,
                              lint=lint_window)

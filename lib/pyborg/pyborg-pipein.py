#!/usr/bin/env python
# vim: set sw=4 sts=4 ts=8 et:
#
# PyBorg Offline line input module
#
# Copyright (c) 2000, 2006 Tom Morton, Sebastien Dailly
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
import string
import sys

import pyborg

class ModLineIn:
    """
    Module to interface piped input and output with the PyBorg learn module.
    """

    def __init__(self, my_pyborg):
        self.pyborg = my_pyborg
        self.start()

    def start(self):
        while 1:
            try:
                body = raw_input()
            except (KeyboardInterrupt, EOFError), e:
                print
                return
            if body == "":
                continue
            # Pass message to borg
            self.pyborg.process_msg(self, body, 0, 1, ())

if __name__ == "__main__":
    # start the pyborg
    my_pyborg = pyborg.pyborg()
    try:
        ModLineIn(my_pyborg)
    except SystemExit:
        pass
    my_pyborg.save_all()
    del my_pyborg
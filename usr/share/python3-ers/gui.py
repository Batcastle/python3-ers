#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  gui.py
#
#  Copyright 2020 Thomas Castleman <contact@draugeros.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""GUI for ERS"""
import gi
gi.require_version("Gtk", 3.0)
from gi.repository import Gtk


class ERS_Window(Gtk.Window):
    """Main Window for ERS"""
    def __init__(self, game_object):
        """Initialize Window"""
        Gtk.Window.__init__(self, title="ERS")
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_name("kpatience")
        
        self.ers = game_object
        
        self.main_window("clicked")
        
    def main_window(self, widget):
        """Set up main game window and game logic"""
        
        self.show_all()
        
    def clear_window(self):
        """Clear Window"""
        children = self.grid.get_children()
        for each0 in children:
            self.grid.remove(each0)

    def exit(self, button):
        """Exit"""
        Gtk.main_quit("delete-event")
        self.destroy()


def show_window(game_object):
    """Show Main UI"""
    window = ERS_Window(game_object)
    window.set_decorated(True)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", ERS_Window.exit)
    window.show_all()
    Gtk.main()
    window.exit("clicked")

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
import time
import json
import os
import copy
import threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk, cairo


class ERS_Window(Gtk.Window):
    """Main Window for ERS"""
    def __init__(self, game_object):
        """Initialize Window"""
        # Set up generic window properties
        Gtk.Window.__init__(self, title="ERS")
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_name("kpatience")
        self.connect("key-press-event", self.on_key_press_event)

        # Make our game object
        self.ers = game_object

        # Get our images for the cards into memory so we can improve performance
        # by not needing to load them from disk all the time
        suit_order = {"2": None, "3": None, "4": None, "5": None, "6": None,
                      "7": None, "8": None, "9": None, "10": None, "ace": None,
                      "jack": None, "queen": None, "king": None}
        back_buf = GdkPixbuf.Pixbuf.new_from_file("assets/back.svg")
        self.cards = {"back": back_buf,
                      "hearts": copy.copy(suit_order),
                      "diamonds": copy.copy(suit_order),
                      "spades": copy.copy(suit_order),
                      "clubs": copy.copy(suit_order)}

        for suit in self.cards:
            if suit == "back":
                continue
            for rank in self.cards[suit]:
                self.cards[suit][rank] = load_image(suit, rank)

        # Make slap timestamp to tell who slapped first
        self.slap_timestamp = None

        # Endgame flag
        self.end_game = False

        # Difficulty Settings
        self.settings = {"setting_name": None, "delay_time": 0,
                         "auto_shuffle": False}
        with open("../../../etc/python3-ers/python3-ers.json", "r") as settings_file:
            self.settings_global = json.load(settings_file)

        self.home = os.getenv("HOME")
        if os.path.isfile(self.home + "/.config/ers/settings.json"):
            with open(HOME + "/.config/ers/settings.json", "r") as settings_file:
                settings_local = json.load(settings_file)
            self.settings = settings_local

        self.slap_info = {"timestamp": 0, "valid": False}
        self.key_commands = {"Enter": None, "Space": None, "Esc": None}

        # Start the game window
        self.comp_play_card()

    def main_window(self, widget, comp_play=None):
        """Set up main game window and game logic"""
        self.clear_window()

        self.key_commands = {"Enter": self.user_play_card, "Space": self.slap,
                             "Esc": None}

        tool_bar = Gtk.Toolbar.new()
        settings_item = Gtk.ToolItem()
        settings_item.set_is_important(True)
        settings_item.set_tooltip_markup("Edit your current settings")
        settings = Gtk.Button.new_from_icon_name("settings", 3)
        settings.connect("clicked", self.settings_dialog)
        settings_item.add(settings)
        tool_bar.add(settings_item)
        self.grid.attach(tool_bar, 0, 0, 4, 1)

        label = Gtk.Label()
        label.set_markup("<b>COMPUTER: cards left: %s</b>" % (self.ers.computer.get_size()))
        label.set_justify(Gtk.Justification.LEFT)
        label = self._set_default_margins(label)
        self.grid.attach(label, 0, 1, 4, 1)

        deck = self.generate_image()
        for each in deck:
            self.grid.attach(each, 1, 2, 2, 1)

        label1 = Gtk.Label()
        label1.set_markup("<b>YOU: cards left: %s</b>" % (self.ers.player1.get_size()))
        label1.set_justify(Gtk.Justification.LEFT)
        label1 = self._set_default_margins(label1)
        self.grid.attach(label1, 0, 3, 4, 1)

        play_button = Gtk.Button.new_from_icon_name("go-up", 5)
        play_button.set_label("Play Card")
        play_button.connect("clicked", self.user_play_card)
        self.grid.attach(play_button, 0, 4, 2, 1)

        slap_button = Gtk.Button.new_with_label("SLAP!!!")
        slap_button.connect("clicked", self.slap)
        self.grid.attach(slap_button, 2, 4, 2, 1)

        if comp_play == True:
            timer = threading.Timer(2, self.comp_play_card)
            timer.start()

        self.show_all()

    def _set_default_margins(self, widget):
        """Set default margin size"""
        widget.set_margin_start(10)
        widget.set_margin_end(10)
        widget.set_margin_top(10)
        widget.set_margin_bottom(10)
        return widget

    def settings_dialog(self, button):
        """Settings dialog"""
        self.clear_window()

        self.key_commands = {"Enter": None, "Space": None,
                             "Esc": self.main_window}

        self.show_all()

    def comp_play_card(self):
        """Pop a user's top card"""
        card = self.ers.computer.pop()
        if card == False:
            print("ENDGAME!")
            self.end_game = True
        else:
            self.ers.deck.prepend(card)
        if self.ers.deck.get_size() < 2:
            self.slap_info["valid"] = False
        else:
            top = self.ers.deck.peek(0)
            cards = [self.ers.deck.peek(1)]
            if self.ers.deck.get_size() >= 3:
                     cards.append(self.ers.deck.peek(2))
            if top.get_rank() in cards:
                self.slap_info["valid"] = True
                self.slap_info["timestamp"] = self.computer.slap(extra_delay=self.settings["delay_time"])
        self.main_window("clicked", comp_play=False)

    def user_play_card(self, widget):
        """Pop a user's top card"""
        card = self.ers.player1.pop()
        if card == False:
            print("ENDGAME!")
            self.end_game = True
        else:
            self.ers.deck.prepend(card)
        if self.ers.deck.get_size() < 2:
            self.slap_info["valid"] = False
        else:
            top = self.ers.deck.peek(0)
            cards = [self.ers.deck.peek(1)]
            if self.ers.deck.get_size() >= 3:
                     cards.append(self.ers.deck.peek(2))
            if top.get_rank() in cards:
                self.slap_info["valid"] = True
                self.slap_info["timestamp"] = self.computer.slap(extra_delay=self.settings["delay_time"])
        self.main_window("clicked")


    def slap(self, widget):
        """Get slap timestamp"""
        # We got a slap! Give the user the best chance of getting it by
        # recording the time now
        slap_time = time.time()
        self.clear_window()
        label = Gtk.Label()

        if self.slap_info["valid"]:
            if slap_time < self.slap_info["timestamp"]:
                label.set_markup("Cards go to you!")
                self.ers.award_cards(True)
            else:
                label.set_markup("Cards go to Computer!")
                self.ers.award_cards(False)
                label = self._set_default_margins(label)
                self.grid.attach(label, 0, 0, 2, 1)
        else:
            card = self.ers.player1.pop()
            self.ers.deck.append(card)
            label.set_markup("""<b>Not a valid slap.</b>

A penalty card has been added to the bottom of the pile.""")
            label.set_justify(Gtk.Justification.CENTER)
            label = self._set_default_margins(label)
            self.grid.attach(label, 0, 0, 2, 1)

        timer = threading.Timer(5, self.main_window, args=["clicked"])
        timer.start()

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

    def on_key_press_event(self, widget, event):
        """Handles keyy press events for window"""
        if event.keyval == Gdk.KEY_Escape:
            if self.key_commands["Esc"] != None:
                self.key_commands["Esc"]("clicked")
        elif event.keyval == Gdk.KEY_Return:
            if self.key_commands["Enter"] != None:
                self.key_commands["Enter"]("clicked")
        elif event.keyval == Gdk.KEY_space:
            if self.key_commands["Space"] != None:
                self.key_commands["Space"]("clicked")

    def generate_image(self):
        """Generate image to show for game"""
        deck = []
        deck_size = 4
        if self.ers.deck.get_size() >= deck_size:
            iterations = deck_size
        else:
            iterations = self.ers.deck.get_size()
        for each in range(iterations - 1, -1, -1):
            last_card = self.ers.deck.peek(each)
            if not last_card:
                deck.append(Gtk.Image.new_from_pixbuf(self.cards["back"]))
            else:
                if len(deck) == 0:
                    deck.append(Gtk.Image.new_from_pixbuf(self.cards[last_card.get_suit()][str(last_card.get_rank())]))
                else:
                    deck.insert(0, Gtk.Image.new_from_pixbuf(self.cards[last_card.get_suit()][str(last_card.get_rank())]))
        for each in range(iterations):
            deck[each] = self._set_default_margins(deck[each])
            deck[each].set_margin_start(75 * each)
        return deck


def load_image(suit, rank):
    """Load Image for card from disk"""
    prefix = "assets/"
    path = prefix + "%s_of_%s.svg" % (str(rank), suit)
    return GdkPixbuf.Pixbuf.new_from_file(path)

def show_window(game_object):
    """Show Main UI"""
    window = ERS_Window(game_object)
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", ERS_Window.exit)
    window.show_all()
    Gtk.main()
    window.exit("clicked")


if __name__ == "__main__":
    print("Loading data and initializing game ...")
    import game
    ers = game.ERS((0, False))
    ers.deal_cards()
    show_window(ers)

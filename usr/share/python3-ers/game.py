#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  game.py
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
"""ERS Game Logic and Code"""
import deck
import player
import comp_player


class ERS():
    """ERS Game Code"""
    def __init__(self, difficulty_settings):
        """Initialize Game Data"""
        self.computer = comp_player.Computer.new()
        self.player1 = player.Player.new()
        self.deck = deck.Deck()
        self.deck.shuffle()
        self._slap_offset = difficulty_settings[0]
        self._auto_shuffle = difficulty_settings[1]

    def deal_cards(self):
        """Seperate cards evenly between player"""
        for each in range(52):
            if each % 2:
                card = self.deck.peek(0)
                self.computer.append(self.deck.pop())
            else:
                card = self.deck.peek(0)
                self.player1.append(self.deck.pop())

    def award_cards(self, player):
        """Award cards to player

        Player should be a bool, True to Player, False to Computer
        """
        self.deck.reverse()
        if player:
            for each in range(self.deck.get_size()):
                self.player1.append(self.deck.pop())
        else:
            for each in range(self.deck.get_size()):
                self.computer.append(self.deck.pop())

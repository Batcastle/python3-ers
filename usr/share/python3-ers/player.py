#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  player.py
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
"""Player"""
import random
import deck


class Player(deck.Deck):
    """Player"""
    def new(self):
        """player setup"""
        self.__init__(auto_populate=False, visible=False)
        
    def bulk_add_cards(self, cards):
        """add cards in bulk"""
        for each in cards:
            self._deck.append(each)
            
    def play_card(self):
        """Play a card"""
        return self._deck.pop()
        

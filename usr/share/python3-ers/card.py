#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  card.py
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
"""Card Data"""

class Card():
    """Card Data"""
    def __init__(self, suit=None, rank=None):
        """Generate a card"""
        self._card_data = {"suit": None, "color": None, "rank": None, "face_card": False}
        
        # Set Suit
        if suit != None:
            if suit.lower() in ("hearts", "clubs", "spades", "diamonds"):
                self._card_data["suit"] = suit.lower()
                if suit.lower() in ("hearts", "diamonds"):
                    self._card_data["color"] = "red"
                else:
                    self._card_data["color"] = "black"
            else:
                raise ValueError("'%s' not a valid suit" % (suit))
        # Set rank
        if isinstance(rank, str):
            if ((rank.lower() in ("ace", "jack",
                                  "queen", "king")) or (rank.lower() in ("1", "2", "3", "4", "5",
                                                                         "6", "7", "8", "9",
                                                                         "10"))):
                if rank == 1:
                    rank = "ace"
                self._card_data["rank"] = str(rank).lower()
                if rank.lower() in ("ace", "jack", "queen", "king"):
                    self._card_data["face_card"] = True
            else:
                raise ValueError("'%s' not a valid rank" % (suit))
        elif isinstance(rank, int):
            if rank in range(1, 11):
                if rank == 1:
                    rank = "ace"
                    self._card_data["face_card"] = True
                self._card_data["rank"] = str(rank).lower()
            else:
                raise ValueError("'%s' not a valid rank" % (suit))
        elif rank != None:
            raise TypeError("'rank' not a valid type")
    
    def get_all_data(self):
        """Get Bulk card data"""
        return self._card_data
        
    def get_suit(self):
        """Return suit of card"""
        return self._card_data["suit"]
        
    def is_face_card(self):
        """Return whether card is a face card or not"""
        return self._card_data["face_card"]
        
    def get_color(self):
        """Return color of card"""
        return self._card_data["color"]
        
    def get_rank(self):
        """Return rank of card"""
        return self._card_data["rank"]
        
    

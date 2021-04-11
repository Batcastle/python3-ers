#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  desk.py
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
"""Deck Data and control"""
import card
import random


class Deck():
    """Card Deck"""
    def __init__(self, auto_populate=True, visible=True):
        """create out inital deck
        
        if auto_populate is True, an organized, 52-card deck is generated,
            if False, the Deck object is created but empty.
        """
        self._deck = []
        self._face_cards = ("ace", "jack", "queen", "king")
        self._max_size = 52
        self._visible = bool(visible)
        if auto_populate:
            for suit in ("hearts", "diamonds", "clubs", "spades"):
                for num_rank in range(2, 11):
                    self._deck.append(card.Card(suit=suit, rank=num_rank))
                for face_rank in self._face_cards:
                    self._deck.append(card.Card(suit=suit, rank=face_rank))
    
    def pop(self):
        """Get top card in deck"""
        return self._deck.pop()
                
    def append(self, new):
        """Append new to deck, if deck < max_size
        
        Returns False if deck is at max size
        """
        if len(self._deck) < self._max_size:
            if isinstance(new, card.Card):
                self._deck.append(new)
            else:
                raise TypeError("Not of type card.Card")
        else:
            return False
    
    def get_size(self):
        """get current size of deck"""
        return len(self._deck)
        
    def peek(self, spot=0):
        """get top card in deck, if peaking enabled
        
        returns False if peeking disabled
        """
        if self._visible:
            return self.deck[spot]
        else:
            return False
            
    def shuffle(self, iterations=1000):
        """Shuffle the deck"""
        for each in range(iterations):
            new_deck = [None] * 52
            for each in self._deck:
                while True:
                    point = random.randint(0, 51)
                    if new_deck[point] is None:
                        new_deck[point] = each
                        break
                self._deck = new_deck

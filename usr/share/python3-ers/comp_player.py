#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  comp_player.py
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
"""Computer Player"""
import random
import player


class Computer(player.Player):
    """Computer Player"""
        
    def slap(self, extra_delay=0):
        """slapping time out"""
        if not isinstance(extra_delay, (int, float)):
            raise TypeError("Not an int or float")
        return 0.3 + extra_delay
        
    
        

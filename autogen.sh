#!/bin/bash
# -*- coding: utf-8 -*-
#
#  autogen.sh
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
if [ "$1" == "" ]; then
	git submodule init
	git submodule update
	echo -e "Run \`./autogen.sh update' to update submodules and other dependencies"
elif [ "$1" == "update" ]; then
	git submodule update --remote playing-cards-assets
fi

#!/usr/bin/env python3
# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math
from boxes import *

class ResourceCardTray(Boxes):
    """Divided tray with an open front for holding cards."""

    ui_group = "Tray"

    description = """Designed to hold resource cards in a board game."""

    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        #self.buildArgParser("x", "y", "h")

        self.argparser.add_argument(
            "--card_width",
            type=float,
            default=58,
            help="Width of the card, add an extra mm or 2",
        )

        self.argparser.add_argument(
            "--card_length",
            type=float,
            default=90,
            help="Length of the card",
        )

        self.argparser.add_argument(
            "--card_stack",
            type=float,
            default=35,
            help="Height of the card stack",
        )

        self.argparser.add_argument(
            "--card_slots",
            type=float,
            default=6,
            help="Number of card slots",
        )
        self.argparser.add_argument(
            "--radius",
            type=float,
            default=10,
            help="Radius of divider end",
        )

    def CardDividers(self, y, h, r, edges="feef", move=None):
        t = self.thickness
        if self.move(y+2*t, h+t, move, True):
            return
        callback = None;
        self.moveTo(t, t)
        self.cc(callback, 0)
        #self.edges["e"](t)      #Bottom Edge
        self.edges[edges[0:1]](y)      #Bottom Edge
        self.corner(90, 0)
        self.cc(callback, 1)
        self.edges[edges[1:2]](h - r )        #Right Edge
        self.corner(90, r)                #Top right radius
        self.cc(callback, 2)
        self.edge(y - r )        #width across the top
        self.corner(90, 0)
        self.cc(callback, 3)
        self.cc(callback, 4)
        self.edges[edges[3:4]](h)  #Left Edge
        self.corner(90)
        self.move(y+2*t, h+t, move)

    def CardDividerEnds(self, y, h, r, edges="feef", move=None):
        t = self.thickness
        if self.move(y+2*t, h+t, move, True):
            return
        callback = None;
        self.moveTo(t, t)
        self.cc(callback, 0)
        self.edges["e"](t)      #Bottom Edge
        self.edges[edges[0:1]](y)      #Bottom Edge
        self.corner(90, 0)
        self.cc(callback, 1)
        self.edges[edges[1:2]](h - r )        #Right Edge
        self.corner(90, r)                #Top right radius
        self.cc(callback, 2)
        self.edge(y - r + t)        #width across the top
        self.corner(90, 0)
        self.cc(callback, 3)
        self.cc(callback, 4)
        self.edges[edges[3:4]](h)  #Left Edge
        self.corner(90)
        self.move(y+2*t, h+t, move)


    def CardTrayBack(self, x, y, edges, callback, move):
        t = self.thickness
        if self.move(y+2*t, y+t, move, True):
            return
        self.moveTo(t, t)
        self.edges[edges[0:1]](x+t)       #Bottom Edge
        self.corner(90, 0)
        self.edges[edges[1:2]](y)     #Right Edge
        self.corner(90)                 #Top right radius
        self.edges[edges[2:3]](x+t)       #Top Edge
        self.corner(90, 0)
        self.edges[edges[3:4]](y)     #Left Edge
        self.corner(90)
        xPos = self.card_width + (self.thickness/2)
        i = 1
        while i <= self.card_slots-1:
            self.fingerHolesAt(xPos, self.thickness, y, 90)
            xPos = xPos + self.card_width + self.thickness
            i += 1
        self.move(y+2*t, y+(t*2), move)


    def CardTrayBase(self, x, y, edges, callback, move):
        t = self.thickness
        if self.move(y+2*t, y+t, move, True):
            return
        self.moveTo(t, t)
        self.edges[edges[0:1]](x)       #Bottom Edge
        self.corner(90, 0)
        self.edges[edges[1:2]](y)       #Right Edge
        self.corner(90)                 #Top right radius
        self.edges[edges[2:3]](x)       #Top Edge
        self.corner(90, 0)
        self.edges[edges[3:4]](y)       #Left Edge
        self.corner(90)

        xPos = self.card_width + (self.thickness/2)
        i = 1
        while i <= self.card_slots-1:
            self.fingerHolesAt(xPos, 0, y, 90)
            xPos = xPos + self.card_width + self.thickness
            i += 1

        self.move(y+2*t, y+(t*2), move)

    def render(self):
        x = ((self.card_width + self.thickness) * self.card_slots) - self.thickness
        y = self.card_length + self.thickness
        h = self.card_stack
        r = self.radius

        t = self.thickness
        d2 = None

        #Render middle dividers
        cards = self.card_slots - 1
        i = 1
        while i <= cards:
            self.CardDividers(y, h, r, "feef", "up")  #Generate the dividers between cards
            i += 1

        #Render Ends
        self.CardDividerEnds(y, h+self.thickness , r, "FeeF", "up")  #Generate the dividers between cards
        self.CardDividerEnds(y, h+self.thickness , r, "FeeF", "up")  #Generate the dividers between cards

        #REnder base and back
        self.CardTrayBase( x, y, "efff", None, "up")    #base plate
        self.CardTrayBack( x, h, "Ffef", None, "up")    #backwall

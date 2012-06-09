# Export finite state machines - base infrastructure.
#
# Based on a script by Unai Estebanez Sevilla:
#
#     From: Unai Estebanez <unai unainet net>
#     To: dia-list gnome org
#     Subject: python script to export finite state machines
#     Date: Tue, 7 Jul 2009 15:05:10 +0200
#
#     https://mail.gnome.org/archives/dia-list/2009-July/msg00005.html
#
# Changes by Tomas Pospisek <tpo_deb@sourcepole.ch>
#
# Copyright (c) 2009-2012, Unai Estebanez Sevilla, Tomas Pospisek
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


import dia

class Transition :
    def __init__(self) :
        self.trigger = ""
        self.action = ""
        self.guard = ""
        self.source = ""
        self.target = ""

    def set_source(self, state):
        self.source = state

    def set_target(self, state):
        self.target = state

    def set_action(self, action):
        self.action = action

    def set_trigger(self, trigger):
        self.trigger = trigger

    def set_guard(self, guard):
        self.guard = guard

class State :
    def __init__(self) :
        self.name = ""
        self.iaction = ""
        self.oaction = ""
        self.type = 0
        self.aux = ""

    def set_name(self, name):
        self.name = name

    def set_input_action(self, action):
        if action == "(NULL)":
            self.iaction = ""
        else:
            self.iaction = action

    def set_output_action(self, action):
        if action == "(NULL)":
            self.oaction = ""
        else:
            self.oaction = action

    def set_do_action(self, action):
        if action == "(NULL)":
            self.doaction = ""
        else:
            self.doaction = action

    def set_type(self, type):
        self.type = type

    def set_aux(self, aux):
        self.aux = aux


class SimpleSTM:
    """This class holds a simplified representation of
    the state machine expressed via the dia UML diagram
    and as such lends itself to base your renderer on"""

    def __init__(self):
        self.states = {}
        self.transitions = []

    def parse(self, data):
        for layer in data.layers :
            for o in layer.objects :
                if o.type.name == "UML - State" :
                    state = State()
                    # State properties are:
                    # [ obj_pos,     obj_bb,      elem_corner, elem_width,
                    #   elem_height, type,        line_colour, fill_colour,
                    #   text_font,   text_height, text_colour, text,
                    #   entry_action,do_action,   exit_action               ]

                    # ----- set name
                    state.set_name(o.properties["text"].value.text.strip())

                    # ----- set input action
                    try :
                        p = o.properties["entry_action"].value
                    except :
                        p = None
                    state.set_input_action(str(p))
                     
                    # ----- set output action
                    try :
                        p = o.properties["exit_action"].value
                    except :
                        p = None
                    state.set_output_action(str(p))

                    # ----- set do action
                    try :
                        p = o.properties["do_action"].value
                    except :
                        p = None
                    state.set_do_action(str(p))

                    state.set_type(STANDARD_STATE)
                    self.states[state.name] = state
                #elif o.type.name == "UML - State Term" :
                    # State Term properties are:
                    # [ obj_pos,    obj_bb,      elem_corner,
                    #   elem_width, elem_height, is_final     ]
                elif o.type.name == "UML - Transition" :
                    # Transition properties are:
                    # [ obj_pos,        obj_bb,         orth_points,
                    #   orth_orient,    orth_autoroute, trigger,
                    #   action,         guard,          trigger_text_pos,
                    #   guard_text_pos, direction_inverted                ]
                    transition = Transition()
                    source = o.handles[0].connected_to.object
                    target = o.handles[1].connected_to.object
                    if source.type.name ==  "UML - State Term":
                        if not source.properties["is_final"].value :
                            transition.set_source("INITIAL_STATE")
                    elif source.type.name == "UML - State":
                        transition.set_source(source.properties["text"].value.text)
                    else:
                        transition.set_source("Unknown source")

                    if target.type.name ==  "UML - State Term":
                        if target.properties["is_final"].value :
                            transition.set_target("FINAL_STATE")
                    elif target.type.name == "UML - State":
                        transition.set_target(target.properties["text"].value.text)
                    else:
                        transition.set_source("Unknown target")
                    
                    try:
                        trigger = o.properties["trigger"].value
                    except:
                        trigger = ""
                    transition.set_trigger(str(trigger))

                    try:
                        action = o.properties["action"].value
                    except:
                        action = ""
                    transition.set_action(str(action))

                    try:
                        guard = o.properties["guard"].value
                    except:
                        guard = ""

                    transition.set_guard(str(guard))
                    self.transitions.append(transition)

INITIAL_STATE, STANDARD_STATE, FINAL_STATE = range(3)

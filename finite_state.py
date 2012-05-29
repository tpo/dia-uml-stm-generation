# python script to export finite state machines
# 
#     From: Unai Estebanez <unai unainet net>
#     To: dia-list gnome org
#     Subject: python script to export finite state machines
#     Date: Tue, 7 Jul 2009 15:05:10 +0200
# 
# Hi,
# This is my script to export from a DIA UML state machine diagram to a neutral text format, later I use a program to convert from this neutra textl to a C language state machine.
# Output of this script contents file format information.
# I do not export the "do_action" because my C FSM(Finite State Machine) implementation does not support it but its really easy to add it.
# Maybe this script will be usefull to someone:
#
# https://mail.gnome.org/archives/dia-list/2009-July/msg00005.html

import dia

class Transition :
    def __init__(self) :
        self.trigger = ""
        self.action = ""
        self.source = ""
        self.target = ""
    def set_source(self, state):
        self.source = state
    def set_target(self, state):
        self.target = state
    def set_action(self, action):
        self.action = ""
    def set_trigger(self, trigger):
        self.trigger = trigger
       
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
    def set_type(self, type):
        self.type = type               
    def set_aux(self, aux):
        self.aux = aux       
       
class TxtDiagramRenderer:
    def __init__(self):
        self.filename = ""       
        self.states = {}
        self.transitions = []
    def begin_render (self, data, filename):
       
        self.filename = filename               
        for layer in data.layers :
            for o in layer.objects :                           
                if o.type.name == "UML - State" :
                    state = State()
                    # las propiedades son: ['obj_pos', 'obj_bb', 'elem_corner', 'elem_width' ,'elem_height', 'type','line_colour', 'fill_colour', 'text_font', 'text_height', 'text_colour', 'text', 'entry_action', 'do_action', 'exit_action' ]
                    state.set_name(o.properties["text"].value.text.strip())                                       
                    try :
                        p = o.properties["entry_action"].value                       
                    except :
                        p = None                   
                    state.set_input_action(str(p))
                     
                    try :
                        p = o.properties["exit_action"].value                       
                    except :
                        p = None                                       
                    state.set_output_action(str(p))                   
                    state.set_type(STANDARD_STATE)
                    self.states[state.name] = state                   
                #elif o.type.name == "UML - State Term" :   
                    # las propiedades son:[ 'obj_pos', 'obj_bb', 'elem_corner', 'elem_width', 'elem_height', 'is_final']                   
                elif o.type.name == "UML - Transition" :
                    #las propiedades son: ['obj_pos', 'obj_bb', 'orth_points', 'orth_orient', 'orth_autoroute', 'trigger', 'action', 'guard', 'trigger_text_pos', 'guard_text_pos', 'direction_inverted']
                    transition = Transition()                   
                    source = o.handles[0].connected_to.object
                    target = o.handles[1].connected_to.object
                    if source.type.name ==  "UML - State Term":
                        if not source.properties["is_final"].value :
                            transition.set_source("INITIAL_STATE")
                    elif source.type.name == "UML - State":
                        transition.set_source(source.properties["text"].value.text)
		    else:
                        transition.set_source("source unknown bullshit")

                    if target.type.name ==  "UML - State Term":                       
                        if target.properties["is_final"].value :
                            transition.set_target("FINAL_STATE")
                    elif target.type.name == "UML - State":
                        transition.set_target(target.properties["text"].value.text)
		    else:
                        transition.set_source("target unknown bullshit")
                    
                    try:
                        trigger = o.properties["trigger"].value
                    except:
                        trigger = ""
                    transition.set_trigger(str(trigger))
                    try:
                        action = ""
                    except:
                        action = ""
                        transition.set_action(str(action))
                    self.transitions.append(transition)
                   
    def end_render(self) :       
        f = open(self.filename, "w")       
        f.write("#Machine generated file, do not edit!!!\n#Generated by sm_export.py script for DIA\n")
        f.write("#Format is: <comments zone>EOL[STATES]EOL<state>EOL....<state>EOL[TRANSITIONS]EOL<transition>EOL...<transition>EOLEOF\n")
        f.write("#Where:\n")
        f.write("#\t<comments zone> is a line that begins with \'#\'\n")
        f.write("#\t<state> is a line with comma separated values: state_name,input_action,output_action\n")
        f.write("#\t<transition> is a line with comma separated values: source_state,target_state,trigger,action\n")
        f.write("#\t[STATES] is states zone begin tag\n")
        f.write("#\t[TRANSITIONS] is transitions zone begin tag\n")
        f.write("#\tEOL means End Of Line and EOF means End Of File\n")
        f.write("#-------------------------------------------------------------------------------\n")
        f.write("[STATES]\n")
        for key in self.states.keys():
            state = self.states[key]
            f.write("%s, %s, %s\n" % (state.name, state.iaction, state.oaction))
        f.write("[TRANSITIONS]\n")
        for transition in self.transitions:
            f.write("%s, %s, %s, %s\n" % (transition.source, transition.target, transition.trigger, transition.action))
        f.close()
        self.states = {}
        self.transitions = []

INITIAL_STATE, STANDARD_STATE, FINAL_STATE = range(3)

# dia-python keeps a reference to the renderer class and uses it on demand
dia.register_export("State Machine Textual Dump", "txt", TxtDiagramRenderer())

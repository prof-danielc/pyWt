from __future__ import print_function

# imports for HelloApplication
from eu.webtoolkit.jwt import Side
from eu.webtoolkit.jwt import Signal
from eu.webtoolkit.jwt import WApplication
from eu.webtoolkit.jwt import WBreak
from eu.webtoolkit.jwt import WEnvironment
from eu.webtoolkit.jwt import WLineEdit
from eu.webtoolkit.jwt import WPushButton
from eu.webtoolkit.jwt import WText

class ButtonListener(Signal.Listener):
    def __init__(self, tmp1, tmp2):
        self.greeting = tmp1
        self.nameEdit = tmp2

    def trigger(self):
        self.greeting.setText("Ola, " + self.nameEdit.getText() + "! :)")
        
class MyWtApplication(WApplication):
    def __init__(self, env):
        WApplication.__init__(self, env)

        self.setTitle("Teste Python")

        self.getRoot().addWidget(WText("Seu nome, senhor? "))
        nameEdit = WLineEdit(self.getRoot())
        nameEdit.setFocus()

        button = WPushButton("Tocai!", self.getRoot())
        button.setMargin(5, Side.Left)

        self.getRoot().addWidget(WBreak())

        greeting = WText(self.getRoot())
        
        # using a class
        buttonListener = ButtonListener(greeting, nameEdit)
        
        # using an inline class similar to Java's anonymous class approach
        # python limits lambda functions to a single line and in this case the called function must return void (have no return value)
        #def teste2():
            #greeting.setText("Ola, " + nameEdit.getText() + "! :)") # setText has a boolean return value so it can't be placed in lambda for trigger
        #buttonListener = type("InlineButtonListener", (Signal.Listener,object), {"greeting":greeting, "trigger": lambda self: teste2() })()

        button.clicked().addListener(self, buttonListener)
        
        

import sys

from PySide6.QtCore import Signal, QEvent, QRect, SIGNAL
from PySide6.QtStateMachine import QStateMachine, QState, QEventTransition
from PySide6.QtWidgets import *

app = QApplication(sys.argv)
button = QPushButton()
machine = QStateMachine()

off = QState()
off.assignProperty(button, 'text', 'Off')
off.setObjectName('off')

on = QState()
on.setObjectName('on')
on.assignProperty(button, 'text', 'On')

off.addTransition(button, SIGNAL('clicked()'), on)
# Let's use the new style signals just for the kicks.
on.addTransition(button.clicked, off)

machine.addState(off)
machine.addState(on)
machine.setInitialState(off)
machine.start()
button.resize(100, 50)
button.show()
sys.exit(app.exec_())
import sys
try:
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import QWidget, QHBoxLayout, QComboBox


class DefaultLabelComboBox(QWidget):
    def __init__(self, parent=None, items=[], attribute = None):
        super(DefaultLabelComboBox, self).__init__(parent)

        # Thinkman edit here
        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.items = items

        self.cb.addItems(self.items)
        
        self.attribute = attribute

        if attribute == 'label':
            self.cb.currentIndexChanged.connect(parent.default_label_combo_selection_changed)
        elif attribute == 'staff_security':
            self.cb.currentIndexChanged.connect(parent.staff_security_combo_selection_changed)
        elif attribute == 'gender':
            self.cb.currentIndexChanged.connect(parent.gender_combo_selection_changed)
        elif attribute == 'age':
            self.cb.currentIndexChanged.connect(parent.age_combo_selection_changed)
        elif attribute == 'QA':
            self.cb.currentIndexChanged.connect(parent.QA_combo_selection_changed)

        self.dict_item = {}

        for i in range(len(items)):
            self.dict_item[items[i]] = i

        layout.addWidget(self.cb)
        self.setLayout(layout)

    def set_selected_text(self, attribute):
        # self.cb.setPlaceholderText(text)
        self.cb.setCurrentIndex(self.dict_item[attribute])
    # def set_selected_index(self, index):
    #     # self.cb.setPlaceholderText(text)
    #     self.cb.setCurrentIndex(1)


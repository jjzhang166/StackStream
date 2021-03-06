# The MIT License (MIT)
#
# Copyright (c) 2016 Erik Hvatum
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Authors: Erik Hvatum <ice.rikh@gmail.com>

from pathlib import Path
from PyQt5 import Qt
import sys
from ris_widget import om
from list_role_model import ListRoleModel

class OutlinePoint(Qt.QObject):
    x_Changed = Qt.pyqtSignal(float)
    y_Changed = Qt.pyqtSignal(float)

    def __init__(self, x=0, y=0, parent=None):
        super().__init__(parent)
        self._x = float(x)
        self._y = float(y)

    def __repr__(self):
        return 'OutlinePoint({}, {})'.format(self._x, self._y)

    def getX_(self):
        return self._x

    def setX_(self, x):
        x = float(x)
        if abs(x - self._x) > 0.00001:
            self._x = x
            self.x_Changed.emit(x)

    x_ = Qt.pyqtProperty(float, fget=getX_, fset=setX_, notify=x_Changed)

    def getY_(self):
        return self._y

    def setY_(self, y):
        if abs(y - self._y) > 0.00001:
            self._y = y
            self.y_Changed.emit(y)

    y_ = Qt.pyqtProperty(float, fget=getY_, fset=setY_, notify=y_Changed)

class OutlinePointList(om.UniformSignalingList):
    def take_input_element(self, obj):
        if isinstance(obj, OutlinePoint):
            return obj
        elif isinstance(obj, (Qt.QPointF, Qt.QPoint)):
            return OutlinePoint(obj.x(), obj.y())
        else:
            i = iter(obj)
            return OutlinePoint(next(i), next(i))

class PointListModel(ListRoleModel):
    @Qt.pyqtSlot(float, float)
    def append(self, x, y):
        self.signaling_list.append(OutlinePoint(x, y))

    @Qt.pyqtSlot(int)
    def delAtIndex(self, idx):
        del self.signaling_list[idx]

_QML_TYPES_REGISTERED = False

class PickerWidget(Qt.QQuickWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        global _QML_TYPES_REGISTERED
        if not _QML_TYPES_REGISTERED:
            Qt.qmlRegisterType(OutlinePoint)
            Qt.qmlRegisterType(ListRoleModel)
            _QML_TYPES_REGISTERED = True
        self.setResizeMode(Qt.QQuickWidget.SizeRootObjectToView)
        self.point_list = OutlinePointList()
        self.point_list_model = PointListModel(('x_', 'y_'), self.point_list)
        self.rootContext().setContextProperty("pointListModel", self.point_list_model)
        self.setSource(Qt.QUrl(str(Path(__file__).parent / 'PyQmlProof.qml')))
        self.show()

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    picker_widget = PickerWidget()
    app.exec_()

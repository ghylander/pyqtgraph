import numpy as np

from . import functions as fn
from .Qt import QtGui
from .Vector import Vector


class Transform3D(QtGui.QMatrix4x4):
    """
    Extension of QMatrix4x4 with some helpful methods added.
    """
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], (list, tuple, np.ndarray)):
                args = [x for y in args[0] for x in y]
                if len(args) != 16:
                    raise TypeError("Single argument to Transform3D must have 16 elements.")
            elif isinstance(args[0], QtGui.QMatrix4x4):
                args = list(args[0].copyDataTo())
        
        QtGui.QMatrix4x4.__init__(self, *args)
        
    def matrix(self, nd=3):
        if nd == 3:
            return np.array(self.copyDataTo()).reshape(4,4)
        elif nd == 2:
            m = np.array(self.copyDataTo()).reshape(4,4)
            m[2] = m[3]
            m[:,2] = m[:,3]
            return m[:3,:3]
        else:
            raise Exception("Argument 'nd' must be 2 or 3")

    def map(self, obj):
        """
        Extends QMatrix4x4.map() to allow mapping (3, ...) arrays of coordinates
        """
        if isinstance(obj, np.ndarray) and obj.shape[0] in (2,3):
            if obj.ndim >= 2:
                return fn.transformCoordinates(self, obj)
            elif obj.ndim == 1:
                v = QtGui.QMatrix4x4.map(self, Vector(obj))
                return np.array([v.x(), v.y(), v.z()])[:obj.shape[0]]
        elif isinstance(obj, (list, tuple)):
            v = QtGui.QMatrix4x4.map(self, Vector(obj))
            return type(obj)([v.x(), v.y(), v.z()])[:len(obj)]
        else:
            retval = QtGui.QMatrix4x4.map(self, obj)
            if not isinstance(retval, type(obj)):
                return type(obj)(retval)
            return retval

    def inverted(self):
        inv, b = QtGui.QMatrix4x4.inverted(self)
        return Transform3D(inv), b

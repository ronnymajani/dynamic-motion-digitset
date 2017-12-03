# TODO: Fill in this file

from PyQt4 import QtGui
import pygame
import logging

logging.basicConfig(level=logging.DEBUG)

pygame.init()


class PanelMap(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedWidth(parent.width())  # Set the width to match parent
        self.setFixedHeight(parent.height())  # Set the height to match parent

        # Initiate Logger
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Canvas Width = %d, Height = %d", self.width(), self.height())

        # Attach pygame buffer to the QtImage widget (canvas)
        self.surface = pygame.Surface((self.width(), self.height()))
        data = self.surface.get_buffer().raw
        self.canvas = QtGui.QImage(data, self.width(), self.height(), QtGui.QImage.Format_RGB32)

        # Set BG Color
        self.background_color = (255, 255, 255, 255)
        self.surface.fill(self.background_color)

    def paintEvent(self, event):
        data = self.surface.get_buffer().raw
        self.canvas = QtGui.QImage(data, self.width(), self.height(), QtGui.QImage.Format_RGB32)
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, self.canvas)
        qp.end()

    def draw(self):
        self.surface.fill(self.background_color)
        # self.car.graphicDriver.draw(self.surface)

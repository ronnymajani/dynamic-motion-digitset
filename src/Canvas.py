# TODO: Fill in this file

from PyQt4 import QtGui
import pygame
import logging

logging.basicConfig(level=logging.DEBUG)

pygame.init()


class Canvas(QtGui.QWidget):
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

        self.color = (150, 150, 150)
        self.lineWidth = 1
        self.pointRadius = 3

        # Set BG Color
        self.background_color = (255, 255, 255, 255)
        self.surface.fill(self.background_color)

    def paintEvent(self, event):
        """QT Paint Event; This is called by the context; We just copy over the pygame buffer to the QT canvas"""
        data = self.surface.get_buffer().raw
        self.canvas = QtGui.QImage(data, self.width(), self.height(), QtGui.QImage.Format_RGB32)
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, self.canvas)
        qp.end()

    def draw(self, points):
        """Draw in the pygame buffer"""
        self.surface.fill(self.background_color)

        # Make sure we actually have point to draw
        if len(points < 1):
            return

        # draw first point
        pygame.draw.circle(self.surface, self.color, points[0], self.pointRadius, self.lineWidth)
        # draw lines
        if len(points) > 1:
            for i in range(1, len(points)):
                curr_point = points[i]
                prev_point = points[i-1]
                # draw point
                pygame.draw.circle(self.surface, self.color, curr_point, self.pointRadius, self.lineWidth)
                # draw line between current and previous points
                pygame.draw.line(self.surface, self.color, prev_point, curr_point, self.lineWidth)


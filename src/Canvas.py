from PyQt4 import QtGui
import pygame
import logging

logging.basicConfig(level=logging.DEBUG)

pygame.init()


class Canvas(QtGui.QWidget):
    def __init__(self, parent):
        """
        :param parent: the QT window of which this widget is a child of
        """
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

        self.color = (0, 0, 0)
        self.lineWidth = 10
        self.pointRadius = 5

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

    def draw(self, points, resolution_x, resolution_y, resolution_p):
        """
        Draw in the pygame buffer
        :param points: a list of 3d tuples in the form (X, Y, P) to draw
        :param resolution_x: the horizontal resolution of the device
        :param resolution_y: the vertical resolution of the device
        :param resolution_p: the pressure resolution of the device
        """
        self.surface.fill(self.background_color)

        # Make sure we actually have point to draw
        if len(points) < 1:
            return

        # Clarification:
        # Each "point" in the list is a tuple in the form (X, Y, P)
        # and we are only interested in the X and Y values when drawing

        scale_x = float(self.canvas.width()) / float(resolution_x)
        scale_y = float(self.canvas.height()) / float(resolution_y)
        scale_p = float(self.pointRadius) / float(resolution_p)

        def scale(point):
            return int(point[0]*scale_x), int(point[1]*scale_y)

        # draw first point
        prev_point = scale(points[0])
        pygame.draw.circle(self.surface, self.color, prev_point, 1+int(points[0][2]*scale_p))
        # draw lines
        if len(points) > 1:
            for i in range(1, len(points)):
                curr_point = scale(points[i])
                # draw point
                circle_radius = 1+int(points[i][2]*scale_p)
                pygame.draw.circle(self.surface, self.color, curr_point, circle_radius)
                # draw line between current and previous points
                line_width = 5+int(points[i][2] * 2 * scale_p)  # chosen by trial and error
                pygame.draw.line(self.surface, self.color, prev_point, curr_point, line_width)
                # set current point as "previous point"
                prev_point = curr_point



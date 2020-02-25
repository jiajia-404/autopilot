"""
.. module:: autopilot
   :synopsis: Main routine for autopilot package
.. moduleauthor:: Adam Moss <adam.moss@nottingham.ac.uk>
"""

import threading


class AutoPilot:

    def __init__(self, capture, front_wheels, back_wheels, camera_control):

        # Try getting camera from already running capture object, otherwise get a new CV2 video capture object
        try:
            self.camera = capture.camera
        except:
            import cv2
            self.camera = cv2.VideoCapture(0)

        # These are picar controls
        self.front_wheels = front_wheels
        self.back_wheels = back_wheels
        self.camera_control = camera_control

        # Thread variables
        self._started = False
        self._terminate = False
        self._thread = None

    def start(self):
        """
        Starts autopilot in separate thread
        :return:
        """
        if self._started:
            print('[!] Self driving has already been started')
            return None
        self._started = True
        self._terminate = False
        self._thread = threading.Thread(target=self._drive, args=())
        self._thread.start()

    def stop(self):
        """
        Stops autopilot
        :return:
        """
        self._started = False
        self._terminate = True
        if self._thread is not None:
            self._thread.join()

    def _drive(self):
        """
        Drive routine for autopilot. Processes frame from camera
        :return:
        """
        while not self._terminate:
            ret, frame = self.camera.read()

            # !! Use machine learning to determine angle and speed (if necessary - you may decide to use fixed speed) !!

            speed = 30
            angle = self.front_wheels._straight_angle

            # !! End of machine learning !!

            # Do not allow angle or speed to go out of range
            angle = max(min(angle, self.front_wheels._max_angle), self.front_wheels._min_angle)
            speed = max(min(speed, 100), -100)

            # Set picar angle and speed
            self.front_wheels.turn(angle)
            self.back_wheels.forward()
            self.back_wheels.speed = speed

        self.back_wheels.speed = 0

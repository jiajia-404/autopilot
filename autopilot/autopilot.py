"""
.. module:: autopilot
   :synopsis: Main routine for autopilot package
.. moduleauthor:: Adam Moss <adam.moss@nottingham.ac.uk>
"""

import threading


class AutoPilot:

    def __init__(self, capture, front_wheels, back_wheels, camera_control,
                 debug=False, test_mode=False):
        model=tf.keras.models.load_model(model_path="/home/pi/SunFounder_PiCar-V/model_epo50.tflite")

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

        self.debug = debug
        self.test_mode = test_mode

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
            

         def img_preprocess(image):
             height, _, _ = image.shape
             image = image[int(height*0.15):,:,:]  # remove top half of the image, as it is not relavant for lane following
             image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)  # Nvidia model said it is best to use YUV color space
             image = cv2.GaussianBlur(image, (3,3), 0)
             image = cv2.resize(image, (200,120)) # input image size (200,66) Nvidia model
             image = image / 255 # normalizing, the processed image becomes black for some reason.  do we need this?
             return image
          
         frame = img_preprocess(frame)
            # !! Use machine learning to determine angle and speed (if necessary - you may decide to use fixed speed) !!

            angle = model.predict(frame)
            speed = 30
            # angle = 90

            # !! End of machine learning !!

            angle = int(angle)
            speed = int(speed)

            if self.debug:
                print('Speed: %d, angle: %d ' % (angle, speed))

            if not self.test_mode:

                # Do not allow angle or speed to go out of range
                angle = max(min(angle, self.front_wheels._max_angle), self.front_wheels._min_angle)
                speed = max(min(speed, 100), -100)

                # Set picar angle and speed
                self.front_wheels.turn(angle)
                self.back_wheels.forward()
                self.back_wheels.speed = speed
                 

        self.back_wheels.speed = 0
        

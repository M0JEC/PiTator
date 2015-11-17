#!/usr/bin/env python3

import logging
import os
import RPi.GPIO as GPIO
import socket
import sys
import time


class ConnectionFinished(Exception):
    pass


class ActionHandler(object):
    """
    Handle messages received on the socket
    """
    def __init__(self, rotator):
        self.rotator = rotator

    def handle_p_set(self, azimuth, elevation):
        self.rotator.xt = float(azimuth)
        self.rotator.yt = float(elevation)
        logging.info("set to {}:{}".format(azimuth, elevation))
        self.rotator.move()

    def handle_p_get(self):
        return [str(self.rotator.az), str(self.rotator.ele)]

    def close_connection(self):
        raise ConnectionFinished()

    def handle_message(self, cmd, *params):
        action_map = {
            'P': self.handle_p_set,
            'p': self.handle_p_get,
            'q': self.close_connection
        }
        return "\n".join(action_map[cmd](*params) or []) or "\n"


class Rotator(object):
    def __init__(self):
        self.ele = 0  # Elevation
        self.az = 0  # Azimuth
        self.xc = 6.666  # X axis correction factor (degrees per second)
        self.yc = 1.875  # Y axis Correction Factor (degrees per second)
        self.yt = 0  # Y axis Target position
        self.xt = 0  # X axis Target position

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Setup IO to Pi numbering
        GPIO.setup(17, GPIO.OUT)  # Setup Relay pins as OUTPUTS
        GPIO.setup(27, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)

    def move(self):
        """
        Direction test - Decides which routine to call for movement
        """
        # subroutine to position the X axis 90 degrees off when at near
        # vertical >85 Deg (saves time on overhead passes)
        old_xt = self.xt
        if self.yt >= 85:
            logging.debug('old x = {}'.format(self.xt))

            # Decides if the current position is above or below the mid
            # position on the rotator.
            if self.xt >= 180:
                self.xt -= 90
            else:
                self.xt += 90

            logging.debug('new x = {}'.format(self.xt))
            self.xt = nxt

        if self.xt >= self.az:  # RIGHT test
            if self.yt >= self.ele:  # UP Test
                self.ur()
            else:  # If RIGHT and not UP must be DOWN and Right
                self.dr()
        elif self.xt <= self.az:  # LEFT test
            if self.yt >= self.ele:  # UP test
                self.ul()
            else:   # If LEFT and not UP must be DOWN and Left
                self.dl()
        self.xt = old_xt

    def ul():
        """
        Move Up and/or Left
        """
        yseconds = (self.yt - self.ele) * (1 / self.yc)
        logging.debug('Y: target {} degrees'.format(self.yt))
        logging.debug('moving up for {} seconds'.format(yseconds))

        xseconds = (self.az - self.xt) * (1 / self.xc)
        logging.debug('X: target {} degrees'.format(self.xt))
        logging.debug('moving left for {} seconds'.format(xseconds))

        GPIO.output(17, True)
        GPIO.output(18, False)
        GPIO.output(27, True)
        GPIO.output(22, False)
        if xseconds > yseconds:
            time.sleep(yseconds)
            GPIO.output(18, True)
            time.sleep(xseconds - yseconds)
            GPIO.output(22, True)
        else:
            time.sleep(xseconds)
            GPIO.output(22, True)
            time.sleep(yseconds - xseconds)
            GPIO.output(18, True)

        self.ele = self.yt
        logging.info('elevation is {}'.format(self.ele))

        self.az = self.xt
        logging.debug('azimuth is {}'.format(self.az))

    def ur(self):
        """
        Move Up and/or Right
        """
        yseconds = (self.yt - self.ele) * (1 / self.yc)
        logging.debug('Y: target {} degrees'.format(self.yt))
        logging.debug('moving up for {} seconds'.format(yseconds))

        xseconds = (self.xt - self.az) * (1 / self.xc)
        logging.debug('X: target {} degrees'.format(self.xt))
        logging.debug('moving right for {} seconds'.format(xseconds))

        GPIO.output(17, True)
        GPIO.output(18, False)
        GPIO.output(22, True)
        GPIO.output(27, False)
        if xseconds > yseconds:
            time.sleep(yseconds)
            GPIO.output(18, True)
            time.sleep(xseconds - yseconds)
            GPIO.output(27, True)
        else:
            time.sleep(xseconds)
            GPIO.output(27, True)
            time.sleep(yseconds - xseconds)
            GPIO.output(18, True)

        self.ele = self.yt
        logging.info('elevation is {}'.format(self.ele))

        self.az = self.xt
        logging.debug('azimuth is {}'.format(self.az))

    def dl(self):
        """
        move down and/or left
        """
        yseconds = (self.ele - self.yt) * (1 / self.yc)
        logging.debug('Y: target {} degrees'.format(self.yt))
        logging.debug('moving down for {} seconds'.format(yseconds))

        xseconds = (self.az - self.xt) * (1 / self.xc)
        logging.debug('X: target {} degrees'.format(self.xt))
        logging.debug('moving left for {} seconds'.format(xseconds))

        GPIO.output(18, True)
        GPIO.output(17, False)
        GPIO.output(27, True)
        GPIO.output(22, False)
        if xseconds > yseconds:
            time.sleep(yseconds)
            GPIO.output(17, True)
            time.sleep(xseconds - yseconds)
            GPIO.output(22, True)
        else:
            time.sleep(xseconds)
            GPIO.output(22, True)
            time.sleep(yseconds - xseconds)
            GPIO.output(17, True)

        self.ele = self.yt
        logging.info('elevation is {}'.format(self.ele))

        self.az = self.xt
        logging.debug('azimuth is {}'.format(self.az))

    def dr(self):
        """
        move down and/or right
        """
        yseconds = (self.ele - self.yt) * (1 / self.yc)
        logging.debug('Y: target {} degrees'.format(self.yt))
        logging.debug('moving down for {} seconds'.format(yseconds))

        xseconds = (self.xt - self.az) * (1 / self.xc)
        logging.debug('X: target {} degrees'.format(self.xt))
        logging.debug('moving right for {} seconds'.format(xseconds))

        GPIO.output(18, True)
        GPIO.output(17, False)
        GPIO.output(22, True)
        GPIO.output(27, False)
        if xseconds > yseconds:
            time.sleep(yseconds)
            GPIO.output(17, True)
            time.sleep(xseconds - yseconds)
            GPIO.output(27, True)
        else:
            time.sleep(xseconds)
            GPIO.output(27, True)
            time.sleep(yseconds - xseconds)
            GPIO.output(17, True)

        self.ele = self.yt
        logging.info('elevation is {}'.format(self.ele))

        self.az = self.xt
        logging.debug('azimuth is {}'.format(self.az))

    def m():
        """
        Reset Rotator to MAXIMUM end stop
        """
        logging.info('resetting Max')
        GPIO.output(18, False)
        GPIO.output(17, True)
        GPIO.output(27, False)
        GPIO.output(22, True)
        time.sleep(55)
        GPIO.output(18, True)
        GPIO.output(27, True)
        self.yt = 90
        self.ele = 90
        self.xt = 360
        self.az = 360
        logging.info('reset to max')

    def c(self):
        """
        Move rotator to centre position on both Axis
        """
        self.yt = 45
        self.xt = 180
        self.move()

    def zero(self):
        """
        Reset Rotator to ZERO end stop
        """
        logging.info('resetting zero')
        GPIO.output(18, True)
        GPIO.output(17, False)
        GPIO.output(27, True)
        GPIO.output(22, False)
        time.sleep(55)
        GPIO.output(17, True)
        GPIO.output(22, True)
        self.az = 0
        self.ele = 0
        logging.info('reset to zero')


PORT = 4500

r = Rotator()
r.zero()

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('', PORT))
    s.listen(10)
    logging.info('Socket now listening')

    while True:
        conn, addr = s.accept()
        logging.info('Connected with {}:{}'.format(addr[0], addr[1]))

        while True:
            data = conn.recv(1024)
            logging.debug("Received: {}".format(data))
            try:
                ret = ActionHandler(r).handle_message(*data.split())
                conn.sendall(ret)
            except ConnectionFinished:
                break

        conn.close()

# coding=utf-8
# !/usr/bin/python

from gopigo import *
import time
import math
import random

# constants

# während der Programmierung, damit das Programm irgendwann
# einfach aufhört und nicht ewig läuft
FAILSAFE_STOP = 20

# Entfernung in cm wenn der GoPiGo anhalten soll
STOP_DISTANCE = 30

# Zeit, die zwischen den Iterationen liegen soll (in sekunden)
SLEEP_TIME = .200

# Entfernung in CM, welche als "unendlich" gelten
INFINITY = 200

# 360 rotation is ~64 encoder pulses or 5 deg/pulse
# DPR is the Deg:Pulse Ratio or the # of degrees per
# encoder pulse.
DPR = 360.0 / 64
WHEEL_RAD = 3.25  # Wheels are ~6.5 cm diameter.
CHASS_WID = 13.5  # Chassis is ~13.5 cm wide.


SAMPLES = 4  # Number of sample readings to take for each reading.
DELAY = .02
INF = 200

en_debug = 1


def cm2pulse(dist):
    """
    Calculate the number of pulses to move the chassis dist cm.
    pulses = dist * [pulses/revolution]/[dist/revolution]
    """
    wheel_circ = 2 * math.pi * WHEEL_RAD  # [cm/rev] cm traveled per revolution of wheel
    revs = dist / wheel_circ
    PPR = 18  # [p/rev] encoder Pulses Per wheel Revolution
    pulses = PPR * revs  # [p] encoder pulses required to move dist cm.
    if en_debug:
        print 'WHEEL_RAD', WHEEL_RAD
        print 'revs', revs
        print 'pulses', pulses
    return pulses


def left_deg(deg=None):
    """
    Turn chassis left by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes left().
    """
    if deg is not None:
        pulse = int(deg / DPR)
        enc_tgt(0, 1, pulse)
    left()


def right_deg(deg=None):
    """
    Turn chassis right by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes right().
    """
    if deg is not None:
        pulse = int(deg / DPR)
        enc_tgt(1, 0, pulse)
    right()


def fwd_cm(dist=None):
    """
    Move chassis fwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes fwd().
    """
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1, 1, pulse)
    fwd()


def bwd_cm(dist=None):
    """
    Move chassis bwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes bwd().
    """
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1, 1, pulse)
    bwd()


def scan_room():
    '''
    Start at 0 and move to 180 in increments.
    Angle required to fit chass @20cm away is:
        degrees(atan(CHASS_WID/20))
    Increments angles should be 1/2 of that.
    Looking for 3 consecutive readings of inf.
    3 misses won't guarantee a big enough hole
     because not every obstacle will be 20cm away,
     but it is a good place to start, and more
     importantly, gives us edges to use to
     measure.

    Return list of (angle,dist).
    '''
    ret = []
    #inc = int(math.degrees(math.atan(CHASS_WID / 20)))
    inc = 10
    print "Scanning room in {} degree increments".format(inc)
    for ang in range(0, 181, inc):
        print "  Setting angle to {} ... ".format(ang),
        ## resetting ang because I've seen issues with 0 and 180
        if ang == 0: ang = 1
        if ang == 180: ang = 179
        servo(ang)
        buf = []
        for i in range(SAMPLES):
            dist = us_dist(15)
            print dist,
            if dist < INF and dist >= 0:
                buf.append(dist)
            else:
                buf.append(INF)
        print
        ave = math.fsum(buf) / len(buf)
        print "  dist={}".format(ave)
        ret.append((ang, ave))
        ## Still having issues with inconsistent readings.
        ## e.g.
        ##  Setting angle to   0 ...    18   19 218 49
        ##  Setting angle to 170 ...  1000 1000  45 46
        time.sleep(DELAY)
    ## Reset servo to face front
    servo(90)
    return ret


def obstacle_in_front(distances):
    if distances[7][1] < STOP_DISTANCE or distances[8][1] < STOP_DISTANCE or distances[9][1] < STOP_DISTANCE or distances[10][1] < STOP_DISTANCE or distances[11][1] < STOP_DISTANCE:
        return True
    else:
        return False


def obstacle_right(distances):
    if distances[0][1] < STOP_DISTANCE or distances[1][1] < STOP_DISTANCE or distances[2][1] < STOP_DISTANCE or distances[3][1] < STOP_DISTANCE or distances[4][1] < STOP_DISTANCE or distances[5][1] < STOP_DISTANCE:
        return True
    else:
        return False


def obstacle_left(distances):
    if distances[13][1] < STOP_DISTANCE or distances[14][1] < STOP_DISTANCE or distances[15][1] < STOP_DISTANCE or distances[16][1] < STOP_DISTANCE or distances[17][1] < STOP_DISTANCE or distances[18][1] < STOP_DISTANCE:
        return True
    else:
        return False


class Controller(object):
    """
    Die Controller Klasse ist für die eigentliche Kontrolle
    des Programmes zuständig.

    Sie lädt alle wichtigen Klassen und Funktionen und
    ist für die Routine zuständig.
    """

    def __init__(self):
        print "init Controller()"
        super(Controller, self).__init__()
        self.goMax = FAILSAFE_STOP
        self.goCounter = 0
        self.go = True
        ## reduzierte geschwindigkeit, damit die raeder nicht durch drehen
        self.defaultSpeed = 80
        self.leftSpeed = self.defaultSpeed
        self.rightSpeed = self.defaultSpeed
        set_speed(self.defaultSpeed)


    def run(self):
        print "run Controller()"

        # gefahrene Entfernung in CM
        dist = 0

        while self.go:
            # print "iteration %d" % self.goCounter

            # fahre vorwärts, solange wir kein Hinderniss finden
            # self.move(STOP_DISTANCE)

            # check distance
            scan_results = scan_room()

            # TODO: eintragen in Karte...

            # wenn geradeaus (80, 90, 100 Grad) gemessene dist < 30cm
            # dann drehe X
            if obstacle_in_front(scan_results):
                if obstacle_left(scan_results) and not obstacle_right(scan_results):
                    right_deg(70)
                elif not obstacle_left(scan_results) and obstacle_right(scan_results):
                    left_deg(70)
                elif obstacle_left(scan_results) and obstacle_right(scan_results):
                    left_deg(180)
                else:
                    # zufaellig links oder rechts
                    if random.randint(0, 1):
                        left_deg(70)
                    else:
                        right_deg(70)
            else:
                # ansonsten fahr X geradeaus
                if obstacle_left(scan_results):
                    right_deg(25)
                elif obstacle_right(scan_results):
                    left_deg(25)
                # fwd(20)
                dist = self.move_and_return_distance(STOP_DISTANCE)

            # TODO: Eintragen in karte...

            # safety check %
            # stop after max-counter is reached
            self.goCounter += 1
            if self.goCounter >= self.goMax:
                self.go = False

            # wait a little bit
            time.sleep(SLEEP_TIME)  # in seconds
        pass

    def stop(self):
        self.go = False

    # noinspection PyMethodMayBeStatic
    def move(self, min_dist):
        # Set servo to point straight ahead
        servo(90)

        startL = enc_read(0)
        startR = enc_read(1)
        currentL = startL
        currentR = startR
        distL = currentL - startL
        distR = currentR - startR
        lastMeasureL = currentL

        print "Moving Forward"
        while us_dist(15) > min_dist:

            # read current ticks
            currentL = enc_read(0)
            currentR = enc_read(1)
            distL = currentL - startL
            distR = currentR - startR

            if (currentL - lastMeasureL) > 10:
                if distL == distR:
                    print("moved {} ticks".format(distL))
                elif distL > distR:
                    self.rightSpeed += 3
                    print("set right speed to {}".format(self.rightSpeed))
                elif distL < distR:
                    self.rightSpeed -= 3
                    print("set right speed to {}".format(self.rightSpeed))
                set_right_speed(self.rightSpeed)
                lastMeasureL = distL

            fwd()
            time.sleep(.02)
        stop()
        print "Found obstacle"
        return


    def move_and_return_distance(self, min_dist):

        servo(90)
        startTickL = enc_read(0)
        startTickR = enc_read(1)
        print("start: {},{}".format(startTickL, startTickR))
        self.move(min_dist)
        endTickL = enc_read(0)
        endTickR = enc_read(1)
        print("end: {},{}".format(endTickL, endTickR))

        #Entfernung Berechnen
        tickCountL = endTickL - startTickL
        tickCountR = endTickR - startTickR
        print("count: {},{}".format(tickCountL, tickCountR))
        averageTick = (tickCountL + tickCountR) / 2
        print("average Ticks: {}".format(averageTick))

        # in cm
        dist = WHEEL_CIRC * averageTick / 18
        print("Distance in cm: {}".format(dist))
        return dist
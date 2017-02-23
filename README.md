# dexter_roommap
Using a dexter GoPiGo to create a map of a room


# Programming Setup

* install ```pip``` (https://pip.pypa.io/en/stable/installing/)
* install gopigo library: ```sudo pip install gopigo```


# Setup Dexter

Der Ultraschallsensor muss an den A1 Port angeschlossen werden.  
Der Servo wird vorne in der Mitte an den 3-PIN port angeschlossen.

# Direkte Steuerung

gehe in das projekt
```python
cd ~/Desktop/roommap
```

gehe in die python console und lade den controller
```python
python
>>> from controller import *
```

## Fahren

forwärts (20 cm)
```python
fwd_cm(20)
```

rückwärts (20cm)
```python
bwd_cm(20)
```

stop
```python
stop()
```

links drehen (grad)
```python
left_deg(45)
```

rechts drehen (grad)
```python
right_deg(45)
```

## Servo steuerung

Der servo hat eine Bandbreite von 0 - 180 grad  
Mittelstellung ist 90 grad

```python
servo(90)
```

## Ultraschall Sensor

Der Ultraschallsensor gibt die Maße in cm an

Wenn der Ultraschallsensor an Port A1 angeschlossen ist, so ist der "Pin" **15**

Port: A1 = pin: 15

ultraschall-sensor befehl:  `us_dist(<pin>) `
```python
us_dist(15)
```

# Programmablauf

1. Distanz messen
1. wenn `dist > 30cm` gehe zu Schritt 3., wenn `dist < 30cm` sind, gehe zu Schritt 5
1. Fahre 20cm vorwärts
1. Gehe zu Schritt 1
1. Messe Distanz links 70 grad und rechts 110 grad
1. je nachdem, wo dist. größer ist, drehen wir uns um 20 grad hin und gehen zu schritt 1
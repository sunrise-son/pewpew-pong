This is an online version of Pong on PewPew. Connect the device to a linux based server and use it as a screen for online players.

Setup
=====

* Connnect PewPew via USB and list your devices to find a new serial named like `/dev/ttyACM*`. Let's say it's `/dev/ttyACM0`.
* Make the serial device read and write able (`chmod 666 /dev/ttyACM0` is fair enough but potentially unsafe!)
* Optional: run `minicom -D /dev/ttyACM0` and push first Ctrl-C and second Enter. You will enter the shell session with PewPew, the same which is used by the application code. You can play around a little and after running the game you can monitor all the commands sent to PewPew from the application.
* Install requirements.txt (use Python 3).
* Verify is the path to your serial device is the same as in `ball.py` and 
* Type `python manage.py runserver` and visit http://localhost:8000/1 and http://localhost:8000/2 to verify you can move the paddles.
* Type `python ball.py` to run the game.

Optional setup steps
====================

* You can publish the service online by setting up an ssh tunnel to a server with public IP:
    * `ssh -R 0.0.0.0:8000:localhost:8000 remote.host.com`
    * `socat TCP-LISTEN:8000,fork TCP:127.0.0.1:8000` (on the remote host)
* The remote host public IP must be added to ALLOWED_HOSTS in the django app settings.

Where is the essential part of code?
====================================
* `pewpewrelay/pong/views.py` - paddles movement
* `pewpewrelay/pewpewrelay/settings.py` - django globals related to the device at the bottom
* `ball.py` - game runner

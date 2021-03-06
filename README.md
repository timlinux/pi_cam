# pi_cam


A raspberry pi camera project. I plan to have / do have the following features:

* log temperature to a log file and web page
* show temperature on an lcd panel
* monitor jenkins and show a red light if any test is failing
* monitor jenkins and show a yellow light if any test has bad QA
* monitor jenkins and show a green light if all tests are in good state
* push button on front of device to power down OS

* Setup

You need to install these:

```bash
sudo apt-get update
sudo apt-get install figlet python-imaging-tk git nginx python-virtualenv \
    python-dev uwsgi uwsgi-plugin-python supervisor
```

Due to this issue: https://github.com/raspberrypi/linux/issues/435

You should set your /etc/modules to look like this:

```
w1-therm
w1-gpio pullup=1
i2c-dev
i2c-bcm2708
spi-bcm2708
snd-bcm2835
```

Alternatively or additionally you should run

```
sudo apt-get install rpi-update
```


Then clone this repository to your pi e.g.:

```bash
cd
git clone git://github.com/timlinux/pi_cam.git
```

Now setup a virtualenv. We will host the web server component with django,
uwsgi and nginx.

```bash
cd ~/pi_cam
virtualenv venv
source venv/bin/activate
pip install -r REQUIREMENTS.txt

echo "daemon off;" | sudo tee -a /etc/nginx/nginx.conf

cd /etc/nginx/sites-available
sudo rm default
sudo ln -s /home/pi/pi_cam/server-conf/nginx-site.conf default

cd /etc/uwsgi/apps-available/
sudo ln -s /home/pi/pi_cam/server-conf/django_project_uwsgi.ini default
sudo ln -s ../apps-available/default .

cd /etc/supervisor/conf.d/
sudo ln -s /home/pi/pi_cam/server-conf/supervisor-nginx.conf .
sudo ln -s /home/pi/pi_cam/server-conf/supervisor-uwsgi.conf .

```

Edit ``/etc/default/uwsgi`` and set:

```
# Run automatically at system startup?
RUN_AT_STARTUP=no
```


# Run manually

```bash
cd ~/pi_cam
sudo python controller.py
```

**Note:** Needs to run as root for access to /dev/mem

# Run automatically on boot

```
cd ~/pc_cam
cd /etc/init.d/
sudo cp ~/pi_cam/picam .
sudo chmod +x picam
```

Now either reboot or do:

```
sudo /etc/init.d/picam start
```

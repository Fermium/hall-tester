default: build install-deps

build:
	docker build . -t hall-tester

sync:
	eval "$(ssh-agent -s)"
	ssh-add ~/.ssh/id_rsa
	lsyncd  -nodaemon -delay 5 -rsyncssh $(shell pwd) d@172.100.0.6  /home/d/hall-tester

clean:
	find . -name assets -type d -exec rm -rf {} \;

run:
	export DISPLAY=":0"; xhost +local:root
	docker run -it --privileged -v /tmp/.X11-unix:/tmp/.X11-unix -e uid=$(shell id -u) -e gid=$(shell id -g) -e DISPLAY=":0" -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) -v /dev/bus/usb:/dev/bus/usb -v  $(shell pwd):/root "hall-tester" bash -c "cd root && python /root/run.py"
  export DISPLAY=":0"; xhost -local:root
test:
	docker run -it --privileged -v /tmp/.X11-unix:/tmp/.X11-unix -e uid=$(shell id -u) -e gid=$(shell id -g) -e DISPLAY=":0" -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) -v /dev/bus/usb:/dev/bus/usb -v  $(shell pwd):/root "hall-tester" bash

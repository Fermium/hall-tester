default: build install-deps

build:
	docker build . -t hall-tester

sync:
	eval "$(ssh-agent -s)"
	ssh-add ~/.ssh/id_rsa
	lsyncd  -nodaemon -delay 5 -rsyncssh $(shell pwd) s@172.100.0.34  /home/s/hall-tester

clean:
	find . -name assets -type d -exec rm -rf {} \;

run:
	docker run --privileged -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) -v /dev/bus/usb:/dev/bus/usb -v  $(shell pwd):/root "hall-tester" bash -c "cd root && python /root/run.py"

test:
	docker run -it --privileged -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) -v /dev/bus/usb:/dev/bus/usb -v  $(shell pwd):/root "hall-tester" bash -c "python root/cose.py"

default: build install-deps
	
build: 
	docker build . -t hall-tester
	
sync:
	eval "$(ssh-agent -s)"
	ssh-add ~/.ssh/id_rsa
	lsyncd  -nodaemon -rsyncssh $(shell pwd) d@172.100.0.34  /home/d/hall-tester
	
install-deps: 
	docker run -it --privileged -v /dev/bus/usb:/dev/bus/usb -v  $(shell pwd):/root "hall-tester" bash -c "cd /root/ && pip install -r requirements.txt"

clean:
	find . -name assets -type d -exec rm -rf {} \;

run:
	docker run -it --privileged -v /dev/bus/usb:/dev/bus/usb -v  $(shell pwd):/root "hall-tester" bash -c "python /root/run.py"

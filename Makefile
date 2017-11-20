default: build install-deps
	
build: 
	docker build . -t hall-tester
	
sync:
	eval "$(ssh-agent -s)"
	ssh-add ~/.ssh/id_rsa
	lsyncd  -nodaemon -delay 5 -rsyncssh $(shell pwd) d@172.100.0.34  /home/d/hall-tester
	
clean:
	find . -name assets -type d -exec rm -rf {} \;

run:
	docker run -it --privileged -v /dev/bus/usb:/dev/bus/usb -v  $(shell pwd):/root "hall-tester" bash -c "cd /root && python /root/run.py"

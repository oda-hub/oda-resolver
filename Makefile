REPO=odahub/resolver
IMAGE=$(REPO):$(shell git describe --always)-$(shell cd magic-backend; git describe --always)
CONTAINER=resolver

listen: 
	gunicorn #

run: build
	docker rm -f $(CONTAINER) || true
	docker run \
                -p 8000:5001 \
                -it \
                --rm \
                --name $(CONTAINER) $(IMAGE)

	        #-e ODATESTS_BOT_PASSWORD=$(shell cat testbot-password.txt) \

build:
	rm -fv /dist/*
	docker build --pull -t $(IMAGE) .

push: build
	docker push $(IMAGE)
	docker tag $(IMAGE) $(REPO):latest
	docker push $(REPO):latest

test:
	mypy *.py
	pylint -E  *.py
	echo secret > secret
	GCPROXY_SECRET_LOCATION=./secret \
	POLAR_GRB_DATA_CSV=$(PWD)/data/polar/polar_gwgrb.csv \
		python -m pytest  -sv

.FORCE:

dist: requirements.txt
	rm -rf dist dist.new
	mkdir -p dist.new
	cp requirements.txt dist.new
	docker pull lambci/lambda:build-python3.6
	docker run --rm -t -v "`pwd`/dist.new":/var/task lambci/lambda:build-python3.6 \
		sh -c "\
		yum clean all && yum -y install wget libxml2-devel libxslt-devel && \
		pip install -t . -r requirements.txt"
	mv dist.new dist

build: dist
	rm -f sunset.zip
	cp -r sunset_lambda/lambda_handler.py dist/
	find dist -name __pycache__ -delete
	find dist -name '*.pyc' -delete
	rm -rf dist/bin dist/*.dist-info dist/boto3 dist/botocore
	cd dist && zip -r ../sunset.zip *

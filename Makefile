
PYTEST_OPTIONS = -v -x
PYTEST_JENKINS = --junitxml=./result.xml

.PHONY: test jenkins release audit doc upload-doc

help:
	@echo "test    Launch unittest and display the result"
	@echo "jenkins Create a xUnit XML file to display result in JenkinsCI"

audit:
	python setup.py audit

release:
	python scripts/make-release.py

test:
	@echo "If import failed launch this command before test target"
	@echo "export PYTHONPATH=./"
	py.test $(PYTEST_OPTIONS)

jenkins:
	py.test $(PYTEST_JENKINS)

doc:
	make -C doc clean
	make -C doc html

upload-doc: doc
	@echo "Upload documentation on github"
	@ghp-import -p -m "Update documentation" doc/build/html/


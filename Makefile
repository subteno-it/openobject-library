
PYTEST_OPTIONS = -v -x
PYTEST_JENKINS = --junitxml=./result.xml

.PHONY: test jenkins

help:
	@echo "test    Launch unittest and display the result"
	@echo "jenkins Create a xUnit XML file to display result in JenkinsCI"

test:
	@echo "If import failed launch this command before test target"
	@echo "export PYTHONPATH=./"
	py.test $(PYTEST_OPTIONS)

jenkins:
	py.test $(PYTEST_JENKINS)

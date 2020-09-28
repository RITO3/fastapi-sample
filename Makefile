debug:
	pipenv run debug

format:
	pipenv run sort
	pipenv run format

ci:
	pipenv run ci_init
	pipenv run lint_output
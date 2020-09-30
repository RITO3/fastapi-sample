debug:
	pipenv run debug

format:
	pipenv run sort
	pipenv run sort_test
	pipenv run format


test:
	pipenv run test

ci:
	pipenv run ci_clean
	pipenv run ci_init
	pipenv run lint_output
	pipenv run test
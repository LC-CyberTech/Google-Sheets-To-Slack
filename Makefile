setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
run:
	.venv/bin/python3 autom8.py
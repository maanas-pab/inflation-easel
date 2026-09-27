.PHONY: run test render fmt

run:
	streamlit run app.py

test:
	pytest -q

render:
	python scripts/render_examples.py

fmt:
	python -m compileall -q src app.py

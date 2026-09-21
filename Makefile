# Reproduce the analysis and the distill document.
# Usage: make setup && make data && make all
PY := .venv/bin/python

.PHONY: setup data figures html all clean

setup:                 ## create venv and install deps
	python3 -m venv .venv
	$(PY) -m pip install -q --upgrade pip -r requirements.txt

data:                  ## download all external data (~1.7 GB, not committed)
	$(PY) download_data.py            # arXiv metadata (1.6 GB)
	$(PY) download_conf_data.py       # NeurIPS/ICML/ICLR author files (~70 MB)
	$(PY) download_iclr_decisions.py  # ICLR accept/reject decisions

figures:               ## compute aggregates -> results/figures.json (+ archive)
	$(PY) build_figures.py

html:                  ## assemble the self-contained distill page
	$(PY) build_html.py

all: figures html      ## rebuild findings and the distill document

clean:                 ## remove build caches (keeps data and results)
	rm -f .chartjs.cache

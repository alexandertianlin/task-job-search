.PHONY: setup search report clean

setup:
	@echo "=== Setting up task-job-search environment ==="
	@chmod +x scripts/*.sh 2>/dev/null || true
	@pip3 install -r requirements.txt 2>/dev/null || pip install -r requirements.txt 2>/dev/null || echo "No requirements.txt found, skipping"
	@echo "Setup complete!"

search:
	@echo "=== Running job search ==="
	@bash scripts/search_jobs.sh

report:
	@echo "=== Generating job search report ==="
	@python3 src/generate_report.py 2>/dev/null || python src/generate_report.py

clean:
	@echo "=== Cleaning up ==="
	@rm -rf __pycache__ */__pycache__ 2>/dev/null || true
	@rm -rf .pytest_cache 2>/dev/null || true
	@echo "Clean complete!"

help:
	@echo "Available commands:"
	@echo "  make setup   - Setup environment"
	@echo "  make search  - Run job search"
	@echo "  make report  - Generate report"
	@echo "  make clean   - Clean cache files"

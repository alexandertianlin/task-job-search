# Makefile 模板 — 任务本地自动化

.PHONY: setup clean help

setup:
	@echo "=== Setting up ==="
	@pip3 install -r requirements.txt 2>/dev/null || pip install -r requirements.txt 2>/dev/null || echo "No requirements.txt found"
	@echo "Setup complete!"

clean:
	@echo "=== Cleaning up ==="
	@rm -rf __pycache__ */__pycache__ .pytest_cache 2>/dev/null || true
	@echo "Clean complete!"

help:
	@echo "Available commands:"
	@echo "  make setup   - Setup environment"
	@echo "  make clean   - Clean cache files"
	@echo "  make help    - Show this help"

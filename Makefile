SHELL = /bin/sh

# Virtual environment
venv_path = .venv
venv_bin_path = $(venv_path)/bin
venv_activate = $(venv_bin_path)/activate
venv_pip = $(venv_bin_path)/pip

# Python
python_bin = $(shell which python3)

# Build the virtual environment.
$(venv_path): $(venv_activate)
$(venv_activate): requirements.txt
	@test -d $(venv_path) || virtualenv -p $(python_bin) $(venv_path)
	@$(venv_pip) install -Ur requirements.txt pip
	@touch $(venv_activate)

# Save the list of all currently installed packages.
.PHONY: freeze
freeze: $(venv_activate)
	@$(venv_pip) freeze > requirements.txt

# Execute the code inside the virtual environment.
.PHONY: run
run: $(venv_path) Makefile
	@$(SHELL) -c "source $(venv_activate) && exec python -tt src/main.py"

# Destroy the virtual environment and cache files.
.PHONY: clean
clean:
	@$(RM) -rf $(venv_path)
	@find src/ -name __pycache__ -type d -exec rm -rf {} \;

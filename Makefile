DATA_DIR=data
ACCEPTANCE_DIR=tests/accepted
TEST_LOCATION:=$(DATA_DIR)/tests
$(shell mkdir -p $(ACCEPTANCE_DIR))
$(shell mkdir -p $(TEST_LOCATION))


MPL_ASCII_FILES=$(shell find mpl_ascii -name *.py)

EXAMPLES_PY_FILES=$(wildcard examples/*.py)
EXAMPLES_FILE_NAMES_WO_EXT=$(basename $(notdir $(EXAMPLES_PY_FILES)))
ALL_PLOTS_TXT=$(addsuffix .txt,$(EXAMPLES_FILE_NAMES_WO_EXT))

ALL_PLOTS_NAMES=$(basename $(notdir $(EXAMPLES_PY_FILES)))

.SECONDARY: accept

$(ACCEPTANCE_DIR)/%.txt: $(MPL_ASCII_FILES) examples/%.py
	@mkdir -p $$(dirname $@)
	@python -m examples.$* --ascii --out $@

ascii.%:
	python -m examples.$* --ascii

png.%:
	python -m examples.$*

.PHONY: accept all

accept: $(addprefix $(ACCEPTANCE_DIR)/,$(ALL_PLOTS_TXT))
	@true


test-%.success: $(ACCEPTANCE_DIR)/%.txt
	@mkdir -p $(TEST_LOCATION)
	@if [ -n "$$(git diff $<)" ]; then \
		echo "\033[1m[\033[1;31mTEST FAILED:\033[1;93m $<\033[0m\033[1m]\033[0m"; \
		exit 1; \
	fi;
	@echo "\033[1m[\033[1;32mSUCCESS:\033[1;93m $<\033[0m\033[1m]\033[0m"

test: $(patsubst %,test-%.success,$(ALL_PLOTS_NAMES))

venv-dev:
	eval "$$(pyenv init -)"; \
	pyenv shell 3.11; \
	python -m venv $@; \
	. $@/bin/activate; \
	pip install -r requirements.txt

venv-%:
	eval "$$(pyenv init -)"; \
	pyenv shell $*; \
	python -m venv $@; \
	. $@/bin/activate; \
	pip install -r requirements.txt



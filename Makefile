DATA_DIR=data
LOCATION:=$(DATA_DIR)/plots
TEST_LOCATION:=$(DATA_DIR)/tests

ACCEPTANCE_DIR=examples

MPL_ASCII_FILES=$(wildcard mpl_ascii/*.py)
EXAMPLES_PY_FILES=$(wildcard examples/*.py)
EXAMPLES_FILE_NAMES_WO_EXT=$(basename $(notdir $(EXAMPLES_PY_FILES)))

ALL_PLOTS_NAMES=$(basename $(notdir $(EXAMPLES_PY_FILES)))

ALL_PLOTS_TXT=$(addsuffix .txt,$(EXAMPLES_FILE_NAMES_WO_EXT))
ALL_PLOTS_PNG=$(addsuffix .png,$(EXAMPLES_FILE_NAMES_WO_EXT))

.SECONDARY: accept

$(LOCATION)/%.txt: $(MPL_ASCII_FILES) examples/%.py
	@mkdir -p $(LOCATION)
	@echo -e $*
	@python -m examples.$* --out $@

$(LOCATION)/%.png: $(MPL_ASCII_FILES) examples/%.py
	@mkdir -p $(LOCATION)
	@echo -e $*
	@python -m examples.$* --out $@


$(ACCEPTANCE_DIR)/%.txt: $(LOCATION)/%.txt
	mkdir -p $(ACCEPTANCE_DIR)
	TEMP_HASH=$$(basename $$(mktemp)); \
	cp $< $@.$$TEMP_HASH; \
	mv $@.$$TEMP_HASH $@;

.PHONY: accept all

all: $(addprefix $(LOCATION)/,$(ALL_PLOTS_TXT))
	@true

accept: $(addprefix $(ACCEPTANCE_DIR)/,$(ALL_PLOTS_TXT))
	@true

all.png: $(addprefix $(LOCATION)/,$(ALL_PLOTS_PNG))
	@true

clear:
	-rm -rf $(DATA_DIR)

%.txt: $(LOCATION)/%.txt
	@true

%.png: $(LOCATION)/%.png
	@true

test-%.success: $(ACCEPTANCE_DIR)/%.txt
	@mkdir -p $(TEST_LOCATION)
	@if [ -n "$$(git diff $<)" ]; then \
		echo "\033[1m[\033[1;31mTEST FAILED:\033[1;93m $<\033[0m\033[1m]\033[0m"; \
		exit 1; \
	fi;
	@echo "\033[1m[\033[1;32mSUCCESS:\033[1;93m $<\033[0m\033[1m]\033[0m"

test: $(patsubst %,test-%.success,$(ALL_PLOTS_NAMES))
	@true


venv-dev:
	eval "$$(pyenv init -)"; \
	pyenv shell 3.10; \
	python -m venv $@; \
	. $@/bin/activate; \
	pip install -r requirements.txt

venv-%:
	eval "$$(pyenv init -)"; \
	pyenv shell $*; \
	python -m venv $@; \
	. $@/bin/activate; \
	pip install -r requirements.txt

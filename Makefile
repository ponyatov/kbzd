kb.log: kb.py kb.ini
	python $^ > $@ && tail $(TAIL) $@

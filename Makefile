kb.log: kb.py kb.ini
	python $^ > $@ && tail $(TAIL) $@

merge:
	git checkout master
	git checkout ponyatov -- Makefile kb.py kb.ini

kb.log: kb.py kb.ini
	python $^ > $@ && tail $(TAIL) $@

merge:
	git checkout master
	git checkout ponyatov -- Makefile kb.py kb.ini

NOW = $(shell date +%d%m%y) 
release:
	git tag $(NOW) && git push -v gh master

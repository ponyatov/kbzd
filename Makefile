kb.log: kb.py kb.ini
	python $^ > $@ && tail $(TAIL) $@

web: kb.py kb.ini
	python $^

merge:
	git checkout master
	git checkout ponyatov -- Makefile kb.py kb.ini static templates

NOW = $(shell date +%d%m%y) 
release:
	git tag $(NOW) && git push -v gh master --tags

CMAKE  = cmake
MAKE   = make
WCLEAN = wclean
WMAKE  = wmake


.PHONY: help cmake wmake clean


help:
	@echo "make help:  Print this message and exit"
	@echo "make cmake: Use CMake to compile libraries"
	@echo "make wmake: Use wmake to compile libraries"
	@echo "make clean: Clean cache"

cmake:
	mkdir --parents src/build/
	cd src/build/ && \
		$(CMAKE) .. && \
		$(MAKE) install

wmake:
	cd src/ && \
		$(WMAKE)

clean:
	# cmake
	rm --recursive --force src/build/
	# wmake
	cd src/ && $(WCLEAN)

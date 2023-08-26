CMAKE  = cmake
MAKE   = make
WCLEAN = wclean
WMAKE  = wmake


.PHONY: help cmake wmake test clean


help:
	@echo "make help:  Print this message and exit"
	@echo "make cmake: Use CMake to compile libraries"
	@echo "make wmake: Use wmake to compile libraries"
	@echo "make test:  Test solverHook for OpenFOAM"
	@echo "make clean: Clean cache"

cmake:
	mkdir --parents src/build/
	cd src/build/ && \
		$(CMAKE) .. && \
		$(MAKE) install

wmake:
	cd src/ && \
		$(WMAKE)

test:
	# 7, 8, 9, 10
	cd test/elbow.in/ && \
		./Allrun
	# mv mtx/ ../elbow.out/

clean:
	# cmake
	rm --recursive --force src/build/
	# wmake
	cd src/ && $(WCLEAN)
	# test
	cd test/elbow.in/ && ./Allclean

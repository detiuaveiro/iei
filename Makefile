# Makefile
#
# This Makefile recursively finds and executes any Makefile in subdirectories.
# It is designed to work correctly with directory and file names that contain spaces.
#
# Targets like 'all', 'clean', and 'install' are automatically forwarded to the sub-makes.

# By declaring these as .PHONY, we tell 'make' that they are not actual files.
.PHONY: all clean

# This generic rule uses 'find' to locate all sub-Makefiles and then uses
# the '-execdir' action. '-execdir' runs the specified command from within
# the subdirectory where the Makefile was found, solving the issue with spaces.
all clean:
	@echo "--- Executing target '$@' for Makefiles in subdirectories ---"
	@find . -mindepth 2 -name "Makefile" -execdir $(MAKE) $@ \;
	@echo "--- Finished target '$@' in subdirectories ---"

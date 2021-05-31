import sys

if sys.platform.startswith('win'):
    print("win")
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    print("linux/cygwin")

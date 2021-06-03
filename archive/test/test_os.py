import sys

if sys.platform.startswith('win'):
    print("win")
elif sys.platform.startswith('linux'):
    print("linux")
elif sys.platform.startswith('cygwin'):
    print("cygwin")
elif sys.platform.startswith('darwin'):
    # mac
    print("darwin")

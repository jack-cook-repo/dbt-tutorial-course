import sys
if hasattr(sys, "real_prefix"):
    print("Running in a virtual environment")
else:
    print("Not running in a virtual environment")
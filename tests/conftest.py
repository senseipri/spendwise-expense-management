import os
import sys

# Resolve the absolute path to project root (one level up from this file)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Debug print (optional)
print("**PROJECT ROOT:", project_root)

# Add project root to the Python path if not already included
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(sys.path)  # Debug print to confirm path added (optional)

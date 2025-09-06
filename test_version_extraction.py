#!/usr/bin/env python3
"""Test the version extraction logic used in the workflow."""

import re

# Test the version extraction logic
with open('pyproject.toml', 'r') as f:
    content = f.read()

match = re.search(r'version = "([^"]+)"', content)
if match:
    version = match.group(1)
    print(f"Extracted version: {version}")
else:
    print("No version found!")
    
# Also test the one-liner version
import re
content = open('pyproject.toml').read()
match = re.search(r'version = "([^"]+)"', content)
print(f"One-liner version: {match.group(1)}")

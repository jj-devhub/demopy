# Test file to verify pre-commit hooks
import os,sys,json
import subprocess

def test_function(  ):
    x=1+2
    y = 3 + 4
    return x+y

# This should trigger formatting issues
def another_function( a,b,c ):
    result=a+b+c
    return result

# Add some code that will trigger flake8 errors
def bad_function():
    unused_variable = "this will trigger F841"
    import json  # This will trigger E402 (import not at top)
    return "test"

if __name__=="__main__":
    print("Testing pre-commit hooks")

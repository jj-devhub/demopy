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

if __name__=="__main__":
    print("Testing pre-commit hooks")

"""
Should emit:
B029 - on lines 8 and 13
"""

try:
    pass
except (): # B029: 0, ""
    pass

try:
    pass
except () as e: # B029: 0, ""
    pass

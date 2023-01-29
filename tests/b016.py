"""
Should emit:
B016 - on lines 6, 7, 8, and 10
"""

raise False
raise 1
raise "string"
fstring = "fstring"
raise f"fstring {fstring}"
raise Exception(False)
raise Exception(1)
raise Exception("string")
raise Exception(f"fstring {fstring}")

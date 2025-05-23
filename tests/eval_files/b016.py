"""
Should emit:
B016 - on lines 6, 7, 8, and 10
"""

raise False  # B016: 0
raise 1  # B016: 0
raise "string"  # B016: 0
fstring = "fstring"
raise f"fstring {fstring}"  # B016: 0
raise Exception(False)
raise Exception(1)
raise Exception("string")
raise Exception(f"fstring {fstring}")

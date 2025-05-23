"""
Should emit:
B026 - on lines 16, 17, 18, 19, 20, 21
"""

def foo(bar, baz, bam):
    pass


bar_baz = ["bar", "baz"]

foo("bar", "baz", bam="bam")
foo("bar", baz="baz", bam="bam")
foo(bar="bar", baz="baz", bam="bam")
foo(bam="bam", *["bar", "baz"]) # B026: 15
foo(bam="bam", *bar_baz) # B026: 15
foo(baz="baz", bam="bam", *["bar"]) # B026: 26
foo(bar="bar", baz="baz", bam="bam", *[]) # B026: 37
foo(bam="bam", *["bar"], *["baz"]) # B026: 15 # B026: 25
foo(*["bar"], bam="bam", *["baz"]) # B026: 25
foo.bar(bam="bam", *["bar"]) # B026: 19

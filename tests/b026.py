"""
Should emit:
B026 - on lines 14, 15, 16
"""


def foo(bar, baz, bam):
    pass


foo("bar", "baz", bam="bam")
foo("bar", baz="baz", bam="bam")
foo(bar="bar", baz="baz", bam="bam")
foo(bam="bam", *["bar", "baz"])
foo(baz="baz", bam="bam", *["bar"])
foo(bar="bar", baz="baz", bam="bam", *[])

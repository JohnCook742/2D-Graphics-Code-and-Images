# See https://stackoverflow.com/a/10452244/10047920

import zlib

teststr = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus
pretium justo eget elit eleifend, et dignissim quam eleifend. Nam vehicula nisl
posuere velit volutpat, vitae scelerisque nisl imperdiet. Phasellus dignissim,
dolor amet."""

cmpstr = zlib.compress(teststr.encode('utf-8'))
uncmpstr = zlib.decompress(cmpstr)

#Print sizes
fmt = '{:>8}: (length {})'
print(fmt.format('teststr', len(teststr)))
print(fmt.format('cmpstr', len(cmpstr)))
print(fmt.format('uncmpstr', len(uncmpstr)))

# Compress again - Do we keep getting smaller?
cmp2 = zlib.compress(cmpstr)
print(fmt.format('cmp2', len(cmp2)))



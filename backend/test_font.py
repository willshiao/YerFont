import os
import random
from os import path
from wand.image import Image
import fontforge
import psMat
import sys

SPECIAL_CHARS = set('gjpqy')

def normalizeGlyph(g, letter):
    bb = g.boundingBox()
    dy = bb[3]-bb[1]
    newScale = 400/(dy)
    transforms = []
    if letter in SPECIAL_CHARS:
        print('SPECIAL CASE: ', letter)
        print(bb)
        transforms.append(psMat.translate(-bb[0], -bb[1] - 0.5 * (bb[3] - bb[1])))
    else:
        transforms.append(psMat.translate(-bb[0], -bb[1]))

    if dy > 400:
        transforms.append(psMat.scale(newScale))
    if len(transforms) > 1:
        g.transform(psMat.compose(*transforms))
    else:
        g.transform(transforms[0])
    print(g.boundingBox())
    return g

if len(sys.argv) > 2 or len(sys.argv) < 1:
    print('Invalid # of arguments')
    sys.exit(1)
dname = sys.argv[1]
files = os.listdir(dname)
chrs = [x.split('_')[1].split('.')[0] for x in files if '.svg' in x]

font = fontforge.font()
for ltr in chrs:
    glyph = font.createMappedChar(ltr)
    glyph.importOutlines(path.join(dname, f'letter_{ltr}.svg'))
    try:
        normalizeGlyph(glyph, ltr)
    except Exception as err:
        print('Caught error: ', err)
font.generate('testfont.ttf')
print('Done')

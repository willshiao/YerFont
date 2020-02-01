import os
import random
from os import path
from wand.image import Image
import fontforge
import psMat
import sys
from collections import deque

CAP_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
DOWN_CHARS = set('gjpqy')
UP_CHARS = set('bdfhiklt')
MID_CHARS = set('acemnorsuvwxz')
SPECIAL_CHARS = set('i')
SPECIAL_Y_TRANS = {
    'j': 0.2,
    'u': 0.1,
    '-': -1.5,
    '\'': -0.9,
    '`': -0.9,
}
SPECIAL_Y_SCALE = {
    'i': 0.75,
    '\'': 0.4,
    '`': 0.4,
    '-': 0.6
}

def normalizeGlyph(g, letter):
    bb = g.boundingBox() #compact box that contains the letter
    dy = bb[3]-bb[1]     # xmin,ymin,xmax,ymax
    newScale = 800/(dy)
    transforms = deque()
    #shifting
    if letter in SPECIAL_Y_TRANS:
        transforms.append(psMat.translate(-bb[0], -bb[1] - SPECIAL_Y_TRANS[letter] * (bb[3] - bb[1])))
    elif letter in DOWN_CHARS:
        #print('DOWN CASE: ', letter)
        #print(bb)
        transforms.append(psMat.translate(-bb[0], -bb[1] - 0.35 * (bb[3] - bb[1]))) # 0,0 35% of its height
    else:
        transforms.append(psMat.translate(-bb[0], -bb[1]))

    # if letter in SPECIAL_CHARS:
    #     print('i: ', letter)
    #     print(bb)
    #     transforms.append(psMat.translate(300, 0) )
    # scaling
    if dy > 800:
        transforms.append(psMat.scale(newScale))
    if letter in MID_CHARS and letter not in SPECIAL_Y_SCALE:
        transforms.append(psMat.scale(0.5))
    elif letter in SPECIAL_Y_SCALE:
        transforms.append(psMat.scale(SPECIAL_Y_SCALE[letter]))

    #composing
    while len(transforms) > 1:
        el1 = transforms.popleft()
        el2 = transforms.popleft()
        transforms.appendleft(psMat.compose(el1, el2))
    g.transform(transforms[0])
    print('POST: ', letter)
    bb2 = g.boundingBox()
    g.width = bb2[2]
    g.simplify()
    # g.round()
    # g.cluster(0, 100)
    print(g.boundingBox(), g.width)
    
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

import fontforge
import psMat

SPECIAL_CHARS = set('gjpqy')

def normalizeGlyph(g, letter):
    bb = g.boundingBox()
    dy = bb[3]-bb[1]
    newScale = 800/(dy)
    transforms = []
    if letter in SPECIAL_CHARS:
        print('SPECIAL CASE: ', letter)
        print(bb)
        transforms.append(psMat.translate(-bb[0], -bb[1] - 0.5 * (bb[3] - bb[1])))
    else:
        transforms.append(psMat.translate(-bb[0], -bb[1]))

    if dy > 800:
        transforms.append(psMat.scale(newScale))
    if len(transforms) > 1:
        g.transform(psMat.compose(*transforms))
    else:
        g.transform(transforms[0])
    print(g.boundingBox())
    return g


font = fontforge.font()
# glyph = font.createMappedChar('A')
# glyph.importOutlines('a.svg')
# normalizeGlyph(glyph)

glyph = font.createMappedChar('B')
glyph.importOutlines('yin_yang.svg')
normalizeGlyph(glyph, 'B')

for i in range(26):
    ltr = chr(ord('a') + i)
    glyph = font.createMappedChar(ltr)
    glyph.importOutlines(f'letter_{i}_clean.svg')
    normalizeGlyph(glyph, ltr)

font.generate('testfont.ttf')

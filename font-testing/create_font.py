import fontforge
import psMat

def normalizeGlyph(g):
    bb = g.boundingBox()
    dy = bb[3]-bb[1]
    newScale = 800/(dy)
    transforms = []
    transforms.append(psMat.translate(-bb[0], -bb[1]))
    if dy > 800:
        transforms.append(psMat.scale(newScale))
    if len(transforms) > 1:
        g.transform(psMat.compose(*transforms))
    else:
        g.transform(transforms[0])
    return g


font = fontforge.font()
glyph = font.createMappedChar('A')
glyph.importOutlines('a.svg')
normalizeGlyph(glyph)

glyph = font.createMappedChar('B')
glyph.importOutlines('yin_yang.svg')
normalizeGlyph(glyph)

for i in range(26):
    ltr = chr(ord('a') + i)
    glyph = font.createMappedChar(ltr)
    glyph.importOutlines(f'letter_{i}_clean.svg')
    normalizeGlyph(glyph)

font.generate('testfont.ttf')

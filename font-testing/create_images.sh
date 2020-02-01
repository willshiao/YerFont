#!/bin/bash

magick convert sprites_clean.svg -crop 2x13-1-4@ +repage +adjoin letter_%d.svg
for i in {0..25}; do
    magick "letter_${i}.svg" -trim "letter_${i}_clean.svg"
done

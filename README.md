# YerFont
Make your handwriting into a font, but not just any regular font... The goal of YerFont is taking multiple trials of the users' handwriting of the letters in the English alphabet, selecting from the multiple trials, making the typing look as realistic as possible.

When first loading up the website, the user is introduced to two options: create their own font or use previously existing ones and convert text into the selected fonts. Creating their own font will require them to write letters into a canvas and after they have selected "Create font!" they will be able to use it to type. This will also download their font to their computer.

Created by [Paris Hom](https://github.com/tomehomme), [Ji Hwan Kim](https://github.com/kimjihwan0208), [Carolyn Kong](https://github.com/ckong007), and [William Shiao](https://github.com/willshiao) for [HackUCI 2020](https://hackuci2020.devpost.com/).

# Inspiration
Normal fonts are cool but do they _really_ represent who you are? We wanted to make a font creation website that takes a person's handwriting and forms it into a realistic font, as if the user had written it themselves.

# What we learned
Making fonts is difficult.

# How we built it
Half the team focused on the website front end where users can input their own writing style to create the font, and the other half focused on taking in the .svg file of each letter and linking it correctly for the user to be able to type in their handwriting. Machine learning was implemented to create completely new handwriting styles based off our own database of handwritten alphabetic characters. Allowed users to preview preset fonts or try out a font they just used in a text area.

# Challenges
Natural human handwriting has ligatures which connect letters to each other (like cursive). Recording every combination of how each letter transitions into all possible letters would have been extremely time consuming so we were restricted to recording single letters at a time.

# Next for YerFont
Giving users an option to sign in and save their recorded letters would give them easy access to their own fonts. Numbers would also be nice.

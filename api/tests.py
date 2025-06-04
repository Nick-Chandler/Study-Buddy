text = """Dear Nick in like 3 months,
This is going to be a hard semester. Operating systems, math concepts 2, calc 2. To be
honest it’s probably going to suck (As in it’s going to be hard). Also this is after a year long break
from school so you are still getting used to being back at school/in Philly. That doesn’t mean that
you can’t do it though! It’s important to understand that something being difficult does not mean
that it cannot be done, especially by you. The way that my remaining courses are laid out, this is
probably the last semester I’ll have to take more than like 2-3 classes so if you can power
through this"""

words = text.split()
for index, word in enumerate(words):
    print(index, word)

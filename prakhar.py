from random import randint
names=["We","I","They","He","She","Jack","Jim"]
verbs=["was", "is", "are", "were"]
nouns=["playing a game", "watching television", "talking", "dancing", "speaking"]
while True:
    print(names[randint(0,len(names)-1)]+" "+verbs[randint(0,len(verbs)-1)]+" "+nouns[randint(0,len(nouns)-1)])
    break

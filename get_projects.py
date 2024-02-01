import info
from setting import color

for p in info.projects:
    print(color._blue + "project ID: " + color._ec + "{}".format(p.id) 
          + color._blue + " project name: " + color._ec + "{}".format(p.name))
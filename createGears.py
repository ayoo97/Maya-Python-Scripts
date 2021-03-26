import gearCreator as gc
reload(gc)

# create a gear
transform, constructor, extrude = gc.createGear()

# change a geart
gc.changeTeeth(constructor, extrude, length = 1)

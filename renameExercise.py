from maya import cmds

SUFFIXES = {
    "mesh" : "geo",
    "joint" : "jnt",
    "camera" : None,
    "PxrDomeLight" : "pxrlgt",
    "ambientLight" : "lgt"
}

DEFAULT_SUFFIX = "grp"

# rename(mySelection): renames selected objects or object in the outliner if nothing is selected; returns objects
# - mySelection is a bool;  if True, something MUST be selected by the user
def rename(mySelection = False):
    """
    Renames a list of objects with the appropriate suffixes.

    Args:
        mySelection (bool, optional): Whether or not the function uses the current selection. Defaults to False.

    Raises:
        RuntimeError: Raised if the user sets mySelection to True and does not select an object.

    Returns:
        list: returns the resulting list of objects
    """
    objects = cmds.ls(selection = mySelection, long = True, dag = True)

    if mySelection and not objects:
        raise RuntimeError("Nothing is selected.")
        
    # sort selection by len descending
    objects.sort(key = len, reverse = True)

    for obj in objects:
        shortName = obj.split("|")[-1]
        
        children = cmds.listRelatives(obj, children = True, fullPath = True) or []
        
        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)
        if not suffix:
            continue
        
        if obj.endswith("_" + suffix):
            continue
            
        newName = "%s_%s" % (shortName, suffix)
        cmds.rename(obj, newName)

        i = objects.index(obj)
        objects[i] = obj.replace(shortName, newName)
    
    return objects
# website:
#  http://www.jorendorff.com/articles/python/path/
#
# filename: directory_walk_remove_files.py

# with os.path.walk
def delete_backups(arg, dirname, names):
    for name in names:
        if name.endswith('~'):
            os.remove(os.path.join(dirname, name))

os.path.walk(os.environ['HOME'], delete_backups, None)

# with os.path, if (like me) you can never remember how os.path.walk works
def walk_tree_delete_backups(d):
    for name in os.listdir(d):
        path = os.path.join(d, name)
        if os.path.isdir(path):
            walk_tree_delete_backups(path)
        elif name.endswith('~'):
            os.remove(path)

walk_tree_delete_backups(os.environ['HOME'])

# with path
d = path(os.environ['HOME'])
for f in d.walkfiles('*~'):
    f.remove()
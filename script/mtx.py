import pathlib as p
import shutil


cache = p.Path(__file__).parents[1] / 'cache'
src = cache / 'tutorial'
dst = cache / 'mtx'

if dst.exists():
    exit()

for path in src.rglob('controlDict'):
    mtx = path.parents[1] / 'mtx'
    directory = dst / mtx.relative_to(src).parent
    if not mtx.exists() or directory.exists():
        continue
    shutil.copytree(mtx, directory)

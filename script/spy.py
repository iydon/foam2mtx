import pathlib as p

import matplotlib.pyplot as plt
import tqdm

from scipy.io import mmread


cache = p.Path(__file__).parents[1] / 'cache'
mtx = cache / 'mtx'
spy = cache / 'spy'

if spy.exists():
    exit()

for directory in mtx.iterdir():
    dst = spy / directory.name
    dst.mkdir(parents=True, exist_ok=True)
    for src in tqdm.tqdm(list(directory.rglob('*')), desc=directory.name):
        if not src.is_file():
            continue
        filename = '+'.join(src.relative_to(directory).parts) + '.png'
        path = dst / filename
        if path.exists():
            continue
        # spy
        try:
            matrix = mmread(src)
        except Exception as e:
            print(src, e)
            continue
        fig, ax = plt.subplots(1, 1, dpi=400)
        ax.spy(matrix, markersize=1)
        fig.tight_layout()
        fig.savefig(path)
        # gc
        plt.close('all')

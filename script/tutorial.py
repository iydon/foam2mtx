import os
import pathlib as p
import re
import shutil
import subprocess as sp
import typing as t

import typing_extensions as te


class Tutorial:

    root = p.Path(os.environ['FOAM_TUTORIALS'])
    solver = {
        'diagonal': 'diagonalHook',
        'GAMG': 'GAMGHook',
        'PBiCG': 'PBiCGHook',
        'PBiCGStab': 'PBiCGStabHook',
        'PCG': 'PCGHook',
        'smoothSolver': 'smoothSolverHook',
    }

    _pat_lib = re.compile(r'"[^"]+?"')

    def __init__(self, directory: str) -> None:
        self._directory = p.Path(directory)
        self._pa = self._directory / 'Allrun'
        self._pc = self._directory / 'system' / 'controlDict'
        self._pf = self._directory / 'system' / 'fvSolution'

    @classmethod
    def iterValids(cls) -> t.Iterator[te.Self]:
        for path in cls.root.rglob('controlDict'):
            self = cls(path.parents[1])
            if self.is_valid():
                yield self

    @property
    def directory(self) -> p.Path:
        return self._directory

    def is_valid(self) -> bool:
        return self._pa.exists() and self._pc.exists() and self._pf.exists()

    def copy(self, dst: str) -> te.Self:
        directory = dst / self._directory.relative_to(self.root)
        shutil.copytree(self._directory, directory, dirs_exist_ok=True)
        return self.__class__(directory)

    def hook(self, number: int = 1) -> te.Self:
        # controlDict
        ## endTime
        delta = float(self._fd(self._pc, '-entry', 'deltaT', '-value'))
        self._fd(self._pc, '-entry', 'endTime', '-set', str(number*delta))
        ## libs
        stdout = self._fd(self._pc, '-entry', 'libs', '-value')
        libs = ['"libsolverHook.so"', *self._pat_lib.findall(stdout)]
        self._fd(self._pc, '-entry', 'libs', '-set', '('+' '.join(libs)+')')
        # fvSolution
        for key in self._fd(self._pf, '-entry', 'solvers', '-keywords').splitlines():
            key = key.strip('"')
            old = self._fd(self._pf, '-entry', f'solvers/{key}/solver', '-value').strip()
            if old:
                new = self.solver.get(old, old)
                self._fd(self._pf, '-entry', f'solvers/{key}/solver', '-set', new)
        return self

    def all_run(self) -> sp.CompletedProcess:
        return sp.run([self._pa], capture_output=True, cwd=self._directory)

    def _fd(self, *args: str) -> str:
        cp = sp.run(['foamDictionary', *args], capture_output=True, cwd=self._directory)
        return cp.stdout.decode()


if __name__ == '__main__':
    cache = p.Path(__file__).parents[1] / 'cache'
    for old in Tutorial.iterValids():
        cp = old \
            .copy(cache) \
            .hook() \
            .all_run()
        if cp.returncode == 0:
            print(f'[v] {old.directory}')
        else:
            print(f'[x] {old.directory} {cp.stderr}')
        break

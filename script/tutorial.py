import os
import pathlib as p
import re
import shutil
import subprocess as sp
import typing as t

import typing_extensions as te


version = os.environ['WM_PROJECT_VERSION']  # 7, 8, 9, 10


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
        self._par = self._directory / 'Allrun'
        self._pac = self._directory / 'Allclean'
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
        if not all(map(p.Path.exists, [self._par, self._pac, self._pc, self._pf])):
            return False
        if 'foamDictionary' in self._par.read_text():
            # OpenFOAM-7/tutorials/combustion/reactingFoam/RAS/SandiaD_LTS/Allrun
            return False
        return True

    def copy(self, dst: str) -> te.Self:
        directory = dst / self._directory.relative_to(self.root)
        shutil.copytree(self._directory, directory, dirs_exist_ok=True)
        return self.__class__(directory)

    def hook(self, number: int = 3) -> te.Self:
        # controlDict
        ## endTime
        start = float(self._fd(self._pc, entry='startTime', value=None))
        delta = float(self._fd(self._pc, entry='deltaT', value=None))
        self._fd(self._pc, entry='endTime', set=str(start+number*delta))
        ## libs
        stdout = self._fd(self._pc, entry='libs', value=None)
        libs = ['"libsolverHook.so"', *self._pat_lib.findall(stdout)]
        self._fd(self._pc, entry='libs', set='('+' '.join(libs)+')')
        # fvSolution
        for key in self._fd(self._pf, entry='solvers', keywords=None).splitlines():
            key = key.strip('"')
            old = self._fd(self._pf, entry=f'solvers/{key}/solver', value=None).strip()
            if old:
                new = self.solver.get(old, old)
                self._fd(self._pf, entry=f'solvers/{key}/solver', set=new)
        return self

    def all_run(self) -> sp.CompletedProcess:
        return sp.run([self._par], capture_output=True, cwd=self._directory)

    def all_clean(self) -> sp.CompletedProcess:
        return sp.run([self._pac], capture_output=True, cwd=self._directory)

    def _fd(self, path: str, **kwargs: t.Optional[str]) -> str:
        if 'entry' in kwargs and version in {'7'}:
            kwargs['entry'] = kwargs['entry'].replace('/', ':')
        args = ['foamDictionary', path]
        for key, value in kwargs.items():
            args.append(f'-{key}')
            if value is not None:
                args.append(value)
        cp = sp.run(args, capture_output=True, cwd=self._directory)
        return cp.stdout.decode()


if __name__ == '__main__':
    cache = p.Path(__file__).parents[1] / 'cache' / 'tutorial' / version
    for old in Tutorial.iterValids():
        new = old.copy(cache).hook()
        cp = new.all_run()
        if cp.returncode == 0:
            print(f'[v] {new.directory}')
        else:
            print(f'[x] {new.directory} {cp.stderr}')

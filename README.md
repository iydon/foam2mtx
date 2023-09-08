<div align="center">
  <a href="https://github.com/iydon/foam2mtx">
    🟢⬜🟩⬜🟩<br />
    ⬜⬜⬜⬜⬜<br />
    🟩⬜🟩⬜🟩<br />
    ⬜⬜⬜⬜⬜<br />
    🟩⬜🟩⬜🟩<br />
  </a>

  <h3 align="center">foam2mtx</h3>

  <p align="center">
    Dump OpenFOAM matrix to mtx format (experimental)
  </p>
</div>



## About the Project

This is an experimental sub-project to dump OpenFOAM lduMatrix to matrix market format, which does not yet take into account of certain boundary conditions, but is sufficient as a training dataset. Figure [1](#figure-1) shows the mixing elbow case that comes with the icoFoam solver, and Figure [2](#figure-2) shows a visualization of the dumped $U_x$ matrix at the first time step.

The following OpenFOAM versions are currently supported:

- OpenFOAM-7
- OpenFOAM-8
- OpenFOAM-9
- OpenFOAM-10

<figure id="figure-1">
  <img id="figure-1" src="test/elbow.out/img/paraview.png">
  <figcaption>Figure 1<figcaption>
</figure>

<figure id="figure-2">
  <img id="figure-2" src="test/elbow.out/spy/Ux+0.png">
  <figcaption>Figure 2<figcaption>
</figure>

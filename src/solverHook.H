#pragma once

#include "lduMatrix.H"
#include "diagonalSolver.H"
#include "GAMGSolver.H"
#include "PBiCG.H"
#include "PBiCGStab.H"
#include "PCG.H"
#include "smoothSolver.H"

using namespace Foam;

class diagonalSolverHook : public diagonalSolver
{
public:
    TypeName("diagonalHook");

    diagonalSolverHook(
        const word &fieldName,
        const lduMatrix &matrix,
        const FieldField<Field, scalar> &interfaceBouCoeffs,
        const FieldField<Field, scalar> &interfaceIntCoeffs,
        const lduInterfaceFieldPtrsList &interfaces,
        const dictionary &solverControls)
        : diagonalSolver(
              fieldName,
              matrix,
              interfaceBouCoeffs,
              interfaceIntCoeffs,
              interfaces,
              solverControls) {}

    virtual ~diagonalSolverHook() {}

    solverPerformance solve(
        scalarField &psi,
        const scalarField &source,
        const direction cmpt = 0) const;

    void operator=(const diagonalSolver &) = delete;
};

class GAMGSolverHook : public GAMGSolver
{
public:
    TypeName("GAMGHook");

    GAMGSolverHook(
        const word &fieldName,
        const lduMatrix &matrix,
        const FieldField<Field, scalar> &interfaceBouCoeffs,
        const FieldField<Field, scalar> &interfaceIntCoeffs,
        const lduInterfaceFieldPtrsList &interfaces,
        const dictionary &solverControls)
        : GAMGSolver(
              fieldName,
              matrix,
              interfaceBouCoeffs,
              interfaceIntCoeffs,
              interfaces,
              solverControls) {}

    virtual ~GAMGSolverHook() {}

    virtual solverPerformance solve(
        scalarField &psi,
        const scalarField &source,
        const direction cmpt = 0) const;
};

class PBiCGHook : public PBiCG
{
public:
    TypeName("PBiCGHook");

    PBiCGHook(
        const word &fieldName,
        const lduMatrix &matrix,
        const FieldField<Field, scalar> &interfaceBouCoeffs,
        const FieldField<Field, scalar> &interfaceIntCoeffs,
        const lduInterfaceFieldPtrsList &interfaces,
        const dictionary &solverControls)
        : PBiCG(
              fieldName,
              matrix,
              interfaceBouCoeffs,
              interfaceIntCoeffs,
              interfaces,
              solverControls) {}

    virtual ~PBiCGHook() {}

    virtual solverPerformance solve(
        scalarField &psi,
        const scalarField &source,
        const direction cmpt = 0) const;
};

class PBiCGStabHook : public PBiCGStab
{
public:
    TypeName("PBiCGStabHook");

    PBiCGStabHook(
        const word &fieldName,
        const lduMatrix &matrix,
        const FieldField<Field, scalar> &interfaceBouCoeffs,
        const FieldField<Field, scalar> &interfaceIntCoeffs,
        const lduInterfaceFieldPtrsList &interfaces,
        const dictionary &solverControls)
        : PBiCGStab(
              fieldName,
              matrix,
              interfaceBouCoeffs,
              interfaceIntCoeffs,
              interfaces,
              solverControls) {}

    virtual ~PBiCGStabHook() {}

    virtual solverPerformance solve(
        scalarField &psi,
        const scalarField &source,
        const direction cmpt = 0) const;
};

class PCGHook : public PCG
{
public:
    TypeName("PCGHook");

    PCGHook(
        const word &fieldName,
        const lduMatrix &matrix,
        const FieldField<Field, scalar> &interfaceBouCoeffs,
        const FieldField<Field, scalar> &interfaceIntCoeffs,
        const lduInterfaceFieldPtrsList &interfaces,
        const dictionary &solverControls)
        : PCG(
              fieldName,
              matrix,
              interfaceBouCoeffs,
              interfaceIntCoeffs,
              interfaces,
              solverControls) {}

    virtual ~PCGHook() {}

    virtual solverPerformance solve(
        scalarField &psi,
        const scalarField &source,
        const direction cmpt = 0) const;
};

class smoothSolverHook : public smoothSolver
{
public:
    TypeName("smoothSolverHook");

    smoothSolverHook(
        const word &fieldName,
        const lduMatrix &matrix,
        const FieldField<Field, scalar> &interfaceBouCoeffs,
        const FieldField<Field, scalar> &interfaceIntCoeffs,
        const lduInterfaceFieldPtrsList &interfaces,
        const dictionary &solverControls)
        : smoothSolver(
              fieldName,
              matrix,
              interfaceBouCoeffs,
              interfaceIntCoeffs,
              interfaces,
              solverControls) {}

    virtual ~smoothSolverHook() {}

    virtual solverPerformance solve(
        scalarField &psi,
        const scalarField &source,
        const direction cmpt = 0) const;
};

void ldu2mtx(const lduMatrix &, const word &);
label next(const word &);

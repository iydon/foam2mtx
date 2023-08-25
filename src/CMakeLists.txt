cmake_minimum_required(VERSION 3.10)

project(solverHook)

set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(COMPILE_DEFINITIONS "-std=c++14 -m64 -Dlinux64 -DWM_ARCH_OPTION=64 -DWM_DP -DWM_LABEL_SIZE=32 -Wall -Wextra -Wold-style-cast -Wnon-virtual-dtor -Wno-unused-parameter -Wno-invalid-offsetof -Wno-attributes -O3 -DNoRepository -ftemplate-depth-100 -fPIC")  # demo only

add_definitions("${COMPILE_DEFINITIONS} ")

include_directories(
    $ENV{FOAM_SRC}/OpenFOAM/lnInclude
    $ENV{FOAM_SRC}/OSspecific/POSIX/lnInclude
)

add_library(${PROJECT_NAME} SHARED solverHook.C)

install(
    TARGETS ${PROJECT_NAME}
    DESTINATION $ENV{FOAM_LIBBIN}
)

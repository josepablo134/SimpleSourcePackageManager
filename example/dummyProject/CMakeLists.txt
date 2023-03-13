################################################################################
# @file CMakeLists.txt
# @author Josepablo C (josepablo134@gmail.com)
# @version 1.0
################################################################################

cmake_minimum_required( VERSION 3.18.4 )

project( dummyProject
		LANGUAGES C
)

# ===================================================================
# Project Set-Up
# ===================================================================

set( PROJECT_NAME template )
set( EXEC_NAME ${PROJECT_NAME} )
set( WORK_DIR ${PROJECT_SOURCE_DIR} )

# ===================================================================
# Project content
# ===================================================================

add_executable( ${EXEC_NAME} ${WORK_DIR}/main.c )

# Install using "SimpleSourcePackageManager.py -i ../DummyLib -n DummyLib"
add_subdirectory( ${WORK_DIR}/c_modules )

target_link_libraries( ${EXEC_NAME}
		DummyLib
)

target_include_directories(${EXEC_NAME} PRIVATE
		${WORK_DIR}
)


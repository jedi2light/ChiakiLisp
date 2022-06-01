cmake_minimum_required(VERSION 3.20.0)

project(chiakilisp VERSION 1.0.0
                   DESCRIPTION "Chiakilisp C++ Runtime")

add_library(chiakilisp SHARED chiakilisp.cpp)

set_target_properties(chiakilisp PROPERTIES
                                 PUBLIC_HEADER chiakilisp.hpp)

include(GNUInstallDirs)

install(TARGETS chiakilisp
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})



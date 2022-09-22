cmake_minimum_required(VERSION 3.1)

project(kinova_mj_description VERSION 1.0.0)

if(NOT TARGET mc_mujoco)
  find_package(mc_mujoco REQUIRED)
endif()

option(SRC_MODE "Use files in the repository instead of installed files" OFF)

set(KINOVA_XML_MODEL_PATH "xml/gen3_7dof_mujoco.xml")
set(KINOVA_PDGAINS_PATH "pdgains/PDgains_sim.dat")

if(SRC_MODE)
  set(KINOVA_XML_MODEL_PATH "${CMAKE_CURRENT_SOURCE_DIR}/${KINOVA_XML_MODEL_PATH}")
  set(KINOVA_PDGAINS_PATH "${CMAKE_CURRENT_SOURCE_DIR}/${KINOVA_PDGAINS_PATH}")
else()
  set(KINOVA_XML_MODEL_PATH "${MC_MUJOCO_SHARE_DESTINATION}/kinova/${KINOVA_XML_MODEL_PATH}")
  set(KINOVA_PDGAINS_PATH "${MC_MUJOCO_SHARE_DESTINATION}/kinova/${KINOVA_PDGAINS_PATH}")
endif()

configure_file(mc_mujoco/kinova.in.yaml "${CMAKE_CURRENT_BINARY_DIR}/mc_mujoco/kinova.yaml")
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/mc_mujoco/kinova.yaml" DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}")

install(DIRECTORY meshes DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}/kinova" FILES_MATCHING PATTERN "*.STL")
install(DIRECTORY pdgains DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}/kinova" FILES_MATCHING PATTERN "*.dat")
install(DIRECTORY xml DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}/kinova" FILES_MATCHING PATTERN "*.xml")

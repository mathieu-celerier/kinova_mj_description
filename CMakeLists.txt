cmake_minimum_required(VERSION 3.10)

project(kinova_mj_description VERSION 1.0.0)

option(HONOR_INSTALL_PREFIX "Whether to install in CMAKE_INSTALL_PREFIX (for nix)" OFF)
option(SRC_MODE "Use files in the repository instead of installed files" OFF)

if(HONOR_INSTALL_PREFIX)
  set(MC_MUJOCO_SHARE_DESTINATION "${CMAKE_INSTALL_PREFIX}")
elseif(NOT TARGET mc_mujoco)
  find_package(mc_mujoco REQUIRED)
endif()
# Nothing to do in the remaining case: this tree was add_subdirectory()'d from inside mc_mujoco's
# own build (its robots/CMakeLists.txt globs every child holding a CMakeLists.txt, the way
# robots/jvrc_mj_description is consumed), so the mc_mujoco target already exists and
# MC_MUJOCO_SHARE_DESTINATION is already set by mc_mujoco's top-level CMakeLists. Looking for an
# *installed* mc_mujoco there fails, since the one being built is not installed yet.

function(install_variant VARIANT)
  set(options)
  set(oneValueArgs SOURCE_XML PDGAINS_FILE)
  cmake_parse_arguments(INSTALL_VARIANT "${options}" "${oneValueArgs}" "" ${ARGN})

  if(NOT INSTALL_VARIANT_SOURCE_XML)
    set(INSTALL_VARIANT_SOURCE_XML "${VARIANT}")
  endif()
  if(NOT INSTALL_VARIANT_PDGAINS_FILE)
    set(INSTALL_VARIANT_PDGAINS_FILE "pdgains/PDgains_sim.dat")
  endif()

  set(GENERATED_XML_DIR "${CMAKE_CURRENT_BINARY_DIR}/xml")
  set(GENERATED_YAML_DIR "${CMAKE_CURRENT_BINARY_DIR}/mc_mujoco")
  file(MAKE_DIRECTORY "${GENERATED_XML_DIR}" "${GENERATED_YAML_DIR}")
  configure_file("xml/${INSTALL_VARIANT_SOURCE_XML}.xml" "${GENERATED_XML_DIR}/${VARIANT}.xml" COPYONLY)

  if(SRC_MODE)
    set(KINOVA_XML_MODEL_PATH "${GENERATED_XML_DIR}/${VARIANT}.xml")
    set(KINOVA_PDGAINS_PATH "${CMAKE_CURRENT_SOURCE_DIR}/${INSTALL_VARIANT_PDGAINS_FILE}")
  else()
    set(KINOVA_XML_MODEL_PATH "${MC_MUJOCO_SHARE_DESTINATION}/${VARIANT}/xml/${VARIANT}.xml")
    set(KINOVA_PDGAINS_PATH "${MC_MUJOCO_SHARE_DESTINATION}/${VARIANT}/${INSTALL_VARIANT_PDGAINS_FILE}")
  endif()

  configure_file("mc_mujoco/kinova.in.yaml" "${GENERATED_YAML_DIR}/${VARIANT}.yaml" @ONLY)
  install(FILES "${GENERATED_YAML_DIR}/${VARIANT}.yaml" DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}")
  install(FILES "${GENERATED_XML_DIR}/${VARIANT}.xml" DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}/${VARIANT}/xml")
  install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/xml/includes/" DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}/${VARIANT}/xml/includes"
          FILES_MATCHING PATTERN "*.xml")

  install(DIRECTORY meshes DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}/${VARIANT}" FILES_MATCHING PATTERN "*.STL" PATTERN "*.stl" PATTERN "*.obj")
  install(DIRECTORY pdgains DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}/${VARIANT}" FILES_MATCHING PATTERN "*.dat")
endfunction()

function(install_object OBJECT)
  set(GENERATED_YAML_DIR "${CMAKE_CURRENT_BINARY_DIR}/mc_mujoco")
  file(MAKE_DIRECTORY "${GENERATED_YAML_DIR}")
  configure_file("mc_mujoco/${OBJECT}.in.yaml" "${GENERATED_YAML_DIR}/${OBJECT}.yaml" @ONLY)
  install(FILES "${GENERATED_YAML_DIR}/${OBJECT}.yaml" DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}")
  install(FILES "xml/${OBJECT}.xml" DESTINATION "${MC_MUJOCO_SHARE_DESTINATION}/${OBJECT}/xml")
endfunction()

install_object(kinova_ball)

install_variant(kinova)
install_variant(kinova_bota)
install_variant(kinova_bota_ds4)
install_variant(kinova_bota_plate)
install_variant(kinova_bota_screw)
install_variant(kinova_bota_hook)
install_variant(kinova_bota_peg_plate)
install_variant(kinova_bota_peg_plate_camera)
install_variant(kinova_bota_gena)
install_variant(kinova_bota_gena_ds4)
install_variant(kinova_bota_gena_plate)
install_variant(kinova_bota_gena_screw)
install_variant(kinova_bota_gena_hook)
install_variant(kinova_bota_gena_gripper PDGAINS_FILE pdgains/PDgains_sim_gripper.dat)
install_variant(kinova_bota_gena_gripper_2f140 PDGAINS_FILE pdgains/PDgains_sim_gripper.dat)
install_variant(kinova_camera)
install_variant(kinova_camera_gripper PDGAINS_FILE pdgains/PDgains_sim_gripper.dat)
install_variant(kinova_camera_gripper_2f140 PDGAINS_FILE pdgains/PDgains_sim_gripper.dat)
install_variant(kinova_gripper PDGAINS_FILE pdgains/PDgains_sim_gripper.dat)
install_variant(kinova_gripper_2f140 PDGAINS_FILE pdgains/PDgains_sim_gripper.dat)
install_variant(kinova_callib)

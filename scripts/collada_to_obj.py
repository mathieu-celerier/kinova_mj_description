#!/usr/bin/env python3

import argparse
import pathlib
import xml.etree.ElementTree as ET


COLLADA_NS = {"c": "http://www.collada.org/2005/11/COLLADASchema"}


def parse_float_array(mesh, source_id):
    source = mesh.find(f"c:source[@id='{source_id}']", COLLADA_NS)
    if source is None:
        raise RuntimeError(f"Missing source {source_id}")
    float_array = source.find("c:float_array", COLLADA_NS)
    if float_array is None or float_array.text is None:
        raise RuntimeError(f"Missing float_array for {source_id}")
    values = [float(v) for v in float_array.text.split()]
    accessor = source.find("c:technique_common/c:accessor", COLLADA_NS)
    if accessor is None:
        raise RuntimeError(f"Missing accessor for {source_id}")
    stride = int(accessor.attrib.get("stride", "1"))
    count = int(accessor.attrib["count"])
    return [values[i * stride : i * stride + 3] for i in range(count)]


def parse_geometry(root):
    geometry = root.find(".//c:library_geometries/c:geometry", COLLADA_NS)
    if geometry is None:
        raise RuntimeError("No geometry found")
    mesh = geometry.find("c:mesh", COLLADA_NS)
    if mesh is None:
        raise RuntimeError("No mesh found")

    vertices = mesh.find("c:vertices", COLLADA_NS)
    if vertices is None:
        raise RuntimeError("No vertices node found")
    position_source = None
    for input_tag in vertices.findall("c:input", COLLADA_NS):
        if input_tag.attrib["semantic"] == "POSITION":
            position_source = input_tag.attrib["source"].lstrip("#")
            break
    if position_source is None:
        raise RuntimeError("No POSITION input found")
    positions = parse_float_array(mesh, position_source)

    faces = []
    triangle_sets = mesh.findall("c:triangles", COLLADA_NS)
    if not triangle_sets:
        raise RuntimeError("No triangles node found")
    for triangles in triangle_sets:
        vertex_offset = None
        max_offset = 0
        for input_tag in triangles.findall("c:input", COLLADA_NS):
            offset = int(input_tag.attrib.get("offset", "0"))
            max_offset = max(max_offset, offset)
            if input_tag.attrib["semantic"] == "VERTEX":
                vertex_offset = offset
        if vertex_offset is None:
            raise RuntimeError("No VERTEX input found")

        p = triangles.find("c:p", COLLADA_NS)
        if p is None or p.text is None:
            raise RuntimeError("No triangle index data found")
        indices = [int(v) for v in p.text.split()]
        stride = max_offset + 1
        if len(indices) % (3 * stride) != 0:
            raise RuntimeError("Unexpected triangle index count")

        for i in range(0, len(indices), 3 * stride):
            tri = []
            for j in range(3):
                tri.append(indices[i + j * stride + vertex_offset] + 1)
            faces.append(tri)
    return positions, faces


def write_obj(path, positions, faces):
    with path.open("w", encoding="ascii") as f:
        f.write("# Converted from COLLADA\n")
        for x, y, z in positions:
            f.write(f"v {x:.9g} {y:.9g} {z:.9g}\n")
        for a, b, c in faces:
            f.write(f"f {a} {b} {c}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=pathlib.Path)
    parser.add_argument("dst", type=pathlib.Path)
    args = parser.parse_args()

    root = ET.parse(args.src).getroot()
    positions, faces = parse_geometry(root)
    write_obj(args.dst, positions, faces)


if __name__ == "__main__":
    main()

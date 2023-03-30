import re
import sys
from lxml import etree

def create_drawio_node(node_id, label, x, y, width, height):
    node = etree.Element("mxCell", id=node_id, value=label, style="rounded=1;whiteSpace=wrap;html=1;", vertex="1", parent="1")
    geometry = etree.SubElement(node, "mxGeometry", x=str(x), y=str(y), width=str(width), height=str(height), attrib={"as": "geometry"})
    return node

def create_drawio_edge(edge_id, points):
    edge = etree.Element("mxCell", id=edge_id, style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;", edge="1", source="", target="", parent="1")
    geometry = etree.SubElement(edge, "mxGeometry", relative="1", attrib={"as": "geometry"})

    for index, point in enumerate(points):
        if index == 0:
            geometry.set("x", str(point[0]))
            geometry.set("y", str(point[1]))
        else:
            etree.SubElement(geometry, "mxPoint", x=str(point[0]), y=str(point[1]), attrib={"as": f"points.{index}"})

    return edge

def xdot_to_drawio(xdot_filename, output_filename):
    with open(xdot_filename, "r") as xdot_file:
        xdot_content = xdot_file.read()

    # Parse node and edge data
    node_pattern = r'(\w+) \[pos="([\d.]+),([\d.]+)", width="([\d.]+)", height="([\d.]+)", label="([^"]*)"\];'
    edge_pattern = r'(\w+) -> (\w+) \[pos="e,([\d.]+),([\d.]+) ((?:[\d.]+,){1,}[\d.]+)"\];'

    node_matches = re.findall(node_pattern, xdot_content)
    edge_matches = re.findall(edge_pattern, xdot_content)

    # Initialize draw.io XML structure
    root = etree.Element("mxGraphModel")
    root.set("dx", "1424")
    root.set("dy", "844")
    root.set("grid", "1")
    root.set("gridSize", "10")
    root.set("guides", "1")
    root.set("tooltips", "1")
    root.set("connect", "1")
    root.set("arrows", "1")
    root.set("fold", "1")
    root.set("page", "1")
    root.set("pageScale", "1")
    root.set("pageWidth", "827")
    root.set("pageHeight", "1169")
    root.set("math", "0")
    root.set("shadow", "0")

    root.append(etree.Element("root"))
    root[-1].append(etree.Element("mxCell", id="0"))
    root[-1].append(etree.Element("mxCell", id="1", parent="0"))

    # Create draw.io nodes
    for node_match in node_matches:
        node_id, x, y, width, height, label = node_match
        x = float(x) - (float(width) * 36) / 2
        y = -float(y) - (float(height) * 36) / 2
        width = float(width) * 36
        height = float(height) * 36
        node = create_drawio_node(node_id, label, x, y, width, height)
        root[-1].append(node)

    # Create draw.io edges
    for edge_match in edge_matches:
        source_id, target_id, end_x, end_y, points_str = edge_match
        points = [(float(x), -float(y)) for x, y in zip(*[iter(points_str.split(','))] * 2)]
        edge_id = f"{source_id}_{target_id}"
        edge = create_drawio_edge(edge_id, points)
        root[-1].append(edge)

    # Save draw.io XML file
    with open(output_filename, "wb") as output_file:
        output_file.write(etree.tostring(root, pretty_print=True, encoding="utf-8"))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} input.xdot output.drawio")
        sys.exit(1)

    xdot_filename = sys.argv[1]
    output_filename = sys.argv[2]

    xdot_to_drawio(xdot_filename, output_filename)

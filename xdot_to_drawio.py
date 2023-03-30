import re
import sys
from lxml import etree

with open(sys.argv[1], 'r') as file:
    xdot_data = file.read()

node_pattern = re.compile(r'(?:"(.*?)"\s+\[.*?label="(.*?)".*?pos="(.*?),(.*?)".*?width="(.*?)".*?height="(.*?)".*?\];)', re.DOTALL)
edge_pattern = re.compile(r'(?:"(.*?)" -> "(.*?)".*?pos="(.*?)";)', re.DOTALL)

root = etree.Element("mxGraphModel")
root.set("dx", "0")
root.set("dy", "0")
root.set("grid", "1")
root.set("gridSize", "10")
root.set("guides", "1")
root.set("tooltips", "1")
root.set("connect", "1")
root.set("arrows", "1")
root.set("fold", "1")
root.set("page", "1")
root.set("pageScale", "1")
root.set("pageWidth", "850")
root.set("pageHeight", "1100")
root.set("background", "#ffffff")

root.append(etree.Comment(" The following elements are layers. "))

parent = etree.SubElement(root, "mxCell", id="1")
parent.set("parent", "0")

root.append(etree.Comment(" The following elements are vertices. "))

for match in node_pattern.finditer(xdot_data):
    id, label, x, y, width, height = match.groups()
    x, y, width, height = float(x), float(y), float(width), float(height)

    node = etree.SubElement(parent, "mxCell", id=id, value=label, vertex="1", style="rounded=1;whiteSpace=wrap;html=1;")
    node.set("parent", "1")

    geometry = etree.SubElement(node, "mxGeometry", x=str(x), y=str(y), width=str(width), height=str(height), attrib={"as": "geometry"})

root.append(etree.Comment(" The following elements are edges. "))

for match in edge_pattern.finditer(xdot_data):
    source, target, pos = match.groups()
    points = pos.split(" ")

    edge = etree.SubElement(parent, "mxCell", edge="1", source=source, target=target, style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;")
    edge.set("parent", "1")

    geometry = etree.SubElement(edge, "mxGeometry", relative="1", attrib={"as": "geometry"})
    array = etree.SubElement(geometry, "Array", attrib={"as": "points"})

    for i in range(0, len(points) - 1, 2):
        x, y = points[i], points[i + 1]
        etree.SubElement(array, "mxPoint", x=x, y=y)

etree.ElementTree(root).write(sys.argv[2], pretty_print=True, xml_declaration=True, encoding="UTF-8")

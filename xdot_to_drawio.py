import sys
import pydot
from lxml import etree

dot_graph = pydot.graph_from_dot_file(sys.argv[1])[0]

mxGraphModel = etree.Element("mxGraphModel")
mxGraphModel.set("dx", "0")
mxGraphModel.set("dy", "0")
mxGraphModel.set("grid", "1")
mxGraphModel.set("gridSize", "10")
mxGraphModel.set("guides", "1")
mxGraphModel.set("tooltips", "1")
mxGraphModel.set("connect", "1")
mxGraphModel.set("arrows", "1")
mxGraphModel.set("fold", "1")
mxGraphModel.set("page", "1")
mxGraphModel.set("pageScale", "1")
mxGraphModel.set("pageWidth", "850")
mxGraphModel.set("pageHeight", "1100")
mxGraphModel.set("background", "#ffffff")

root = etree.SubElement(mxGraphModel, "root")

layer0 = etree.SubElement(root, "mxCell", id="0")
layer1 = etree.SubElement(root, "mxCell", id="1", parent="0")

root.append(etree.Comment(" The following elements are vertices. "))

for node in dot_graph.get_nodes():
    if node.get_name() in ['node', 'graph', '"\\n"']:
        continue
    id_ = node.get_name().strip('"')
    label = node.get("label").strip('"').replace("\\n", "<br>")
    pos = node.get("pos") or '"0,0"'
    pos = pos.strip('"').split(",")
    x, y = float(pos[0]), float(pos[1])
    width = node.get("width") or '"0"'
    width = float(width.strip('"')) * 72
    height = node.get("height") or '"0"'
    height = float(height.strip('"')) * 72

    xml_node = etree.SubElement(root, "mxCell", id=id_, value=label, vertex="1", style="rounded=1;whiteSpace=wrap;html=1;")
    xml_node.set("parent", "1")

    geometry = etree.SubElement(xml_node, "mxGeometry", x=str(x), y=str(y), width=str(width), height=str(height), attrib={"as": "geometry"})

root.append(etree.Comment(" The following elements are edges. "))

for edge in dot_graph.get_edges():
    source, target = edge.get_source().strip('"'), edge.get_destination().strip('"')
    pos = edge.get("pos").strip('"').split(" ")[1:-1]

    xml_edge = etree.SubElement(root, "mxCell", edge="1", source=source, target=target, style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;")
    xml_edge.set("parent", "1")

    geometry = etree.SubElement(xml_edge, "mxGeometry", relative="1", attrib={"as": "geometry"})
    #array = etree.SubElement(geometry, "Array", attrib={"as": "points"})

    #for i in range(0, len(pos), 2):
    #    x, y = pos[i].split(",")
    #    etree.SubElement(array, "mxPoint", x=x, y=y)

etree.ElementTree(mxGraphModel).write(sys.argv[2], pretty_print=True, xml_declaration=True, encoding="UTF-8")

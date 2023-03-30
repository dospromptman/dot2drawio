import csv
import sys

def csv_to_dot(input_filename, output_filename):
    nodes = {}
    edges = []

    with open(input_filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            metadata_id = row["MetadataComponentId"]
            metadata_type = row["MetadataComponentType"]
            metadata_name = row["MetadataComponentName"]
            ref_metadata_id = row["RefMetadataComponentId"]
            ref_metadata_type = row["RefMetadataComponentType"]
            ref_metadata_name = row["RefMetadataComponentName"]

            nodes[metadata_id] = f"{metadata_type}\\n{metadata_name}"
            nodes[ref_metadata_id] = f"{ref_metadata_type}\\n{ref_metadata_name}"
            edges.append((metadata_id, ref_metadata_id))

    with open(output_filename, "w") as dotfile:
        dotfile.write("digraph G {\n")
        dotfile.write('  rankdir="LR";\n')  # Set graph layout direction to left-to-right
        dotfile.write('  splines=ortho;\n')  # Set graph to prefer orthogonal splines that route around nodes
        dotfile.write('  node [shape=box];\n')  # Set default node shape to box

        for node_id, label in nodes.items():
            dotfile.write(f'  "{node_id}" [label="{label}"];\n')

        for edge in edges:
            dotfile.write(f'  "{edge[0]}" -> "{edge[1]}";\n')

        dotfile.write("}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} input.csv output.dot")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    csv_to_dot(input_filename, output_filename)

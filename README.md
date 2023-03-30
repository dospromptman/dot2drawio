Convert CSV file to dot graph:

```
    python csv_to_dot.py input.csv graph.dot
```

Run layout algorithm on graph.dot:

```
     dot -Tdot -ooutput.dot graph.dot
```

Alternatively, generate PNG directly from graph.dot:

```
     dot -Tpng -ooutput.png graph.dot
```

Convert dot with layout information to drawio xml format:

```
    python xdot_to_drawio.py output.dot output.drawio
```

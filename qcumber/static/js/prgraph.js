(function() {
    // Define the padding for the nodes
    var nodePadding = 5;

    // Add the edges property to every state
    for (var prop in stateKeys) {
        stateKeys[prop].edges = [];
    }

    function spline(e) {
        var points = e.dagre.points.slice(0);
        var source = dagre.util.intersectRect(e.source.dagre, points[0]);
        var target = dagre.util.intersectRect(e.target.dagre, points[points.length - 1]);
        points.unshift(source);
        points.push(target);
        return d3.svg.line()
            .x(function(d) { return d.x; })
            .y(function(d) { return d.y; })
            .interpolate("linear")
            (points);
    }

    // Translates all points in the edge using `dx` and `dy`.
    function translateEdge(e, dx, dy) {
        e.dagre.points.forEach(function(p) {
            p.x = Math.max(0, Math.min(svgBBox.width, p.x + dx));
            p.y = Math.max(0, Math.min(svgBBox.height, p.y + dy));
        });
    }

    // Get the data in the right form
    transitions.forEach(function(d) {
        var source = stateKeys[d.source],
                target = stateKeys[d.target];
        source.edges.push(d);
        target.edges.push(d);
    });
    var states = d3.values(stateKeys);
    transitions.forEach(function(d) {
        d.source = stateKeys[d.source];
        d.target = stateKeys[d.target];
    });

    // Now start laying things out
    var svg = d3.select("svg#graph");
    var svgGroup = svg.append("g").attr("transform", "translate(5, 5)");

    // `nodes` is center positioned for easy layout later
    var nodes = svgGroup
        .selectAll("g .node")
        .data(states)
        .enter()
            .append("g")
            .attr("class", function(d) { return "node " + d.type; })
            .attr("id", function(d) { return "node-" + d.label; });

    var edges = svgGroup
        .selectAll("path .edge")
        .data(transitions)
        .enter()
            .append("path")
            .attr("class", function(d) { return "edge " + d.type; })
            .attr("marker-end", "url(#arrowhead)");

    // Append rectangles to the nodes. We do this before laying out the text
    // because we want the text above the rectangle.
    var rects = nodes.append("rect");

    // Append text
    var labels = nodes
        .append("text")
            .attr("text-anchor", "middle")
            .attr("x", 0);

    labels
        .append("tspan")
        .attr("x", 0)
        .attr("dy", "1em")
        .text(function(d) { return d.label; });

    // We need width and height for layout.
    labels.each(function(d) {
        var bbox = this.getBBox();
        d.bbox = bbox;
        d.width = bbox.width + 2 * nodePadding;
        d.height = bbox.height + 2 * nodePadding;
    });

    rects
        .attr("x", function(d) { return -(d.bbox.width / 2 + nodePadding); })
        .attr("y", function(d) { return -(d.bbox.height / 2 + nodePadding); })
        .attr("width", function(d) { return d.width; })
        .attr("height", function(d) { return d.height; })
        .attr("rx", "10")
        .attr("ry", "10");

    labels
        .attr("x", function(d) { return -d.bbox.width / 2; })
        .attr("y", function(d) { return -d.bbox.height / 2; });

    // Create the layout and get the graph
    dagre.layout()
        .nodeSep(50)
        .edgeSep(10)
        .rankSep(50)
        .nodes(states)
        .edges(transitions)
        .debugLevel(1)
        .run();

    nodes.attr("transform", function(d) { return 'translate('+ d.dagre.x +','+ d.dagre.y +')'; });

    // Ensure that we have at least two points between source and target
    edges.each(function(d) {
        var points = d.dagre.points;
        if (!points.length) {
            var s = d.source.dagre;
            var t = d.target.dagre;
            points.push({ x: (s.x + t.x) / 2, y: (s.y + t.y) / 2 });
        }

        if (points.length === 1) {
            points.push({ x: points[0].x, y: points[0].y });
        }
    });

    edges
        // Set the id. of the SVG element to have access to it later
        .attr('id', function(e) { return e.dagre.id; })
        .attr("d", function(e) { return spline(e); });

    // Resize the SVG element
    var svgBBox = svg.node().getBBox();
    svg.attr("width", svgBBox.width + 10);
    svg.attr("height", svgBBox.height + 10);

    // Drag handlers
    var nodeDrag = d3.behavior.drag()
        // Set the right origin (based on the Dagre layout or the current position)
        .origin(function(d) { return d.pos ? {x: d.pos.x, y: d.pos.y} : {x: d.dagre.x, y: d.dagre.y}; })
        .on('drag', function (d, i) {
            var prevX = d.dagre.x,
                    prevY = d.dagre.y;

            // The node must be inside the SVG area
            d.dagre.x = Math.max(d.width / 2, Math.min(svgBBox.width - d.width / 2, d3.event.x));
            d.dagre.y = Math.max(d.height / 2, Math.min(svgBBox.height - d.height / 2, d3.event.y));
            d3.select(this).attr('transform', 'translate('+ d.dagre.x +','+ d.dagre.y +')');

            var dx = d.dagre.x - prevX,
                    dy = d.dagre.y - prevY;

            // Edges position (inside SVG area)
            d.edges.forEach(function(e) {
                translateEdge(e, dx, dy);
                d3.select('#'+ e.dagre.id).attr('d', spline(e));
            });
        });

    var edgeDrag = d3.behavior.drag()
        .on('drag', function (d, i) {
            translateEdge(d, d3.event.dx, d3.event.dy);
            d3.select(this).attr('d', spline(d));
        });

    nodes.call(nodeDrag);
    edges.call(edgeDrag);
})();

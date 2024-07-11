js = """
function updateGraph(programs, relationships) {
    console.log("updateGraph called with:", programs, relationships);
    const width = 800;
    const height = 400;
    const radius = 20;

    d3.select("#relationship-graph").selectAll("*").remove();
    const svg = d3.select("#relationship-graph")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const simulation = d3.forceSimulation(programs)
        .force("charge", d3.forceManyBody().strength(-200))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collision", d3.forceCollide().radius(radius * 1.5));

    const link = svg.selectAll("line")
        .data(relationships)
        .enter().append("line")
        .style("stroke", "#999")
        .style("stroke-opacity", 0.6)
        .style("stroke-width", d => d.value * 2);

    const node = svg.selectAll("circle")
        .data(programs)
        .enter().append("circle")
        .attr("r", radius)
        .style("fill", (d, i) => d3.schemeCategory10[i % 10])
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    const label = svg.selectAll("text")
        .data(programs)
        .enter().append("text")
        .text(d => d.name)
        .attr("font-size", "10px")
        .attr("dx", 12)
        .attr("dy", 4);

    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x = Math.max(radius, Math.min(width - radius, d.x)))
            .attr("cy", d => d.y = Math.max(radius, Math.min(height - radius, d.y)));

        label
            .attr("x", d => d.x)
            .attr("y", d => d.y);
    });

    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;

        // Calculate and update relationships
        programs.forEach((p1, i) => {
            programs.forEach((p2, j) => {
                if (i < j) {
                    const dx = p1.x - p2.x;
                    const dy = p1.y - p2.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    const maxDistance = Math.sqrt(width * width + height * height);
                    const relationship = 1 - (distance / maxDistance);
                    relationships.push({source: i, target: j, value: relationship});
                }
            });
        });

        // Send updated relationships to Python
        const relationshipMatrix = programs.map(() => Array(programs.length).fill(0));
        relationships.forEach(rel => {
            relationshipMatrix[rel.source][rel.target] = rel.value;
            relationshipMatrix[rel.target][rel.source] = rel.value;
        });
        gradio('updateRelationships', relationshipMatrix);
    }
}

function initGraph() {
    if (typeof d3 === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://d3js.org/d3.v7.min.js';
        script.onload = () => {
            console.log('D3.js loaded');
            // After D3.js is loaded, initialize the graph if there's data
            const graphData = document.getElementById('graph-data');
            if (graphData) {
                const data = JSON.parse(graphData.textContent);
                updateGraph(data.programs, data.relationships);
            }
        };
        document.head.appendChild(script);
    }
}

// Call initGraph when the page loads
if (document.readyState === 'complete') {
    initGraph();
} else {
    window.addEventListener('load', initGraph);
}
"""
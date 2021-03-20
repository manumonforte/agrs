let svg = d3.select("svg"),
    width = +svg.node().getBoundingClientRect().width,
    height = +svg.node().getBoundingClientRect().height;

let link, node;
let graph;

metrics = {
    "centrality" : true,
    "closeness" : false,
    "betweenness" : false,
    "eigenvector" : false,
    "pagerank" : false
}

const tool_tip = d3.tip()
    .attr("class", "d3-tip")
    .offset([-8, 0])
    .html(function (d) {

        let message = "<strong><center>" + d['id'] + "</strong></center><br>" +
            "<strong>Followers: </strong> " + d['followers'] + "<br>" +
            "<strong>Avg Popularity Songs: </strong> " + d['avg_popularity_songs'] + "<br>" +
            "<strong>Artist Popularity: </strong> " + d['popularity'] + "<br>"

        if (metrics.centrality)
            message += "<strong>Centrality: </strong> " + d['centrality'] + "<br>"
        else if (metrics.closeness)
            message += "<strong>Closeness: </strong> " + d['closeness'] + "<br>"
        else if (metrics.betweenness)
            message += "<strong>Betweenness: </strong> " + d['betweenness'] + "<br>"
        else if (metrics.eigenvector)
            message += "<strong>Eigenvector: </strong> " + d['eigenvector'] + "<br>"
        else
            message += "<strong>Pagerank: </strong> " + d['pagerank'] + "<br>"

        return message
    });

svg.call(tool_tip);

// load the data
d3.json("../data/data_d3js.json", function(error, _graph) {
  if (error) throw error;
  graph = _graph;
  initializeDisplay();
  initializeSimulation();
});

var simulation;

function initializeSimulation() {
    simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force('collide', d3.forceCollide(function (d) {
            return 20
        }));

    simulation.nodes(graph.nodes)
      .on("tick", ticked);

    simulation.force("link")
      .links(graph.links);
}

function update_node_size() {
    node.attr("r", node_size)
}

function initializeDisplay() {

  link = svg.append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(graph.links)
      .enter().append("line").attr("stroke-width", edge_size);

  link.append("title").text(function(d) {
      return d.source + " - " + d.value + " - " + d.target;
  });

  node = svg.append("g")
      .attr("class", "nodes")
      .selectAll("circle")
      .data(graph.nodes)
      .enter().append("circle")
      .attr("r", node_size)
      .attr("fill", node_color)
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended))
      .on('mouseover', tool_tip.show)
      .on('mouseout', tool_tip.hide);

}

function node_color(d) {
    if(d.popularity >= 90) return 'green'
    else if (d.popularity < 90 && d.popularity >= 50) return '#9f00ff'
    else if (d.popularity < 50 && d.popularity >= 25) return 'orange'
    else return 'red'
}

function node_size(d) {
    if (metrics.betweenness)
        return d.betweenness + 10
    else if (metrics.centrality)
        return d.centrality + 10
    else if (metrics.closeness)
        return d.closeness + 10
    else if (metrics.eigenvector)
        return d.eigenvector + 10
    else
        return d.pagerank + 10
}

function edge_size(d) {
    return d.value * 3;
}

// update the display positions after each simulation tick
function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    d3.select('#alpha_value').style('flex-basis', (simulation.alpha()*100) + '%');
}

//////////// UI EVENTS ////////////

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0.0001);
  d.fx = null;
  d.fy = null;
}

// update size-related forces
d3.select(window).on("resize", function(){
    width = +svg.node().getBoundingClientRect().width;
    height = +svg.node().getBoundingClientRect().height;
    update_node_size();
});

function updateAll() {
    update_node_size();
}

function clearMetrics(){
    metrics = {
        "centrality": false,
        "closeness": false,
        "betweenness": false,
        "eigenvector": false,
        "pagerank": false
    }
}
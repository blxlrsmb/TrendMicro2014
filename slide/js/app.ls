margin =
  top: 30
  right: 20
  bottom: 30
  left: 50
width = 700-margin.left - margin.right
height = 340-margin.top - margin.bottom

# pie

do ->
  ww = 700
  hh = 400
  w = ww - margin.left - margin.right
  h = hh - margin.top - margin.bottom

  svg = d3.select('#pie')
  .append 'svg'
    .attr 'class', 'pie'
    .attr('width', ww)
    .attr('height', hh)

  data =
    * label: 0, value: 241110, color: '#3366cc'
    * label: 1, value: 65343, color: '#dc3912'
    * label: 2, value: 56960, color: '#ff9900'
    * label: 3, value: 38178, color: '#109618'
    * label: 4, value: 27335, color: '#990099'
    * label: 5, value: 22464, color: '#663300'
    * label: 6, value: 660165, color: '#888'

  gradPie.draw svg, data, ww/2, 200, 170

# peak

do ->
  ww = 700
  hh = 400
  margin =
    top: 10
    right: 10
    bottom: 40
    left: 80
  w = ww - margin.left - margin.right
  h = hh - margin.top - margin.bottom

  x = d3.time.scale().range([0, w])
  y = d3.scale.linear().range([h, 0])
  xAxis = d3.svg.axis().scale(x).orient('bottom')
  yAxis = d3.svg.axis().scale(y).orient('left')
  color = d3.scale.category10()
  line = d3.svg.line()
    .interpolate 'basic'
    .x -> x(it.date)
    .y -> y(it.value)
  area = d3.svg.area()
    .x -> x(it.date)
    .y0 height
    .y1 -> y(it.close)

  svgPeak = d3.select('#virus-attack')
  .append 'svg'
    .attr 'class', 'peak'
    .attr 'width', ww
    .attr 'height', hh
  .append('g')
    .attr 'transform', 'translate(' + margin.left + ',' + margin.top + ')'

  d3.csv '3peaks.csv', (err,data)!->
    parseDate = d3.time.format('%m/%d/%Y').parse

    color.domain d3.keys(data[0]).filter -> it != 'date'

    data.forEach (d)!->
      d.date = parseDate d.date

    cities = color.domain().map (name)->
      name: name
      values: data.map (d)->
        date: d.date
        value: +d[name]

    x.domain d3.extent data, -> it.date
    y.domain [
      d3.min(cities, -> d3.min(it.values, -> it.value))
      d3.max(cities, -> d3.max(it.values, -> it.value))
    ]

    svgPeak.append 'g'
      .attr 'class', 'x axis'
      .attr 'transform', "translate(0,#{h})"
      .call xAxis
    svgPeak.append 'g'
      .attr 'class', 'y axis'
      .call yAxis

    city = svgPeak.selectAll '.peak-item'
      .data(cities)
      .enter().append("g")
        .attr("class", "peak-item")

    city.append 'path'
        .attr 'class', 'line'
        .attr 'd', -> line it.values
        .style 'stroke', -> color it.name

# det-web-plot

do ->
  ww = 700
  hh = 400
  margin =
    top: 10
    right: 10
    bottom: 20
    left: 40
  w = ww - margin.left - margin.right
  h = hh - margin.top - margin.bottom

  x = d3.scale.linear().range [0, w]
  y = d3.scale.linear().range [h, 0]
  xAxis = d3.svg.axis().scale(x).orient('bottom')
  yAxis = d3.svg.axis().scale(y).orient('left')
  color = d3.scale.category10()
  line = d3.svg.line()
    .interpolate 'basic'
    .x -> x(it.date)
    .y -> y(it.value)

  svgScatter = d3.select('#correlation')
  .append 'svg'
    .attr 'class', 'scatter'
    .attr 'width', ww
    .attr 'height', hh
  .append('g')
    .attr 'transform', 'translate(' + margin.left + ',' + margin.top + ')'

  d3.csv 'det_web_plot.csv', (err,data)!->
    data.forEach !->
      it.x = +it['rank(det-files)']
      it.y = +it['rank(web-ratio)']

    x.domain d3.extent data, -> it.x
    yr = d3.extent data, -> it.y
    y.domain [yr[0], yr[1]+10]

    svgScatter.append 'g'
      .attr 'class', 'x axis'
      .attr 'transform', "translate(0,#{h})"
      .call xAxis
    .append 'text'
      .attr 'x', w
      .attr 'y', -6
      .style 'text-anchor', 'end'
      .text 'rank(det-files)'
    svgScatter.append 'g'
      .attr 'class', 'y axis'
      .call yAxis
    .append 'text'
      .attr 'y', '1em'
      .attr 'transform', 'rotate(-90)'
      .style 'text-anchor', 'end'
      .text 'rank(web-ratio)'

    svgScatter.selectAll '.point'
      .data data
      .enter().append 'circle'
        .attr 'class', -> if it.y >= yr[1] then 'point green' else 'point'
        .attr 'r', 1.5
        .attr 'cx', -> x(it.x)
        .attr 'cy', -> y(it.y)

# dendrogram

do ->
  margin =
    top: 10
    right: 80
    bottom: 10
    left: 100
  ww = 700
  hh = 400
  w = ww - margin.left - margin.right
  h = hh - margin.top - margin.bottom

  svg = d3.select('#summary')
  .append('svg')
    .attr 'class', 'dendrogram'
    .attr('width', w+margin.left+margin.right)
    .attr('height', h+margin.top+margin.bottom)
  .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

  cluster = d3.layout.cluster().size [h, w]
  diagonal = d3.svg.diagonal().projection -> [it.y, it.x]
  data =
    name: 'Renew Label'
    children:
      * name: 'File Detection Logs'
        children:
          * name: 'Data Cleaning - Burst of Virus'
          * name: 'Correlation Analysis'
      * name: 'Web Reputation Service Logs'
        children:
          * name: 'Score & Category Distribution'
          * name: 'Feature Selection & Visualization'
          * name: 'Learning with Different Models'

  nodes = cluster.nodes data
  links = cluster.links nodes

  link = svg.selectAll('.link')
    .data links
    .enter()
      .append 'path'
      .attr 'class', 'link'
      .attr 'd', diagonal

  node = svg.selectAll '.node'
    .data nodes
    .enter()
      .append 'g'
      .attr 'class', 'node'
      .attr 'transform', -> "translate(#{it.y},#{it.x})"
  node.append 'circle'
    .attr 'r', 4.5
  node.append 'text'
    .attr 'dx', ->
      if it.name.length > 7
        '-3em'
      else
        '-1em'
    .attr 'dy', '1.5em'
    .style 'text-anchor', 'middle'
    .text -> it.name

# curve

do ->
  svg = d3.select('#overview')
  .append('svg')
    .attr 'class', 'curve'
    .attr('width', width+margin.left+margin.right)
    .attr('height', height+margin.top+margin.bottom)
  .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

  x = d3.time.scale().range([0, width])
  y = d3.scale.linear().range([height, 0])
  xAxis = d3.svg.axis().scale(x).orient('bottom').ticks(5)
  yAxis = d3.svg.axis().scale(y).orient('left').ticks(5)
  valueline = d3.svg.line()
    .interpolate 'monotone'
    .x -> x(it.date)
    .y -> y(it.close)
  area = d3.svg.area()
    .x -> x(it.date)
    .y0 height
    .y1 -> y(it.close)

  parseDate = d3.time.format('%d-%b-%Y').parse

  d3.tsv 'data.tsv', (err,data)!->
    data.forEach (d)!->
      d.date = parseDate d.date
      d.close = + d.close

    x.domain d3.extent data, -> it.date
    y.domain [0, d3.max(data, -> it.close)]

    svg.append 'path'
      .datum data
      .attr 'class', 'line'
      .attr 'd', valueline
    svg.append 'g'
      .attr 'class', 'x axis'
      .attr 'transform', "translate(0,#{height})"
      .call xAxis
    svg.append 'g'
      .attr 'class', 'y axis'
      .call yAxis

  update = ->
    d3.tsv 'data-alt.tsv', (err,data)!->
      data.forEach (d)!->
        d.date = parseDate d.date
        d.close = +d.close
      x.domain d3.extent data, -> it.date
      y.domain [0, d3.max(data, -> it.close)]

      svgT = svg.transition()
      svgT.select('.line')
        .duration 750
        .attr 'd', valueline(data)
      svgT.select('.x.axis')
        .duration 750
        .call xAxis
      svgT.select('.y.axis')
        .duration 750
        .call yAxis

  d3.select('svg.curve').on 'click', !->
    update()


## histogram

do ->
  margin =
    top: 10
    right: 20
    bottom: 140
    left: 60
  ww = 700
  hh = 400
  w = ww - margin.left - margin.right
  h = hh - margin.top - margin.bottom

  svg = d3.select('#score')
  .append('svg')
    .attr 'class', 'hbar'
    .attr('width', width+margin.left+margin.right)
    .attr('height', height+margin.top+margin.bottom)
  .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

  x = d3.scale.ordinal().rangeRoundBands [0,w],1
  y = d3.scale.linear().range([h, 0])
  xAxis = d3.svg.axis().scale(x).orient('bottom')
  yAxis = d3.svg.axis().scale(y).orient('left')

  data =
    * cat: 'Network Bandwidth',         score: 77.602081708764203
    * cat: '2',                         score: 78.34210526315789
    * cat: 'Lifestyle',                 score: 77.14724767197356
    * cat: 'Business',                  score: 77.797198165228764
    * cat: 'General',                   score: 76.060396893874028
    * cat: '19',                        score: 76.32353596205806
    * cat: 'Communications and Search', score: 76.07692307692308
    * cat: 'Adult',                     score: 77.495485036119717
    * cat: 'Internet Security',         score: 77.884321646566207
    * cat: '92',                        score: 77.207253886010363
    * cat: '93',                        score: 77.402389139028898

  x.domain data.map -> it.cat
  y.domain [0, d3.max(data, -> it.score)]

  svg.append 'g'
    .attr 'class', 'x axis'
    .attr 'transform', "translate(0,#{h})"
    .call xAxis
  svg.append 'g'
    .attr 'class', 'y axis'
    .call yAxis
    .append 'text'
      .attr 'y', '-3em'
      .attr 'transform', 'rotate(-90)'
      .style 'text-anchor', 'end'
      .text 'Average score'

  svg.selectAll '.hbar'
    .data data
    .enter().append 'rect'
      .attr 'class', 'hbar'
      .attr 'x', -> x(it.cat)
      .attr 'width', 40
      .attr 'y', -> y(it.score)
      .attr 'height', -> h - y(it.score)

  svg.selectAll '.x.axis text'
    .attr 'transform', 'rotate(40)'
    .attr 'dx', '1em'
    .attr 'dy', '1em'
    .style 'text-anchor', 'start'

## histogram2

do ->
  margin =
    top: 10
    right: 20
    bottom: 140
    left: 60
  ww = 700
  hh = 400
  w = ww - margin.left - margin.right
  h = hh - margin.top - margin.bottom

  svg = d3.select('#predict-cont')
  .append('svg')
    .attr 'class', 'hbar'
    .attr('width', width+margin.left+margin.right)
    .attr('height', height+margin.top+margin.bottom)
  .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

  x = d3.scale.ordinal().rangeRoundBands [0,w],1
  y = d3.scale.linear().range([h, 0])
  xAxis = d3.svg.axis().scale(x).orient('bottom')
  yAxis = d3.svg.axis().scale(y).orient('left')

  d3.tsv 'feature-weight.tsv', (err,data)!->
    data.forEach (d)!->
      d.weight = + d.weight

    x.domain data.map -> it.feature
    y.domain [0, d3.max(data, -> it.weight)]

    svg.append 'g'
      .attr 'class', 'x axis'
      .attr 'transform', "translate(0,#{h})"
      .call xAxis
    svg.append 'g'
      .attr 'class', 'y axis'
      .call yAxis
      .append 'text'
        .attr 'y', '-3em'
        .attr 'transform', 'rotate(-90)'
        .style 'text-anchor', 'end'
        .text 'Weight'

    svg.selectAll '.hbar'
      .data data
      .enter().append 'rect'
        .attr 'class', 'hbar'
        .attr 'x', -> x(it.feature)
        .attr 'width', 40
        .attr 'y', -> y(it.weight)
        .attr 'height', -> h - y(it.weight)

    svg.selectAll '.x.axis text'
      .attr 'transform', 'rotate(40)'
      .attr 'dx', '2em'
      .attr 'dy', '0em'
      .style 'text-anchor', 'start'

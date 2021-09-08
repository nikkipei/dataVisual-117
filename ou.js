d3 = require("d3@6")
mapboxgl = require('mapbox-gl@~0.44.1/dist/mapbox-gl.js')
deck = require('deck.gl@~5.2.0/deckgl.min.js')
deck = require('deck.gl@~5.2.0/deckgl.min.js')
// import { Select } from "@observablehq/inputs"
// import { soFetch } from '@alecglassford/so-fetch'
// import {slider, select} from '@jashkenas/inputs'
arrow = require('apache-arrow@0.3.1')
topojson = require('topojson')
// import {loadData, range, getMarkdown, toDate} from '@randomfractals/apache-arrow'
// import { Table } from "@observablehq/table"
console.log("+111111111")
movingAverage = (data, window) => {
 
  const result =[]
  if (data.length < window) {
    return result;
  }
  let sum = 0;
  for (let i = 0; i < data.length; ++i) {
    if(i<window)
    {
      result.push([data[i][0],0])
  
    }
    else
    {
      sum=0
      for (let j = 0; j < window; ++j)
      {
        sum += data[i-j][1]

      }
      
      result.push([data[i][0],sum/window])
    
      
    }
    
    
    
  }
 
  return result;
}

display = function(inputID){
  if(inputID=="all")
  {
  return drawTable(carIDs)
  }
  else
  {
    return drawChart(inputID)
  }
}

getSVG = () => {
  const svgElement = DOM.svg(800, 300);

  const svg = d3
    .select(svgElement)
    .append("g")
    .attr("transform", `translate(${margin*2},${margin})`);
  return [svgElement, svg];
}
UAVFilterDataSpeedByID(UAVFilterData,1)[1][0]
d3.max(UAVFilterDataSpeedByID(UAVFilterData,1)[1].map(d => d[1]))
svgHeight =250
svgWidth=250
margin =40
chartWidth=svgWidth-margin
chartHeight=svgHeight-2*margin
UAVFilterDataSpeedByID=(data,id) => {
  const tmpData=data.filter( d =>d[1] ==id).map(d=>[d[0],d[2]])
  const tmpArray=[]

  tmpArray.push(id)
  tmpArray.push(tmpData)
  return tmpArray
}
UAVFilterDataSingleSpeedByID(UAVFilterData,2) 
UAVFilterDataSingleSpeedByID=(data,id) => {
  const tmpData=data.filter( d =>d[1] ==id).map(d=>d[2])
  return tmpData
}
UAVFilterDataDatesByID=(data,id) => {
  const tmpData=data.filter( d =>d[1] ==id).map(d=>d[0])
  return tmpData
}
UAVFilterData=UAVData.reduce((accmulator,currentElement)=>{
    accmulator.push([currentElement.frameNUM,currentElement.carID,currentElement.posChange])
  return accmulator;
},[])

// lightSettings = {
//   return {
//     lightsPosition: [-0.144528, 49.739968, 8000, -3.807751, 54.104682, 8000],
//     ambientRatio: 0.4,
//     diffuseRatio: 0.6,
//     specularRatio: 0.2,
//     lightsStrength: [0.8, 0.0, 0.8, 0.0],
//     numberOfLights: 2
//   };
// }

function onHover (info) {
  const {x, y, object} = info;
  if (object) {
    tooltip.style.left = `${x}px`;    
    tooltip.style.top = `${y}px`;
    tooltip.innerHTML = `car wait for ${Math.round(object.points.length/30)} second`;
  } else { 
    tooltip.innerHTML = '';
  }
}

function filterData(data) {
  let results = []
  for (var i = 0; i < data.length; i++) {
    if(data[i].carID !=carID && carID!="all")
    {
      continue
    }
    results.push({
        'lat': data[i].Lat,
        'lng': data[i].Lng,
        "index":i
    });
}
  return results;
}

 const hexagonLayer = new deck.HexagonLayer({
    id: 'heatmap',
    colorRange,
    data,
    // elevationRange: [1, 5000],
    elevationScale: 1,
    extruded: true,
    getPosition: d => [d.lng,d.lat],
    opacity: 0.5,
    radius: 5,
    coverage: 0.6,
    lightSettings,
    pickable: true,
    autoHighlight: true,
    onHover: onHover,
  });
  deckgl.setProps({layers: [hexagonLayer]});
  return hexagonLayer;


colorRange = {
  return [
    [1, 152, 189],
    [73, 227, 206],
    [216, 254, 181],
    [254, 237, 177],
    [254, 173, 84],
    [209, 55, 78]
  ];
}

tooltip = mapContainer.querySelector('#tooltip')

carIDs=getIdArray()

function getIdArray() {
  let results = []
  results.push("all")
  var tmpId=UAVData[0].carID
  for (var i = 0; i < UAVData.length; i++) {
    if(UAVData[i].carID==tmpId || results.includes(tmpId.toString()))
    {
      continue;
    }
    results.push(tmpId.toString())
    
    tmpId=UAVData[i].carID
    
}
  return results;
}

speedData=getSpeedByID()

function getSpeedByID(){
  let results = []
  var tmpId=UAVData[0].carID
  for (var i = 0; i < UAVData.length; i++) {
    if(carID=="all")
    {
      return results
    }
    if(UAVData[i].carID!=carID)
    {
      continue;
    }
    results.push(UAVData[i].posChange)
    
    
}
  return results;
}

data = filterData(UAVData)

UAVData = (await FileAttachment("test@2.csv").csv({
  typed: true
}))

deckgl = {
  return new deck.DeckGL({
    container: mapContainer,
    map: mapboxgl,
    mapboxAccessToken: 'pk.eyJ1IjoiZGF0YXBpeHkiLCJhIjoiY2tnM3ZhZWJjMDE1ajJxbGY1eTNlemduciJ9.YZ9CJEza0hvAQmTRBhubmQ', //mapboxAccessToken:'pk.eyJ1Ijoib3V6aGVuZyIsImEiOiJja2V2bm5nOWUwNnB2MnNwOWJicGwxY2loIn0.gzyf4FjatSG6g_j84HViag',
    mapStyle: 'https://api.maptiler.com/maps/toner/style.json?key=bMizIsuAeRiZikCLHO9q',
    latitude:28.172049014930117, 
    longitude: 113.04875306301986,
    zoom: 17,
    minZoom: 0,
    maxZoom: 30,
    pitch: 45
  });
}

html `<link href='https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.css' rel='stylesheet' />
mapbox-gl.css`


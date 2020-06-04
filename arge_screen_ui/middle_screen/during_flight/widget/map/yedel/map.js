var map;
var latlngs = Array();

var items = Array();
var Enditems = Array();
var aircarIconU,aircarIconD,aircarIconR,aircarIconL,aircarIconDR,aircarIconUR,aircarIconDL,aircarIconUL;
var polyline;
var marker;
var EndMarker;

function initialize(){
    map = L.map('map').setView([32.38744928,-117.07633626], 17);

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {

        maxZoom: 100
    }).addTo(map);

aircarIconU = L.icon({
    iconUrl: 'img/aircarIconU.png',
    iconSize:     [40, 40], 
    iconAnchor:   [20, 20], 
    popupAnchor:  [0, -20] 
});

aircarIconD = L.icon({
    iconUrl: 'img/aircarIconD.png',
    iconSize:     [40, 40], 
    iconAnchor:   [20, 20],
    popupAnchor:  [0, -20] 
});
aircarIconR = L.icon({
    iconUrl: 'img/aircarIconR.png',
    iconSize:     [40, 40], 
    iconAnchor:   [20, 20],
    popupAnchor:  [0, -20] 
});
aircarIconL = L.icon({
    iconUrl: 'img/aircarIconL.png',
    iconSize:     [40, 40], 
    iconAnchor:   [20, 20],
    popupAnchor:  [0, -20] 
});
aircarIconDR = L.icon({
    iconUrl: 'img/aircarIconDR.png',
    iconSize:     [56, 56], 
    iconAnchor:   [20, 20],
    popupAnchor:  [0, -20] 
});
aircarIconUR = L.icon({
    iconUrl: 'img/aircarIconUR.png',
    iconSize:     [56, 56], 
    iconAnchor:   [20, 20],
    popupAnchor:  [0, -20] 
});
aircarIconDL = L.icon({
    iconUrl: 'img/aircarIconDL.png',
    iconSize:     [56, 56], 
    iconAnchor:   [20, 20],
    popupAnchor:  [0, -20] 
});
aircarIconUL = L.icon({
    iconUrl: 'img/aircarIconUL.png',
    iconSize:     [56, 56], 
    iconAnchor:   [20, 20],
    popupAnchor:  [0, -20] 
});


     marker = new L.marker(map.getCenter(),{icon: aircarIconU}).addTo(map);
 
   // var items = [[52.000,13.015],[52.010,13.010],[52.015,13.025]];

      //items.push([0,1],[0,2],[0,3])
     // window.alert(items)
      //window.alert(items[0])
     // window.alert(items[0][0])
     // window.alert(items[0][1])
    //  window.alert(items[items.length-1])
      
 //var polyline = L.polyline(items, {color: 'red'}).addTo(map);
//map.fitBounds(polyline.getBounds());
/**
        page.runJavaScript("marker =L.Marker(L.latLng({},{})).addTo(map);".format(lat,lng))
Enditems.push([items[items.length-2][0],items[items.length-2][1]],[items[items.length-1][0],items[items.length-1][1]]);
 var polyline = L.polyline(Enditems, {color: 'blue'}).addTo(map);
map.fitBounds(polyline.getBounds());
    
    Enditems = []

items = [[52.000,13.015],[52.010,13.010],[52.015,13.025],[52.010,13.035],[52.015,13.045]];
Enditems.push([items[items.length-2][0],items[items.length-2][1]],[items[items.length-1][0],items[items.length-1][1]]);
 
 var polyline = L.polyline(Enditems, {color: 'green'}).addTo(map);
map.fitBounds(polyline.getBounds());

**/
    
    


  // L.marker(map.getCenter()).addTo(map);
   // marker.bindPopup("Aircar").openPopup();
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.MainWindow = channel.objects.MainWindow;
        if(typeof MainWindow != 'undefined') {
            var onMapMove = function() { MainWindow.onMapMove(map.getCenter().lat, map.getCenter().lng) };
            map.on('move', onMapMove);
            onMapMove();
        }
    });
}

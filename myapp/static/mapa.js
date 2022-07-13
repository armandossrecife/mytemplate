var map;
var idInfoBoxAberto;
var infoBox = [];
var markers = [];

var this_js_script = $('script[src*=mapa]'); // or better regexp to get the file name..

var my_var_1 = this_js_script.attr('data-my_var_1');   

var loja = '';
var qtdPromocoes = '';
var contentString = ''; 
var nomesPromocoes = '';

if (typeof my_var_1 === "undefined" ) {
   var my_var_1 = '/static/mapsStores.json';
}

function initialize() {	
	var centro = {lat:-3.7281295, lng:-38.4954897};

	var latlng = new google.maps.LatLng(centro);
	
    var options = {
        zoom: 17,
	center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("mapa"), options);
}

initialize();

function abrirInfoBox(id, marker) {
	if (typeof(idInfoBoxAberto) == 'number' && typeof(infoBox[idInfoBoxAberto]) == 'object') {
		infoBox[idInfoBoxAberto].close();
	}

	infoBox[id].open(map, marker);
	idInfoBoxAberto = id;
}

function carregarPontos() {
	
	$.getJSON(my_var_1, function(pontos) {
		
		var latlngbounds = new google.maps.LatLngBounds();
		
		$.each(pontos, function(index, ponto) {
			var pontoDegree = {lat: ponto.latitude, lng: ponto.longitude};
			var marker = new google.maps.Marker({
				position: new google.maps.LatLng(pontoDegree),
				title: ponto.name,
				label: ponto.name, 
				icon: '/static/img/pin.png'
			});
			
			var myOptions = {
				content: "<p>" + ponto.id + "</p>",
				pixelOffset: new google.maps.Size(-50, 0)
        	};

			loja = ponto.name;
			qtdPromocoes = ponto.promotions;
			nomesPromocoes = ponto.promotionsNames;
			
			contentString = '<div id="content">'+
			'<div id="siteNotice">'+
			'</div>'+
			'<h2 id="firstHeading" class="firstHeading">' + loja + '</h2>'+
			'<div id="bodyContent">'+
			'<h3>Quantidade de promoções: ' + qtdPromocoes + '</h3>' +  
			'<h3>Promoções: ' + nomesPromocoes + '</h3>'+
			'</div>'+
			'</div>';
			
			var infowindow = new google.maps.InfoWindow({
				content: contentString
				});
			
			infoBox[ponto.id] = new InfoBox(myOptions);
			infoBox[ponto.id].marker = marker;
			
			infoBox[ponto.id].listener = google.maps.event.addListener(marker, 'click', function (e) {
				infowindow.open(map, marker);
			});
			
			markers.push(marker);
			
			latlngbounds.extend(marker.position);
			
		});
		
		var markerCluster = new MarkerClusterer(map, markers, {imagePath: '/static/img/m'});
		
		map.fitBounds(latlngbounds);
		
	});
	
}
carregarPontos();
// QDG Pi Project
// Quantum Degenerate Gases Lab (Madison Research Group)
// graph-and-stat-table.js
// date: May 30, 2016
// author: tristan calderbank
// contact: tristan@alumni.ubc.ca
// purpose: Handles highcharts graph, buttons, stat table
//          


// array indexes

var TEMPERATURE_LONG = 2;
var PRESSURE_LONG = 6;
var HUMIDITY_LONG = 10;

var TEMPERATURE_STAT = 0;
var PRESSURE_STAT = 1;
var HUMIDITY_STAT = 2;

var MAX = 0;
var MIN = 1;
var MEAN = 2;
var STD = 3;

// graph names

var sensor_names_master = ["sensor_0", "sensor_1", "sensor_2", "sensor_3", "sensor_4", "sensor_5", "sensor_6", "sensor_7"]
var sensor_names_mol = ["sensor_0", "sensor_1", "sensor_2", "sensor_3", "sensor_4", "sensor_5", "sensor_6", "sensor_7"]


// options for highcharts graphs

var options_short = {

		chart: {
			type: 'spline',
			zoomType: 'x',
			backgroundColor: 'rgba(255,255,255,0.8)'
		},
		title: {
			text: 'MOL Lab'
		},
		navigator: {
			enabled: true
		},
		rangeSelector: {
			enabled: true,
			inputEnabled: false,
			buttons: [{
				type: 'minute',
				count: 15,
				text: '15m'
			}, {
				type: '30m',
				count: 30,
				text: '30m'
			}, {
				type: 'hour',
				count: 1,
				text: '1h'
			}, {
				type: 'hour',
				count: 6,
				text: '6h'
			}, {
				type: 'hour',
				count: 12,
				text: '12h'
			}, {
				type: 'all',
				text: 'All'
			}]
		},
		tooltip: {
			shared: true,
			crosshairs: true
		},
		xAxis: {
			type: 'datetime'
		},
		yAxis: [{
			title: {
				text: 'Temperature (\xB0C)',
				style: {
					color: '#ea4335'
				}
			}
			},
			{
			title: {
				text: 'Pressure (Kpa)',
				style: {
					color: '#a2d46f'
				}
				},
			opposite: true
			},
			{
			title: {
				text: 'Humidity (%)',
				style: {
					color: '#6fa2d4'
				},
			},
			opposite: true
			}
			],

		series: [
			{
			name: 'temperature',
			color: '#df5e5e',
			yAxis: 0
			},
			{
			name: 'pressure',
			color: '#a2d46f',
			yAxis: 1,
			visible: false
			},
			{
			name: 'humidity',
			color: '#6fa2d4',
			yAxis: 2,
			visible: false
			}
		]
		
	}


var options_long = {

		chart: {
			type: 'spline',
			zoomType: 'x',
			backgroundColor: 'rgba(255,255,255,0.8)'
		},
		title: {
			text: 'Master Table'
		},
		navigator: {
			enabled: true
		},
		rangeSelector: {
			enabled: true,
			allButtonsEnabled: true
		},
		tooltip: {
			shared: true,
			crosshairs: true
		},
		xAxis: {
			type: 'datetime'
		},
		yAxis: [{
			title: {
				text: 'Temperature (\xB0C)',
				style: {
					color: '#ea4335'
				}
			}
			},
			{
			title: {
				text: 'Pressure (Kpa)',
				style: {
					color: '#a2d46f'
				}
				},
			opposite: true
			},
			{
			title: {
				text: 'Humidity (%)',
				style: {
					color: '#6fa2d4'
				},
			},
			opposite: true
			}
			],

		series: [
			{
			name: 'Temperature Mean',
			color: '#df5e5e',
			yAxis: 0,
			zIndex: 1,
			tooltip: {
				valueSuffix: '°C'
			}
			},
			{
			name: 'Temperature Range',
			color: '#e88e8e',
			yAxis: 0,
			type: 'arearange',
			tooltip: {
				valueSuffix: '°C'
			}
			},
			{
			name: 'Pressure Mean',
			color: '#a2d46f',
			yAxis: 1,
			zIndex: 1,
			tooltip: {
				valueSuffix: ' kPa'
			},
			visible: false
			},
			{
			name: 'Pressure Range',
			color: '#bde09a',
			yAxis: 1,
			type: 'arearange',
			tooltip: {
				valueSuffix: ' kPa'
			},
			visible: false
			},
			{
			name: 'Humidity Mean',
			color: '#6fa2d4',
			yAxis: 2,
			zIndex: 1,
			tooltip: {
				valueSuffix: '%'
			},
			visible: false
			},
			{
			name: 'Humidity Range',
			color: '#9abde0',
			yAxis: 2,
			type: 'arearange',
			tooltip: {
				valueSuffix: '%'
			},
			visible: false
			}

		]
		
	}

// initialization for first page load

updateGraphShort("data/page-data/master-sensor-0-short.csv");
updateTable("master-sensor-0-short-stats.csv");
updateGraphTitle("master", 0, "short");


Highcharts.setOptions({
	global: {
		timezoneOffset: 8 * 60
	}
});



//------------------------------------------------#
// getSeries()                                    #
//                                                #
// Given a matrix and column number, returns a    #
// 2D array with the timestamp column and the     #
// chosen column                                  #
//------------------------------------------------#

function getSeries(matrix, column_number){

	var series = new Array(2);

	for(var i = 0; i < matrix.length; i++){

	series[i] = new Array(2);
	series[i][0] = matrix[i][0] * 1000; // Unix --> Javascript timestamp conversion *1000
	series[i][1] = parseFloat(matrix[i][column_number]);

	}

	return series

};

//------------------------------------------------#
// getRangeSeries()                               #
//                                                #
// Given a matrix and two column numbers, returns #
// an 3xn array with the timestamp column and the #
// two chosen columns                             #
//                                                #
//------------------------------------------------#

function getRangeSeries(matrix, column_1, column_2){

	var rangeSeries = new Array(3);

	for(var i = 0; i < matrix.length; i++){

	rangeSeries[i] = new Array(2);
	rangeSeries[i][0] = matrix[i][0] * 1000; // Unix --> Javascript timestamp conversion *1000
	rangeSeries[i][1] = parseFloat(matrix[i][column_1]);
	rangeSeries[i][2] = parseFloat(matrix[i][column_2]);

	}

	return rangeSeries

};

//------------------------------------------------#
// updateGraphLong()                              #
//                                                #
// updates a long term graph with a given         #
// csv file                                       # 
//                                                #
//------------------------------------------------#

function updateGraphLong(path_to_data_file){

$.get(path_to_data_file, function(data){

	short_data = $.csv.toArrays(data);

	temperature_range = getRangeSeries(short_data, TEMPERATURE_LONG + MAX, TEMPERATURE_LONG + MIN);
	temperature_mean = getSeries(short_data, TEMPERATURE_LONG + MEAN)

	pressure_range = getRangeSeries(short_data, PRESSURE_LONG + MAX, PRESSURE_LONG + MIN);
	pressure_mean = getSeries(short_data, PRESSURE_LONG + MEAN)

	humidity_range = getRangeSeries(short_data, HUMIDITY_LONG + MAX, HUMIDITY_LONG + MIN);
	humidity_mean = getSeries(short_data, HUMIDITY_LONG + MEAN)


	options_long.series[0].data = temperature_mean;
	options_long.series[1].data = temperature_range;
	options_long.series[2].data = pressure_mean;
	options_long.series[3].data = pressure_range;
	options_long.series[4].data = humidity_mean;
	options_long.series[5].data = humidity_range;

	$('#container').highcharts(options_long);

});

}

//------------------------------------------------#
// updateGraphShort()                             #
//                                                #
// updates a short term graph with a given        #
// csv file                                       #
//                                                #
//------------------------------------------------#

function updateGraphShort(path_to_data_file){

$.get(path_to_data_file, function(data){

	short_data = $.csv.toArrays(data);
	short_temperature = getSeries(short_data,1);
	short_pressure = getSeries(short_data,2);
	short_humidity = getSeries(short_data,3);

	options_short.series[0].data = short_temperature;
	options_short.series[1].data = short_pressure;
	options_short.series[2].data = short_humidity;

	$('#container').highcharts(options_short);

});

}

//------------------------------------------------#
// getStats()                                     #
//                                                #
// pulls out a column of stats from a 2D array    #
// and returns it as a 1D array                   #
//------------------------------------------------#

function getStats(array, index){

	return [
	       array[index][0],
	       array[index][1], 
	       array[index][2], 
	       array[index][3]
		];

};

//------------------------------------------------#
// pushToTable()                                  #
//                                                #
// puts values from a stat array into html table  #
//                                                #
//------------------------------------------------#

function pushToTable(array, type){

	stat_names = ["max", "min", "mean", "std"];

	for(i = 0; i < 4; i++){
	document.getElementById(stat_names[i] + "_" + type).innerHTML = array[i];
	}
}


//------------------------------------------------#
// updateTable()                                  #
//                                                #
// puts values from a stat array into html table  #
//                                                #
//------------------------------------------------#

function updateTable(stat_file){

$.get('data/page-data/' + stat_file, function(data) {

		    stats = $.csv.toArrays(data);

		    temp_stats_long = getStats(stats, TEMPERATURE_STAT);
		    pressure_stats_long = getStats(stats, PRESSURE_STAT);
		    humidity_stats_long = getStats(stats, HUMIDITY_STAT);

		    pushToTable(temp_stats_long, "temperature");
		    pushToTable(pressure_stats_long, "pressure");
		    pushToTable(humidity_stats_long, "humidity");
		    
});

};

//------------------------------------------------#
//                                                #
// This function handles clicking the buttons     #
// which update the table and graphs on the page  #
//                                                #
//------------------------------------------------#

$("li").click(function() {
	    if(this.id.indexOf("sensor") != -1){
		   var button = this.id;
		   var properties = button.split("-");
		   sensor_number = String(properties[1]);
		   room_name = String(properties[2]);
		   short_or_long = String(properties[3]);

		// Tell server to process required data with python script
		$.ajax({
			  type: "POST",
			  url: "/python/process_data.py",
			  data: { room: room_name, sensor: sensor_number, longshort: short_or_long }
		}).done(function( o ) {
			   });
		
		updateTable(room_name + "-sensor-" + sensor_number + "-" + short_or_long + "-stats.csv")

		updateGraphTitle(room_name, Number(sensor_number), short_or_long);
		
		if(short_or_long == "short"){
			updateGraphShort("data/page-data/" + room_name + "-sensor-" + sensor_number + "-short.csv");
		}	
		else if(short_or_long == "long"){
			updateGraphLong("data/page-data/" + room_name + "-sensor-" + sensor_number + "-long.csv");
		}


		}	   


});


//------------------------------------------------#
// updateGraphTitle()                             #
//                                                #
// edits the highcharts options variable to       #
// update graph title text                        #
//------------------------------------------------#

function updateGraphTitle(room_name, sensor_number, short_or_long){

	if(short_or_long == "short"){
		if(room_name == "master")
			options_short.title.text = sensor_names_master[sensor_number];

		else if(room_name == "mol")
			options_short.title.text = sensor_names_mol[sensor_number];

	}
	else if(short_or_long == "long"){

	if(room_name == "master")
			options_long.title.text = sensor_names_master[sensor_number];

	else if(room_name == "mol")
			options_long.title.text = sensor_names_mol[sensor_number];

	}

}









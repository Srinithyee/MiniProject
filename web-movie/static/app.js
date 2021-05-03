var date = null;
var movieID = null;
var type = null;
var seatNo = null;
var seatClass = null;
var showID = null;


function selectMovie(movID, mtype){
	movieID = movID;
	type = mtype;
	$.ajax({
		type: 'POST',
		url: '/getTimings',
		data: {
			'date' : date,
			'movieID': movieID,
			'type' : type
		},
		success: function(response){
			$('#movies-on-date button').prop('disabled', true);
			$('#timings-for-movie').html(response);
		}
	});
}

function selectTiming(mtime){
	movieTime = mtime;
	$.ajax({
		type: 'POST',
		url: '/getShowID',
		data: {
			'date' : date,
			'movieID': movieID,
			'type' : type,
			'time' : movieTime
		},
		success: function(response){
			$('#timings-for-movie button').prop('disabled', true);
			showID = response['showID'];
			getSeats();
		}
	});
}

function getSeats(){
	$.ajax({
		type: 'POST',
		url: '/ticket',
		data: {'showID' : showID},
		success: function(response){
			$('#available-seats').html(response);
		}
	});
}


function createShow(){
	console.log("HI");
	$('#options button').prop('disabled', true);
	$('#manager-dynamic-1').html('<input id="datepicker-manager-3" placeholder="Pick a date"><input id="timepicker-manager-1" placeholder="Pick a time"><button onclick="getValidMovies()">Submit</button>');
	$('#datepicker-manager-3').pickadate({
				formatSubmit: 'yyyy/mm/dd',
 				hiddenName: true,
 				min: new Date(),
 				onSet: function( event ) {
 					if ( event.select ) {
 						showDate = this.get('select', 'yyyy/mm/dd' );
 					}
 				}
	});
	$('#timepicker-manager-1').pickatime({
				formatSubmit: 'HHi',
 				hiddenName: true,
 				interval: 15,
 				min: new Date(2000,1,1,8),
  				max: new Date(2000,1,1,22),
 				onSet: function( event ) {
 					if ( event.select ) {
 						showTime = parseInt(this.get('select', 'HHi' ), 10);
 					}
 				}
	});
}

function selectSeat(no, sclass){
	seatNo = no;
	seatClass = sclass;
	$.ajax({
		type: 'POST',
		url: '/getPrice',
		data: {
			'showID' : showID,
			'seatClass' : seatClass
			},
		success: function(response){
			$('#price-and-confirm').html(response);
		}
	});
}

function confirmBooking(){
	$.ajax({
		type: 'POST',
		url: '/insertBooking',
		data: {
			'showID' : showID,
			'seatNo' : seatNo,
			'seatClass' : seatClass
			},
		success: function(response){
			$('#available-seats button').prop('disabled', true);
			$('#price-and-confirm').html(response);
		}
	});
}
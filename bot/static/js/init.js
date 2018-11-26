var slider = $('#chat-pane').slideReveal({
  trigger: $('.trigger'),
  width: '90%',
  push: false,
  position: 'right',
  overlay: true,
  overlayColor: 'rgba(0,0,0,0.5)',
});

// Materialize JS

(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('.parallax').parallax();

  }); // end of document ready
})(jQuery); // end of jQuery name space

// Messaging Interactions for Chat Pane

$('.message-submit').click(function(event){
    event.preventDefault();
    insertMessage();
});

var $messages = $('.messages-content'),
  d, h, m,
  i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
  initialMessage();
});

$messages.mCustomScrollbar();

function initialMessage() {

  var html = '<div class="message new"><figure class="avatar"><img src="../static/images/chathead.png" /></figure>Hello! I am Upaj! How can I help you?</div>'
  $(html).appendTo($('.mCSB_container')).addClass('new');
}

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  query = $('textarea[name="message-input"]').val();
  csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
  fakeMessage();

  $.ajax({
    type: 'POST',
    url: '/response',
    data: {
      'query' : query,
      'csrfmiddlewaretoken': csrfmiddlewaretoken,
    },
    success: function(data){

      for (i=0; i<data['bubbles']; i++) {
        $('.message.loading').remove();
        $(data['text'][i]).appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
        i++;
      }
    },
    error: function(data, err){

    }
  });

  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  fakeMessage();
}

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

function fakeMessage() {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="../static/images/chathead.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();
}

// Owl Carousel

$(document).ready(function(){
  $(".owl-carousel").owlCarousel({
    stagePadding : 30,
    responsive : {
      10 : {
          items : 1,
      },
      768 : {
          items : 3,
      }
    },
    dots : true,
  });
});

// Weather API

var latitude, longitude;
navigator.geolocation.getCurrentPosition(function(position) {

  latitude = position.coords.latitude;
  longitude = position.coords.longitude;

    const Http = new XMLHttpRequest();
    const url='https://dev.virtualearth.net/REST/v1/Locations/'+position.coords.latitude + ',' + position.coords.longitude + '?key=AoTJ0es6QeGwvVw9Fb4LCrAhUtdt6ZeDN-eWENSWR8ddNEWPWQ0pTvsA1HZ1ktJj';
    Http.open("GET", url);
    Http.send();
    result = "";
    flag = 0;

    Http.onreadystatechange=function(){
      result = Http.responseText;
      var obj = JSON.parse(result);
      var address = obj.resourceSets["0"]["resources"]["0"]["address"]["formattedAddress"];
      city_name = obj.resourceSets["0"]["resources"]["0"]["address"]["adminDistrict2"]
      document.getElementById("loc").innerHTML = address;
      const http = new XMLHttpRequest();
      var lat = position.coords.latitude;
      var lon = position.coords.longitude;
      const url_weather = 'https://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&appid=c4ebee5432d574b968a2332bfa6ab6f4&units=metric';
      http.open("POST", url_weather);
      http.send();
      res = "";
      http.onreadystatechange = function(){
        res = http.responseText;
        var ob = JSON.parse(res);
        var temp = ob["main"]["temp"];
        var humidity = ob["main"]["humidity"];
        // var condition = ob["weather"]["0"]["description"];
        document.getElementById("temp").innerHTML = temp;
        document.getElementById("humidity").innerHTML = humidity;
        // if(flag == 0){
        //   flag = 1;
        //   var img = document.createElement("img")
        //   img.src = "../../static/images/haze.png";
        //   if(condition.includes("cloud")){
        //     img.src = "../../static/images/haze.png";
        //   }
        //   else{
        //     img.src = "../../static/images/sunny.png";
        //   }
        //   img.style.height = "5vw"
        //   var src = document.getElementById("image_weather");
        //   src.appendChild(img);
        // }
      }

      result = "";
      const protocol = new XMLHttpRequest();
      const url_forecast = 'https://api.darksky.net/forecast/2a99ce9cb51213c9703f94fc6d4f6b5f/' + lat +',' + lon;
      protocol.open("GET", url_forecast);
      protocol.send();
      protocol.onreadystatechange = function(){
        result = protocol.responseText;
        var object = JSON.parse(result)
        console.log(object)
        var i;
        for(i = 0; i < 7; i++){
          var data_in = object['daily']['data'][i.toString()];
          var data_insert = 'day' + (i).toString();
          var data2 = data_insert + '_data';
          var data3 = data_insert + '_data2';
          var data_rise = "rise" + (i).toString();
          var data_set = "set" + (i).toString();

          var temperatureHigh = data_in["temperatureHigh"];
          var temperatureLow = data_in["temperatureLow"];

          temperatureHigh = (Math.round((((temperatureHigh-32)*5)/9)*100))/100;
          temperatureLow = Math.round(((temperatureLow-32)*500)/9)/100;

          var sunriseTime = data_in['sunriseTime'];
          var sunseTime = data_in['sunseTime'];

          document.getElementById(data_insert).innerHTML = data_in[""];
          document.getElementById(data2).innerHTML = temperatureHigh + "<sup>o</sup>C";
          document.getElementById(data3).innerHTML = temperatureLow + "<sup>o</sup>C";
          document.getElementById(data_rise).innerHTML = sunriseTime;
          document.getElementById(data_set).innerHTML = sunseTime;
        }
      }
    }
  });

var latlngo = {lat : "", long : ""};
  navigator.geolocation.getCurrentPosition(function(position) {
    // latlngo.lat = position.coords.latitude.toString();
    // latlngo = position.coords.latitude + ' ' + position.coords.longitude;

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
      document.getElementById("loc").innerHTML = address;
      // console.log(address)
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
        var condition = ob["weather"]["0"]["description"];
        // console.log(condition);
        document.getElementById("temp").innerHTML = temp;
        document.getElementById("humidity").innerHTML = humidity;
        // console.log(ob);
        if(flag == 0){
          flag = 1;
          var img = document.createElement("img")
          if(condition.includes("cloud")){
            img.src = "../../static/images/haze.png";
          }
          else{
            img.src = "../../static/images/sunny.png";
          }
          img.style.height = "5vw"
          var src = document.getElementById("image_weather");
          src.appendChild(img);
        }
      }
      result = "";
      const protocol = new XMLHttpRequest();
      const url_forecast = 'http://api.weatherunlocked.com/api/forecast/23.17,80.02?app_id=c8fc446a&app_key=b774914ba609ae0aacbb827fc88d64a4';
      protocol.open("GET", url_forecast);
      protocol.send();
      protocol.onreadystatechange = function(){
        result = protocol.responseText;
        var object = JSON.parse(result)
        // console.log(object["Days"]);
        var i;
        for(i = 0; i < 5; i++){
          var data_in = object["Days"][i.toString()];
          var data_insert = 'day' + (i+1).toString();
          var data2 = data_insert + '_data';
          var data3 = data_insert + '_data2';
          var data_rise = "rise" + (i+1).toString();
          var data_set = "set" + (i+1).toString();
          console.log(data_in);
          document.getElementById(data_insert).innerHTML = data_in["date"];
          document.getElementById(data2).innerHTML = data_in["temp_max_c"] + "C";
          document.getElementById(data3).innerHTML = data_in["temp_min_c"] + "C";
          document.getElementById(data_rise).innerHTML = data_in["sunrise_time"];
          document.getElementById(data_set).innerHTML = data_in["sunset_time"];
          // console.log(data_in);
        }
        // parser = new DOMParser();
        // xmlDoc = parser.parseFromString(result);
        // document.getElementById("demo").innerHTML = xmlDoc.getElementsByTagName("title")[0].childNodes[0].nodeValue;
      }
    }
  });
  var rain = {{ rain|safe }};
  var rain_year = {{ rain_year|safe }};
  var st = "{{ rain_state }}";
  var title = "Rainfall in " + st + " over years (mm)";

  var crop = {{ crop|safe }}
  var prod = {{ prod|safe }}
  var st = "{{ state }}";
  var year = "{{ year }}"
  var title2 = "Top 5 crops in " + st + " in " + year + " (1000 tonnes)";

  var total_state = {{ total_states| safe}}
  console.log(total_state)
  console.log(rain);
  console.log(rain_year);
  console.log(crop)
  console.log(prod)
  console.log(st);


  window.onload = function () {
    var chart = new CanvasJS.Chart("chartContainer2", {
        title:{
          text: title
        },
        data: [
        {
          // Change type to "doughnut", "line", "splineArea", etc.
          type: "splineArea",
          dataPoints: [
            { label: rain_year[0], y: rain[0]  },
            { label: rain_year[1], y: rain[1]  },
            { label: rain_year[2], y: rain[2]  },
            { label: rain_year[3], y: rain[3]  },
            { label: rain_year[4], y: rain[4]  },
            { label: rain_year[5], y: rain[5]  },
            { label: rain_year[6], y: rain[6]  },
            { label: rain_year[7], y: rain[7]  },
            { label: rain_year[8], y: rain[8]  },
            { label: rain_year[9], y: rain[9]  },
            { label: rain_year[10], y: rain[10]  },
            { label: rain_year[11], y: rain[11]  },
            { label: rain_year[12], y: rain[12]  },
            { label: rain_year[13], y: rain[13]  },
            { label: rain_year[14], y: rain[14]  }
          ]
        }
      ]
    });
    chart.render();

    var chart2 = new CanvasJS.Chart("chartContainer", {
      title:{
        text: title2
      },
      data: [
      {
        // Change type to "doughnut", "line", "splineArea", etc.
        type: "splineArea",
        dataPoints: [
          { label: crop[0], y: prod[0]/1000  },
          { label: crop[1], y: prod[1]/1000  },
          { label: crop[2], y: prod[2]/1000  },
          { label: crop[3], y: prod[3]/1000  },
          { label: crop[4], y: prod[4]/1000  }
        ]
      }
    ]
  });
  chart2.render();
}

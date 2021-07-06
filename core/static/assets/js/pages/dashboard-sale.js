function plot_response_data(json){
  ajaxPostRequest(MyGlobal.all_questions, {}, function(q_data){
    chart1(json, q_data)
  })
  chart2(json)
  chart3(json)
}

function chart1(json, q_data){
    firstN = 5 // this is saying to only plot 5 surveys on the overview dashboard with the highest ids
    ids = []
    for (var response in json){
      ids.push(json[response]['question_id'])
    }

    ids = [...new Set(ids)];

    ids.sort()
    if (firstN < ids.length){
      ids = ids.slice(ids.length-firstN, ids.length)
    }

    data = {}
    for(i=0; i < ids.length; i++){ // loop through the question ids
      list = []
      for(j=0; j < json.length; j++){ // loop through the questions
        if(json[j]['question_id'] == ids[i]){ // if this question has the current id
          list.push([json[j]['user_id'], json[j]['response_feeling'], json[j]['response_summary'], json[j]['response_time']])
        }
      }
      data[ids[i]] = list // add this question id's data to the dictionary
    }

    categories = []
    for (var q_id in ids){
      categories.push(q_data[ids[q_id]]['name'])
    }

    series1 = []
    series2 = []
    series3 = []
    series4 = []
    series5 = []
    for(i=0; i < categories.length; i++){ // loop through each of the questoins
      question = data[ids[i]]
      sum1 = 0
      sum2 = 0
      sum3 = 0
      sum4 = 0
      sum5 = 0
      for(j=0; j < question.length; j++){ // loop through each individual response
        response = question[j][1]
        if(response == 1){sum1 += 1}
        else if(response == 2){sum2 += 1}
        else if(response == 3){sum3 += 1}
        else if(response == 4){sum4 += 1}
        else if(response == 5){sum5 += 1}
      }
      series1.push(sum1)
      series2.push(sum2)
      series3.push(sum3)
      series4.push(sum4)
      series5.push(sum5)
    }

    series = [{name: "😃", data: series5}, {name: "🙂", data: series4}, {name: "😐", data: series3},{name: "🙁", data: series2}, {name: "😭", data: series1}]

    $(function() {
        var options = {
            chart: {
                height: 350,
                type: 'bar',
                stacked: true,
                toolbar: {
                    show: true
                },
                zoom: {
                    enabled: true
                },
                events: {
                  dataPointSelection: function(event, chartContext, config){
                    return null
                    //console.log(event)
                    //console.log(chartContext)
                    //console.log(config)
                    //console.log(config.w.config.xaxis['categories'][config.dataPointIndex])
                  }
                }
            },
            colors: ["#d240ff", "#4099ff", "#0e9e4a", "#FFB64D", "#FF5370"],
            responsive: [{
                breakpoint: 480,
                options: {
                    legend: {
                        position: 'bottom',
                        offsetX: -10,
                        offsetY: 0
                    }
                }
            }],
            plotOptions: {
                bar: {
                    horizontal: false,
                },
            },
            series: series,
            xaxis: {
                type: 'categories',
                categories: categories,
            },
            legend: {
                position: 'right',
                offsetY: 40,
                fontSize: '14px',
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'light',
                    type: "horizontal",
                    shadeIntensity: 0.25,
                    inverseColors: true,
                    opacityFrom: 0.8,
                    opacityTo: 1,
                    stops: [0, 100]
                },
            },
        }
        var chart = new ApexCharts(
            document.querySelector("#bar-chart-2"),
            options
        );
        chart.render();
    });
}

function chart2(json){
  responses = []
  for (var response in json){ // loop through each of the responses
    if(response >= 1){
      this_date = new Date(json[response]['response_time'])
      last_date = new Date(json[response-1]['response_time'])
      // if this response ocurred the same days as the prior response, then add 1 to the last vlaue of responses
      if(this_date.toDateString() == last_date.toDateString()){
        responses[responses.length-1] += 1
      }else{
        responses.push(1)
      }
    }else{
      responses.push(1)
    }
  }

  // [ unique-visitor-chart ] start
  $(function() {
      var options = {
          chart: {
              type: 'bar',
              height: 220,
              zoom: {
                  enabled: false
              },
              toolbar: {
                  show: false,
              },
          },
          dataLabels: {
              enabled: false,
          },
          colors: ["#fff"],
          plotOptions: {
              bar: {
                  color: '#fff',
                  columnWidth: '80%',
              }
          },
          fill: {
              type: 'gradient',
              gradient: {
                  shade: 'light',
                  type: "vertical",
                  shadeIntensity: 0.25,
                  gradientToColors: ["#fff", ],
                  inverseColors: true,
                  opacityFrom: 0.99,
                  opacityTo: 0.65,
                  stops: [0, 100]
              },
          },
          series: [{
              data: responses //[25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54, 25, 66, 41, 89, 63, 54, 25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54, 25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 25, 44, 12, 36, 9, 54]
          }],
          xaxis: {
              crosshairs: {
                  width: 1
              },
              labels: {
                  show: true,
                  style: {
                      colors: '#fff',
                  },
              },
          },
          yaxis: {
              labels: {
                  style: {
                      color: '#fff',
                  },
              },
          },
          grid: {
              borderColor: '#ffffff3b',
          },
          tooltip: {
              fixed: {
                  enabled: false
              },
              x: {
                  show: false
              },
              y: {
                  title: {
                      formatter: function(seriesName) {
                          return 'Click '
                      }
                  }
              },
              marker: {
                  show: false
              }
          }
      }
      var chart = new ApexCharts(document.querySelector("#unique-visitor-chart"), options);
      chart.render();
  });
  // [ unique-visitor-chart ] end
}

function chart3(json){
  $(function() {
      const speed = 1500
      var data = []
      var firstN = 10 // how many datapoints to display initially (if not 10 the beginning animation will be weird)
      //var basetime = new Date(json[0]['response_time']) // basetime is the first day in the graph
      //basetime = new Date(basetime.toDateString()).getTime()
      const today = new Date()
      var basetime = new Date(today) // set basetime to be 30 days ago
      basetime.setDate(basetime.getDate() - 30)
      basetime = basetime.getTime()

      var i = 0;
      while (i < firstN) { // loop through the first 5 dates (whether they have data or nah)
        // if there exists data for that date
        this_date = new Date(basetime).toDateString()
        sum_feeling = 0 // the sum of the feelings for responses that lie on that day
        count = 0 // the # of responses that lie on that day
        for (var response in json){
          check_date = new Date(json[response]['response_time']).toDateString()
          if(check_date == this_date){ // if the date of the response is the data you are on in the graph
            sum_feeling += json[response]['response_feeling']
            count += 1
          }
        }
        if (count >= 1){// if there is at least one response for this day
          data.push({x: basetime, y: sum_feeling/count})
        }else{
          data.push({x: basetime, y: 0})
        }
        basetime += 86400000
        i++;
      }

      const initial_data = JSON.parse(JSON.stringify(data)) // create a shallow copy of the original data
      var lastDate = data[data.length-1]['x']

      function getNewSeries(baseval) {
          var newDate = baseval + 86400000;
          if (new Date(newDate).toDateString() == new Date().toDateString()){ // If we have arrived back to the current day in graph
            data = data.splice(0, 10); // remember that splice works inplace and also has just some unexpected behavior with variable assignment
            lastDate = initial_data[initial_data.length-1]['x']
          }
          else{
            lastDate = newDate

            sum_feeling = 0
            count = 0
            for (var response in json){
              check_date = new Date(json[response]['response_time']).toDateString()
              if(check_date == new Date(newDate).toDateString()){ // if the date of the response is the data you are on in the graph
                sum_feeling += json[response]['response_feeling']
                count += 1
              }
            }
            if (count >= 1){// if there is at least one response for this day
              data.push({x: newDate, y: sum_feeling/count})
            }else{
              data.push({x: newDate, y: 0})
            }
          }
      }


      var options = {
          chart: {
              id: "my-chart",
              height: 300,
              type: 'area',
              animations: {
                  enabled: true,
                  easing: 'linear',
                  dynamicAnimation: {
                      speed: speed
                  }
              },
              toolbar: {
                  show: false
              },
              zoom: {
                  enabled: false
              }
          },
          dataLabels: {
              enabled: false
          },
          stroke: {
              curve: 'smooth'
          },
          series: [{
              name: 'Average Sentiment :',
              data: data
          }],
          colors: ["#FF5370"],
          fill: {
              type: 'gradient',
              gradient: {
                  shadeIntensity: 1,
                  type: 'horizontal',
                  opacityFrom: 0.8,
                  opacityTo: 0,
                  stops: [0, 100]
              }
          },
          markers: {
              size: 0
          },
          xaxis: {
              type: 'datetime',
              range: 777600000,
          },
          yaxis: {
              max: 5.5
          },
          legend: {
              show: false
          },
      }
      var chart = new ApexCharts(
          document.querySelector("#site-visitor-chart"),
          options
      );
      chart.render();
      window.setInterval(function() {
          getNewSeries(lastDate) // add a new value to the data list
          chart.updateSeries([{
              data: data
          }], true)
      }, speed)

  });
}

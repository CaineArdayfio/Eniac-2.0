emoji_key = {
    1: "😭",
    2: "🙁",
    3: "😐",
    4: "🙂",
    5: "😃"
}

function plot_data(text){
  am4core.options.queue = true;
  color1 = am4core.color("#3358f4");
  color2 = am4core.color("#1d8cf8");

  // Themes begin
  am4core.useTheme(am4themes_animated);

  // Create chart instance
  var chart = am4core.create("dashboardchart", am4charts.XYChart);
  chart.data = text; //[{"Date": "2012-07-27", "Day": 3, "Feeling": 2, "Moving Average": 4.3, "Summary": "They are gay", "Summary Length": 3}];
  // zoom in if they have at least 40 days of data already
  if(text.length >= 40){
    dateIndices = [text.length-40, text.length-1];
    dateStart = text[dateIndices[0]]["Date"];
    dateEnd = text[dateIndices[1]]["Date"];
    chart.events.on("ready", function () {
      dateAxis.zoomToDates(
        new Date(dateStart),
        new Date(dateEnd)
      );
    });
  }


  // Title
  let title = chart.titles.create();

  // Set input format for the dates
  chart.dateFormatter.inputDateFormat = "yyyy-MM-dd";

  // Create axes
  var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
  dateAxis.renderer.labels.template.fill = am4core.color("#9a9a9a");
  var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
  valueAxis.min = 0.5;
  valueAxis.max = 5.5;

  // Custom axis labels
  valueAxis.renderer.grid.template.disabled = true;
  valueAxis.renderer.labels.template.disabled = true;
  valueAxis.fontSize = 40;
  function createGrid(value) {
    var range = valueAxis.axisRanges.create();
    range.value = value;
    range.label.text = emoji_key[value];
  }

  createGrid(1);
  createGrid(2);
  createGrid(3);
  createGrid(4);
  createGrid(5);

  // Create series
  var series1 = chart.series.push(new am4charts.LineSeries());
  series1.dataFields.valueY = "Feeling";
  series1.dataFields.dateX = "Date";
  series1.dataFields.value = "Summary Length"// What values determine the bullet (the circle thing on graph) radii... these values will be interpolated between series1.heatrule.min and max. see https://www.amcharts.com/docs/v4/concepts/series/#Heat_maps
  series1.minBulletDistance = 1;
  series1.strokeOpacity = 0;
  series1.defaultState.transitionDuration = 1500;
  //series1.slices.template.cursorOverStyle = am4core.MouseCursorStyle.pointer;

  var series2 = chart.series.push(new am4charts.LineSeries());
  series2.dataFields.valueY = "Moving Average";
  series2.dataFields.dateX = "Date";
  series2.strokeWidth = 4;
  series2.defaultState.transitionDuration = 2500;
  series2.stroke = color2;
  series2.fillOpacity = 0.2;

  // Bullets
  var bullet = series1.bullets.push(new am4charts.CircleBullet());
  bullet.circle.radius = 6; // if the bullet doesn't have a Summary length attribute aka we don't have a summary for it
  bullet.stroke = color1;
  bullet.fill = color1;
  bullet.cursorOverStyle = am4core.MouseCursorStyle.pointer;

  series1.heatRules.push({
    target: bullet.circle,
    min: 12, // the minimum allowable bullet radius for data points with a summary... the length of the summary will interpolate between min and max to determine radius
    max: 35, // the maximum allowable bullet radius
    property: "radius"
  });

  // Make bullets grow on hover
  var bullethover = bullet.states.create("hover");
  bullethover.properties.scale = 1.5;

  // Drop-shaped tooltips
  series1.tooltipText = "{Feeling}"
  series1.tooltip.background.cornerRadius = 20;
  series1.tooltip.background.strokeOpacity = 0;
  series1.tooltip.pointerOrientation = "vertical";
  series1.tooltip.label.minWidth = 40;
  series1.tooltip.label.minHeight = 40;
  series1.tooltip.label.textAlign = "middle";
  series1.tooltip.label.textValign = "middle";
  series1.tooltip.label.fontSize = 35;
  series1.tooltip.getFillFromObject = false;
  series1.tooltip.background.fill = color2;

  // disable grid lines
  valueAxis.renderer.grid.template.strokeWidth = 0;
  dateAxis.renderer.grid.template.strokeWidth = 0;

  // Chart cursor
  chart.cursor = new am4charts.XYCursor();
  chart.cursor.behavior = "panX";
  chart.cursor.snapToSeries = series1;

  // Create a horizontal scrollbar with preview and place it underneath the date axis
  chart.scrollbarX = new am4charts.XYChartScrollbar();
  chart.scrollbarX.series.push(series2);
  chart.scrollbarX.thumb.minWidth = 50;
  chart.scrollbarX.parent = chart.bottomAxesContainer;

  function customizeGrip(grip) {

    grip.icon.disabled = true;
    grip.background.disabled = true;

    var img = grip.createChild(am4core.Rectangle);
    img.width = 15;
    img.height = 15;
    img.fill = am4core.color("#999");
    img.rotation = 45;
    img.align = "center";
    img.valign = "middle";

    // Add vertical bar
    var line = grip.createChild(am4core.Rectangle);
    line.height = 60;
    line.width = 3;
    line.fill = am4core.color("#999");
    line.align = "center";
    line.valign = "middle";

  }

  customizeGrip(chart.scrollbarX.startGrip);
  customizeGrip(chart.scrollbarX.endGrip);

  chart.scrollbarX.background.fill = color1;
  chart.scrollbarX.background.fillOpacity = 0;

  chart.scrollbarX.unselectedOverlay.fill = am4core.color("#fff");
  chart.scrollbarX.unselectedOverlay.fillOpacity = 0.4;

  var scrollAxis = chart.scrollbarX.scrollbarChart.xAxes.getIndex(0);
  scrollAxis.renderer.labels.template.disabled = true;
  scrollAxis.renderer.grid.template.disabled = true;

  // Legend
  chart.legend = new am4charts.Legend();
  series1.legendSettings.labelText = "[bold {color}]Individual Day[/]";
  series2.legendSettings.labelText = "[bold {color}]7-Day Moving Average[/]";

  json = ajaxPostRequest(MyGlobal.survey_details, {id: MyGlobal.q_id}, null, async=false)

  summaries = json.responseJSON.responses.response_summary // all of this survey's summaries ["a good day", "not fun", "just chillin", ""]
  feelings = json.responseJSON.responses.response_feeling // [4, 2, 1, 1]
  dates = json.responseJSON.responses.response_time // [2021-07-05, 2021-07-06, 2021-07-05, 2021-07-06]
  users = json.responseJSON.responses.user_id // I get user data but I don't do anything with it to keep it anonymous ['User 1', 'User '1', 'User 2', 'User 2']


  bullet.events.on("hit", function(event){
    date = event.target.dataItem.dataContext["Date"]; // this is the date of the object they clicked
    summary = event.target.dataItem.dataContext["Summary"]; // these are the summaries separated by linebreaks of the date of the datapoint they clicked (not useful because I need to correlate a summary with a user, not just all aggregate summaries)
    feeling = event.target.dataItem.dataContext["Feeling"]; // same deal as ^^

    $.notifyClose();

    if (summary == undefined){
      $('#response-table').html("")
    }
    else{
      //https://robohash.org/${img}.png?bgset=bg1
      function gen_list(emoji, date, summary, number, img){
        return `<li class="active-feed">
          <div class="feed-user-img">
            <img src="https://robohash.org/${img}.png?bgset=bg1" class="img-radius " alt="User-Profile-Image">
          </div>
          <h6>
            <span class="badge badge-danger">Response</span>
            User #${number} responded: <small class="text-muted">${date}</small>
          </h6>
          <p class="m-b-15 m-t-15">${emoji} ${summary}</p>
        </li>`
      }
      list_element = ''
      count = 0
      for (i = 0; i < json.responseJSON.responses.length; i++){
        if (dates[i].substring(0, 10) == date){ // get today's user responses
          clicked_date = new Date(dates[i])
          year_month_day = dates[i].substring(0, 10) // or use getUTCDate/Month
          hour = clicked_date.getUTCHours()
          minute = clicked_date.getMinutes()
          list_element += gen_list(emoji_key[feelings[i]], `${year_month_day} @${hour}:${minute}`, summaries[i], count+1, parseInt(i)*5)
          count += 1
        }
      }
      $('#response-table').html(list_element)
    }
  })




}

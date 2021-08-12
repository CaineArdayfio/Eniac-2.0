
$(function() {
  // define tour
  /*
  var tour = new Tour({
    debug: true,
    basePath: '/',
    framework: 'bootstrap4',   // or "bootstrap4"
    steps: [{
      path: "home/",//"/home/",//MyGlobal.home,
      element: "#overview",
      title: "Overview Tab",
      content: "The overview tab contains a broad overview summarizing all the surveys you've sent out"
    },{
      path: "surveys/",//MyGlobal.surveys,
      element: "#surveys",
      title: "Surveys Tab",
      content: "The survey tab shows all the surveys you've created"
    },{
      path: "surveys/",//MyGlobal.surveys,
      element: "#survey-create-button",
      reflex: true,
      reflexOnly: true,
      title: "Surveys Tab",
      content: "Click this button to create your first survey",
      onNext: function(tour){
                //tour.end();
                setTimeout(function(){
                    //tour.restart();
                    tour.goTo(4); //substitute your step index here
                }, 1500); //change this to as little as your load time allows
            }
    },{
      element:  function(){
          console.log("looking for element")
          console.log($(document))
          console.log($("#recipients"))
          return $(document).find("#recipients");
      },
      title: "Recipients",
      content: "Create your first user group to send this survey to"
    },{
      path: "users/",//MyGlobal.surveys,
      element: "#users",
      title: "Users Tab",
      content: "The users tab shows all the users in the system."
    }]
  });
  */

  var tour = new Tour({
    debug: true,
    basePath: '/',
    framework: 'bootstrap4',   // or "bootstrap4"
    steps: [{
      path: "home/",//"/home/",//MyGlobal.home,
      element: "#overview",
      title: "Overview Tab",
      content: "The overview tab contains a broad overview summarizing all the surveys you've sent out"
    },{
      path: "surveys/",//MyGlobal.surveys,
      element: "#surveys",
      title: "Surveys Tab",
      content: "The survey tab shows all the surveys you've created"
    },{
      path: "surveys/",//MyGlobal.surveys,
      element: "#survey-create-button",
      reflex: true,
      reflexOnly: true,
      title: "Surveys Tab",
      content: "Click this button to create your first survey",
    }]
  });

  tour.start();

  // start tour
  $('#start-tour').click(function() {
    tour.restart();
  });
});

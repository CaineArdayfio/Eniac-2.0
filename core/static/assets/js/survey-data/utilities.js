function ajaxPostRequest(url, data, onSuccess, async=true){
  $.ajaxSetup({
      headers: { "X-CSRFToken": Cookies.get('csrftoken')}
  });
  if (async==true){
    $.ajax({
      url : url,
      type : "POST",
      data : data,
      context: this,
      success : onSuccess,
      error : function(xhr,errmsg,err) {
         console.log(errmsg)
         console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    })
  }else{
    return $.ajax({
          url : url,
          type : "POST",
          data : data,
          async: false,
          error : function(xhr,errmsg,err) {
             console.log(errmsg)
             console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    })
  }
}

function notify(title, message, from, align, icon, type, animIn, animOut, delay=3000, allow_dismiss=true) {
  return $.notify({
      icon: icon,
      title: ` ${title} `,
      message: message,
      url: ''
  }, {
      element: 'body',
      type: type,
      allow_dismiss: allow_dismiss,
      placement: {
          from: from,
          align: align
      },
      offset: {
          x: 30,
          y: 30
      },
      spacing: 10,
      z_index: 999999,
      delay: delay,
      timer: 1000,
      url_target: '_blank',
      mouse_over: false,
      animate: {
          enter: animIn,
          exit: animOut
      },
      icon_type: 'class',
  template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
        '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">&times</button>' +
        '<h6 class="text-c-blue"><span data-notify="icon"></span> ' +
        '<span data-notify="title">{1}</span></h6> ' +
        '<span data-notify="message">{2}</span>' +
        '<div class="progress" data-notify="progressbar">' +
          '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
        '</div>' +
        '<a href="{3}" target="{4}" data-notify="url"></a>' +
      '</div>'
  });
};

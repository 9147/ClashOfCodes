function updateLandingPage() {
    date ={
        'is_set': document.getElementById('is_set').checked
    }
    console.log(date,document.getElementById('is_set'));
    setRequestHeader();
    $.ajax({
        type: 'POST',
        data: date,
        url: '../update_landing_page/',
        success: function(response){
            console.log(response);
        },
        error: function(error){
            console.log(error);
        }
    });
}


// Function to GET csrftoken from Cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  
  var csrftoken = getCookie('csrftoken');
  
  
  
  
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  
  // Function to set Request Header with `CSRFTOKEN`
  function setRequestHeader(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
  }
  

  function OpenHome(){
    ele = document.getElementById('is_set');
    if (ele.checked){
        // home cant be loaded until this site is set as landing page
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'This page must be removed as landing page to open home page',
          })
    }
    else{
    window.location.href = '../';
    }
  }
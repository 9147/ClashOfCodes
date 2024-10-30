function SubmitData() {
    var role = document.getElementById("role").value;
    var college = document.getElementById("college").value;
    if( role.trim() == "" || college.trim() == ""){
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Please fill all the fields!',
          })
        return;
    }
    setRequestHeader();
    var data = {
        'role': role,
        'college': college
    };
    console.log(data);
    $.ajax({
        type: "POST",
        url: "/generateReferral/",
        data: data,
        success: function (data) {
                Swal.fire({
                    title: 'Referral Code generated successfully!',
                    html: `
                        <p>Use this code to get ₹100 off on all 6 teams registration fee.</p>
                        <h3 class="sub-menu"><span>Referral code: <input type="text" id="referral_code" onclick="copyToClipboard()" class="referral_code"  value="${data['referral_code']}" readonly></span></h3>
                    `,
                    showCloseButton: true,
                    customClass: {
                        popup: 'swal2-fullscreen'
                    },
                    // width: '100%',
                    heightAuto: false,
                    allowOutsideClick: false,
                    allowEscapeKey: true,
                    willClose: () => {
                        // Redirect to a different page upon closing the alert
                        window.location.href = '../';
                    }
                });
                
        
        },
        error: function (data) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong! Please try again.',
            });
        }
    });
}

function copyToClipboard() {
    const input = document.getElementById("referral_code");

    input.select();
    input.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(input.value).then(() => {
        // Show toast message
        Toastify({
            text: "Text copied!",
            duration: 5000, // 5 seconds
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "center", // `left`, `center`, or `right`
            color: "black",
            backgroundColor: "linear-gradient(to right, #dfa739, hsla(42, 99%, 46%, 0.75))",
        }).showToast();
    }).catch(err => {
        console.error("Failed to copy text: ", err);
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
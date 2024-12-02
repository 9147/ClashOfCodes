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

function changeSection(callingObject,section){
    ele = document.getElementsByClassName('menu-item');
    for (i=0;i<ele.length;i++){
        ele[i].classList.remove('active-menu-item');
    }
    callingObject.classList.add('active-menu-item');

    const rows = document.querySelectorAll('.table-section tr');

    // Loop through the NodeList and do something with each <tr>

    ele = document.getElementsByClassName('table-section');
    for (i=0;i<ele.length;i++){
        ele[i].style.display = 'none';
    }
    console.log(section,document.getElementById(section));
    document.getElementById(section).style.display = 'block';

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

tippy('.info-icon', {
    placement: 'top', // Tooltip position
    animation: 'shift-away', // Smooth animation
    theme: 'light', // Custom theme
    duration: [200, 150], // Duration for show/hide
});


function makePayment() {
    Swal.fire({
        title: 'Make Payment',
        text: 'Please make payment to the following account',
        imageUrl: '/static/images/payment_qr.jpg',
        imageWidth: 375,
        imageHeight: 470,
        imageAlt: 'Custom image',
        showCancelButton: true,
        confirmButtonText: 'Submit',
        cancelButtonText: 'Cancel',
        reverseButtons: true,
        preConfirm: () => {
            Swal.fire({
                title: 'Payment Details',
                html:
                '<input id="swal-input1" class="swal2-input" placeholder="Transaction ID">' +
                '<input id="swal-input2" class="swal2-input" value=\'600\' readonly placeholder="Amount Paid">' +
                '<input type="file" id="swal-input3" class="swal2-file" placeholder="Screenshot of Payment">',
                focusConfirm: false,
                preConfirm: () => {
                    const fileInput = document.getElementById('swal-input3');
                    return {
                        transaction_id: document.getElementById('swal-input1').value,
                        amount_paid: document.getElementById('swal-input2').value,
                        screenshot: fileInput.files.length > 0 ? fileInput.files[0] : null
                    };
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    const formData = new FormData();
                    formData.append('transaction_id', result.value.transaction_id);
                    formData.append('amount_paid', result.value.amount_paid);
                    if (result.value.screenshot) {
                        formData.append('screenshot', result.value.screenshot);
                    }

                    setRequestHeader();

                    $.ajax({
                        type: 'POST',
                        url: '../make_payment/',
                        data: formData,
                        processData: false, // Important: Prevent jQuery from converting the data
                        contentType: false, // Important: Let the browser set the content type
                        success: function(response) {
                            if (response['status'] === 'success') {
                                Swal.fire({
                                    icon: 'success',
                                    title: 'Payment Successful',
                                    text: 'Your payment has been received',
                                });
                            } else {
                                Swal.fire({
                                    icon: 'error',
                                    title: 'Payment Failed',
                                    text: response['error'] || 'Your payment could not be processed',
                                });
                            }
                        },
                        error: function(error) {
                            Swal.fire({
                                icon: 'error',
                                title: 'Payment Failed',
                                text: 'An error occurred during the submission',
                            });
                        }
                    });
                }
            });
        }
    });
}

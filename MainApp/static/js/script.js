'use strict';

const navbar = document.querySelector("[data-navbar]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");
const navbarToggler = document.querySelector("[data-nav-toggler]");

// get form closing time from the server
function getFormClosingTime() {
  return new Promise((resolve, reject) => {
    setRequestHeader();
    $.ajax({
      dataType: 'json',
      type: 'GET',
      url: "../get_form_closing_time/",
      success: function (data) {
        const closingTime = new Date(data.form_closing_time).getTime();
        resolve(closingTime);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        const defaultClosingTime = new Date("Oct 31, 2024 12:00:00").getTime();
        resolve(defaultClosingTime);
      }
    });
  });
}

getFormClosingTime().then(function(countDownDate) {
  console.log("Form closing time:", countDownDate);
  // Update the count down every 1 second
  var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
    
  // Find the distance between now and the count down date
  var distance = countDownDate - now;
    
  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
  // Output the result in an element with id="demo"
  document.getElementById("counter").innerHTML = days + "d " + hours + "h "
  + minutes + "m " + seconds + "s ";
    
  // If the count down is over, write some text 
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("demo").innerHTML = "EXPIRED";
  }
}, 1000);

});

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



navbarToggler.addEventListener("click", function () {
  navbar.classList.toggle("active");
  this.classList.toggle("active");
});

for (let i = 0; i < navbarLinks.length; i++) {
  navbarLinks[i].addEventListener("click", function () {
    navbar.classList.remove("active");
    navbarToggler.classList.remove("active");
  });
}



/**
 * search toggle
 */

const searchTogglers = document.querySelectorAll("[data-search-toggler]");
const searchBox = document.querySelector("[data-search-box]");

for (let i = 0; i < searchTogglers.length; i++) {
  searchTogglers[i].addEventListener("click", function () {
    searchBox.classList.toggle("active");
  });
}



/**
 * header
 */

const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

window.addEventListener("scroll", function () {
  if (window.scrollY >= 200) {
    header.classList.add("active");
    backTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    backTopBtn.classList.remove("active");
  }
});

function register(){
  var ele = document.getElementById('popup_window');
  ele.style.display = 'block';
  ele.onclick = function(){
    ele.style.display = 'none';
  }
}

function CreateAccount(){
  console.log("Create Account");
  var ele = document.getElementById('popup_registration');
  ele.style.display = 'block';
  ele.onclick = function(event) {
    // If the clicked element is not the form, hide the div
    if (!event.target.closest('form')) {
      ele.style.display = 'none';
    }
  }
  
}

function RegisterAccount(event) {

  var data = {
    name: document.getElementById('registration_name').value,
    email: document.getElementById('registration_email').value
  }

  // Show loading overlay
  document.getElementById('loadingOverlay').style.display = 'flex';

  setRequestHeader();

  $.ajax({
    dataType: 'json',
    type: 'POST',
    url: "register/",
    data: data,
    success: function (data) {
      console.log("Success:", data);      
      Swal.fire({
        title: 'Registered Successfully!!!',
        text: 'Please check your email for further instructions',
        icon: 'info',
        confirmButtonText: 'OK'
      }); 
      document.getElementById('popup_registration').style.display = 'none';
    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log("Error:", errorThrown);
    },
    complete: function() {
      // Hide loading overlay after AJAX call completes (both success and error)
      document.getElementById('loadingOverlay').style.display = 'none';
    }
  });
}





function LoginUser(){
  var ele = document.getElementById('popup_login');
  ele.style.display = 'block';
}

function LoginAccount(){
  var data = {
    email: document.getElementById('login_email').value,
    password: document.getElementById('login_password').value
  }
  console.log(data);
  setRequestHeader();

  $.ajax({
      dataType: 'json',
      type: 'POST',
      url: "login/",
      data: data,
      success: function (data) {
          console.log("Success:", data);      
          Swal.fire({
            title: 'Login Successfully!!!',
            text: 'Welcome to the website',
            icon: 'info',
            confirmButtonText: 'OK'
        }); 
        document.getElementById('popup_login').style.display = 'none';
        // wait for 2sec
        
        window.location.href = '/';
      },
      error: function (jqXHR, textStatus, errorThrown) {
          Swal.fire({
            title: 'Error!!!',
            text: 'Invalid Email or Password',
            icon: 'error',
            confirmButtonText: 'OK'
      });
    }
  });

}


function updateTitle() {
  const heroTitle = document.getElementById('brand-text');
  if (! heroTitle ){
    return;
  }
  if (window.innerWidth < 600) {
    heroTitle.innerHTML = 'X';
    heroTitle.style.fontSize = '6rem';
  } else {
    heroTitle.innerHTML = 'Presents';
  }
}

// Run the function on page load
updateTitle();

// Run the function on window resize
window.onresize = updateTitle;



// registration form

var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  // if x is undefined, return
  if (x.length == 0) {
    return;
  }
  x[n].style.display = "flex";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    document.getElementById('loadingOverlay').style.display = 'flex';

    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}



function adjustMembers() {

  var teamStrength = document.getElementById("team_strength");
  var member4 = document.getElementById("member4");
  if (!member4 || !teamStrength) {
      return;
  }
  teamStrength = teamStrength.value;
  console.log("Team Strength:", teamStrength);
  
  // Show/hide member 4 input based on the selected team strength
  if (teamStrength == 4) {
      member4.style.display = "block";  // Show Member 4 field
      member4.value = ""

  } else {
      member4.style.display = "none";    // Hide Member 4 field
      member4.value = "None"
  }
}

// Set initial state based on the default value (team of 3)
window.onload = function() {
  adjustMembers(); // Call this to set the initial visibility and state
};


document.getElementById('Idea-ppt').addEventListener('change', function() {
  var file = this.files[0];  // Get the uploaded file
  console.log("File Size:", file.size);
  if (file.size > 2097152) {  // 2MB in bytes
      Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'The file size must be less than 2MB!',
      });
      this.value = '';  // Clear the file input
  }
});
console.log(document.getElementById('Idea-ppt'));
// Add your JavaScript functionality here

// Function to validate the signup form
function validateSignupForm() {
    var firstName = document.getElementById("first-name").value;
    var lastName = document.getElementById("last-name").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
  
    // Perform validation checks
    if (firstName === "") {
      alert("Please enter your first name.");
      return false;
    }
  
    if (lastName === "") {
      alert("Please enter your last name.");
      return false;
    }
  
    if (email === "") {
      alert("Please enter your email.");
      return false;
    }
  
    if (password === "") {
      alert("Please enter a password.");
      return false;
    }
  
    // All validation checks pass
    return true;
  }
  
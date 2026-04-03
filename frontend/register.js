const registration = {
    form: document.getElementById("registration-form"),
    email: document.getElementById("new-email"),
    password: document.getElementById("new-password"),
    confirmPassword: document.getElementById("confirmPassword"),
    registrationScreen: document.getElementById("registration-screen"),
    registrationButton: document.getElementById("register-btn"),
};

const login = {
    form: document.getElementById("login-form"),
    email: document.getElementById("email"),
    password: document.getElementById("password"),
    loginScreen: document.getElementById("login-screen"),
    loginButton: document.getElementById("login-btn"),
    goRegisterButton: document.getElementById("go-register-btn"),
};

console.log("login-screen element:", document.getElementById("login-screen"));

//validation
registration.form.addEventListener("submit", function (e) {
  e.preventDefault();

  const isRequiredValid = checkRequired([
    registration.email, 
    registration.password, 
    registration.confirmPassword
  ]);

  let isFormValid = isRequiredValid;

  if (isRequiredValid) {
    const isEmailValid = checkEmail(registration.email);
    const isPasswordValid = checkLength(registration.password, 6, 25);
    const isPasswordsMatch = checkPasswordsMatch(registration.password, registration.confirmPassword);

    isFormValid = isEmailValid && isPasswordValid && isPasswordsMatch;
  }

  if (isFormValid) {
    alert("Registration successful!");
    registration.form.reset();
    document.querySelectorAll(".form-group").forEach((group) => {
      group.className = "form-group";
    });
  }
});
function checkPasswordsMatch(input1, input2) {
  if (input1.value !== input2.value) {
    showError(input2, "Passwords do not match");
    return false;
  }
  return true;
}

function checkEmail(email) {
  // Email regex that covers most common email formats
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (emailRegex.test(email.value.trim())) {
    showSuccess(email);
    return true;
  } else {
    showError(email, "Email is not valid");
    return false;
  }
}

function checkLength(input, min, max) {
  if (input.value.length < min) {
    showError(input, `${formatFieldName(input)} must be at least ${min} characters.`);
    return false;
  } else if (input.value.length > max) {
    showError(input, `${formatFieldName(input)} must be less than ${max} characters.`);
    return false;
  } else {
    showSuccess(input);
    return true;
  }
}

function checkRequired(inputArray) {
  let isValid = true;

  inputArray.forEach((input) => {
    // Password is required
    if (input.value.trim() === "") {
      showError(input, `${formatFieldName(input)} is required`);
      isValid = false;
    } else {
      showSuccess(input);
    }
  });

  return isValid;
}

// format the field name with capitalization
function formatFieldName(input) {
  return input.id.charAt(0).toUpperCase() + input.id.slice(1);
}

function showError(input, message) {
  const formGroup = input.parentElement;
  formGroup.className = "form-group error";
  const small = formGroup.querySelector("small");
  small.innerText = message;
}

function showSuccess(input) {
  const formGroup = input.parentElement;
  formGroup.className = "form-group success";
}

//changing pages based on what button is pressed
function goToRegistration(){
    login.goRegisterButton.addEventListener("click",(e) => {
      e.preventDefault();
      //console.log("Button clicked!");
    login.loginScreen.classList.remove("active");
    registration.registrationScreen.classList.add("active");
    });
}
goToRegistration();

// Custom JavaScript for the Flask Monolith application

document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss alerts after 5 seconds
  setTimeout(function () {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 5000);

  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Initialize popovers
  const popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Password strength indicator
  const passwordFields = document.querySelectorAll('input[type="password"]');

  passwordFields.forEach(function (field) {
    if (field.id === "password" || field.name === "password") {
      field.addEventListener("input", function () {
        checkPasswordStrength(field);
      });
    }
  });

  function checkPasswordStrength(passwordField) {
    const password = passwordField.value;
    let strength = 0;
    let strengthIndicator = document.getElementById("password-strength");

    // If indicator doesn't exist, create it
    if (!strengthIndicator) {
      strengthIndicator = document.createElement("div");
      strengthIndicator.id = "password-strength";
      strengthIndicator.className = "progress mt-2";
      strengthIndicator.innerHTML =
        '<div class="progress-bar" role="progressbar" style="width: 0%"></div>';
      passwordField.parentNode.appendChild(strengthIndicator);
    }

    const progressBar = strengthIndicator.querySelector(".progress-bar");

    // Password length check
    if (password.length >= 8) {
      strength += 25;
    }

    // Contains lowercase
    if (password.match(/[a-z]/)) {
      strength += 25;
    }

    // Contains uppercase
    if (password.match(/[A-Z]/)) {
      strength += 25;
    }

    // Contains numbers or special characters
    if (password.match(/[0-9]/) || password.match(/[^a-zA-Z0-9]/)) {
      strength += 25;
    }

    // Update the progress bar
    progressBar.style.width = strength + "%";

    // Set the color based on strength
    if (strength < 50) {
      progressBar.className = "progress-bar bg-danger";
    } else if (strength < 75) {
      progressBar.className = "progress-bar bg-warning";
    } else {
      progressBar.className = "progress-bar bg-success";
    }
  }
});

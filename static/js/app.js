/* =========================================================
   QUIZARENA - PARTICIPANT FRONTEND
   Frontend-only demo logic
   Backend can be connected later by the team lead.
========================================================= */

const STORAGE_USER = "qa_student_user";
const STORAGE_SESSION = "qa_student_session";
const STORAGE_TEAM = "qa_student_team";
const STORAGE_PROGRESS = "qa_student_progress";


/* -------------------------
   STORAGE HELPERS
------------------------- */

function getData(key, fallback = null) {
  try {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : fallback;
  } catch {
    return fallback;
  }
}

function saveData(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}


/* -------------------------
   SESSION
------------------------- */

function getCurrentUser() {
  return getData(STORAGE_SESSION);
}

function getCurrentTeam() {
  return getData(STORAGE_TEAM);
}

function logout() {
  localStorage.clear();
  sessionStorage.clear();
  window.location.href = "/logout";
}


/* -------------------------
   LOGIN
------------------------- */

function initLogin() {

  const form = document.getElementById("loginForm");

  if (!form) return;

  form.addEventListener("submit", function (event) {

    event.preventDefault();

    const email = document
      .getElementById("email")
      .value
      .trim()
      .toLowerCase();

    const password = document
      .getElementById("password")
      .value;

    let users = getData(STORAGE_USER, []);

    /*
      Demo account
      Backend authentication will replace this later.
    */

    if (users.length === 0) {

      users.push({
        name: "Demo Participant",
        email: "maya@college.edu",
        password: "demo123"
      });

      saveData(STORAGE_USER, users);
    }


    const user = users.find(
      item =>
        item.email === email &&
        item.password === password
    );


    if (!user) {

      showMessage(
        form,
        "Invalid email or password.",
        "error"
      );

      return;
    }


    saveData(STORAGE_SESSION, {
      name: user.name,
      email: user.email
    });


    window.location.href = "dashboard.html";
  });
}


/* -------------------------
   REGISTER
------------------------- */

function initRegister() {

  const form = document.getElementById("registerForm");

  if (!form) return;


  form.addEventListener("submit", function (event) {

    event.preventDefault();


    const name = document
      .getElementById("name")
      .value
      .trim();

    const email = document
      .getElementById("email")
      .value
      .trim()
      .toLowerCase();

    const password = document
      .getElementById("password")
      .value;

    const confirmPassword = document
      .getElementById("confirmPassword")
      .value;


    if (name.length < 2) {

      showMessage(
        form,
        "Please enter your full name.",
        "error"
      );

      return;
    }


    if (!email.includes("@")) {

      showMessage(
        form,
        "Please enter a valid college email.",
        "error"
      );

      return;
    }


    if (password.length < 6) {

      showMessage(
        form,
        "Password must contain at least 6 characters.",
        "error"
      );

      return;
    }


    if (password !== confirmPassword) {

      showMessage(
        form,
        "Passwords do not match.",
        "error"
      );

      return;
    }


    let users = getData(STORAGE_USER, []);


    if (
      users.some(
        user => user.email === email
      )
    ) {

      showMessage(
        form,
        "This email is already registered.",
        "error"
      );

      return;
    }


    users.push({
      name: name,
      email: email,
      password: password
    });


    saveData(STORAGE_USER, users);


    saveData(STORAGE_SESSION, {
      name: name,
      email: email
    });


    window.location.href = "team.html";
  });
}


/* -------------------------
   MESSAGE
------------------------- */

function showMessage(form, message, type) {

  let messageBox = form.querySelector(".form-message");


  if (!messageBox) {

    messageBox = document.createElement("div");

    messageBox.className = "form-message";

    form.prepend(messageBox);
  }


  messageBox.textContent = message;

  messageBox.className =
    `form-message alert ${type}`;
}


/* -------------------------
   AUTH PROTECTION
------------------------- */

function protectPage() {

  const protectedPages = [
    "dashboard",
    "team",
    "event",
    "arena",
    "leaderboard",
    "profile"
  ];


  const page =
    document.body.dataset.page;


  if (
    protectedPages.includes(page) &&
    !getCurrentUser()
  ) {

    window.location.href = "login.html";

    return false;
  }


  return true;
}


/* -------------------------
   DYNAMIC PARTICIPANT INFO
------------------------- */

function loadParticipantInfo() {

  const user = getCurrentUser();

  if (!user) return;


  /*
    These IDs can be added later to HTML
    when backend integration is done.
  */

  const nameElements =
    document.querySelectorAll(
      "[data-user-name]"
    );

  nameElements.forEach(element => {
    element.textContent = user.name;
  });


  const emailElements =
    document.querySelectorAll(
      "[data-user-email]"
    );

  emailElements.forEach(element => {
    element.textContent = user.email;
  });
}


/* -------------------------
   LOGOUT BUTTONS
------------------------- */

function setupLogout() {

  const logoutButtons =
    document.querySelectorAll(
      ".logout-link, [data-logout]"
    );


  logoutButtons.forEach(button => {

    button.addEventListener(
      "click",
      function (event) {

        event.preventDefault();

        logout();
      }
    );

  });
}


/* -------------------------
   TEAM CODE
------------------------- */

function generateTeamCode() {

  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  let code = "";

  for (let i = 0; i < 3; i++) {

    code +=
      letters[
        Math.floor(
          Math.random() * letters.length
        )
      ];
  }


  code += "-";


  code += Math.floor(
    1000 + Math.random() * 9000
  );


  return code;
}


/* -------------------------
   COPY TEAM CODE
------------------------- */

function setupCopyButtons() {

  const buttons =
    document.querySelectorAll(
      "[data-copy-team]"
    );


  buttons.forEach(button => {

    button.addEventListener(
      "click",
      async function () {

        const team =
          getCurrentTeam();


        if (!team) return;


        try {

          await navigator.clipboard.writeText(
            team.code
          );


          const oldText =
            button.textContent;


          button.textContent =
            "Copied ✓";


          setTimeout(() => {

            button.textContent =
              oldText;

          }, 1500);


        } catch {

          alert(
            `Team Code: ${team.code}`
          );

        }

      }
    );

  });
}


/* -------------------------
   INITIAL PAGE SETUP
------------------------- */

document.addEventListener(
  "DOMContentLoaded",
  function () {

    const page =
      document.body.dataset.page;


    /* Participant information - keeps the name updates active */
    loadParticipantInfo();


    /* Team code copy */
    setupCopyButtons();

  }
);
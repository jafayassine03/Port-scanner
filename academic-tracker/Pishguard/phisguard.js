const allEmails = {
  easy: [
    {
      from: "security@paypal-alerts.com",
      subject: "Urgent Account Verification",
      content: "Your PayPal account has been limited due to suspicious activity.",
      type: "phishing",
      reason: "Suspicious sender and urgency tactics.",
      hint: "Check the sender domain carefully."
    },

    {
      from: "orders@amazon.com",
      subject: "Your package has shipped",
      content: "Your recent Amazon order has been shipped and will arrive tomorrow.",
      type: "safe",
      reason: "Legitimate sender and normal message.",
      hint: "Trusted company domain."
    }
  ],

  medium: [
    {
      from: "support@netfIix-help.com",
      subject: "Payment Failed",
      content: "Update your payment details within 24 hours.",
      type: "phishing",
      reason: "Fake domain uses spelling trick.",
      hint: "Look closely at the spelling of Netflix."
    },

    {
      from: "no-reply@github.com",
      subject: "New sign-in from Chrome",
      content: "We noticed a new sign-in to your GitHub account.",
      type: "safe",
      reason: "Trusted service security notification.",
      hint: "Official GitHub domain."
    }
  ],

  hard: [
    {
      from: "microsoft-support@security-checkup.co",
      subject: "Password Expiring Today",
      content: "Your Microsoft password expires today.",
      type: "phishing",
      reason: "Fake support domain pretending to be Microsoft.",
      hint: "Microsoft emails usually use microsoft.com."
    },

    {
      from: "team@linkedin.com",
      subject: "New login to your account",
      content: "A login to your LinkedIn account was detected.",
      type: "safe",
      reason: "Legitimate login notification.",
      hint: "The domain is authentic."
    }
  ]
};

let difficulty = "easy";
let emails = [...allEmails[difficulty]];

let current = 0;
let score = 0;
let correct = 0;
let wrong = 0;
let streak = 0;
let highScore = localStorage.getItem("highScore") || 0;

let timer = 15;
let timerInterval;

const header = document.getElementById("emailHeader");
const content = document.getElementById("emailContent");
const resultBox = document.getElementById("resultBox");
const nextBtn = document.getElementById("nextBtn");
const restartBtn = document.getElementById("restartBtn");
const timerText = document.getElementById("timer");
const progress = document.getElementById("progress");
const badge = document.getElementById("badge");
const hintBox = document.getElementById("hintBox");

document.getElementById("highScore").textContent = highScore;

document.getElementById("difficultySelect").addEventListener("change", function () {
  difficulty = this.value;
  emails = [...allEmails[difficulty]];
  restartGame();
});

function startTimer() {
  clearInterval(timerInterval);

  timer = 15;
  timerText.textContent = timer;

  timerInterval = setInterval(() => {
    timer--;
    timerText.textContent = timer;

    if (timer <= 0) {
      clearInterval(timerInterval);
      checkAnswer("timeout");
    }
  }, 1000);
}

function loadEmail() {
  const email = emails[current];

  header.innerHTML = `
    <strong>From:</strong> ${email.from}<br>
    <strong>Subject:</strong> ${email.subject}
  `;

  content.textContent = email.content;

  resultBox.style.display = "none";
  nextBtn.style.display = "none";
  hintBox.innerHTML = "";

  document.querySelector(".safe").disabled = false;
  document.querySelector(".phishing").disabled = false;

  startTimer();

  updateProgress();
}

function checkAnswer(answer) {
  clearInterval(timerInterval);

  const email = emails[current];

  resultBox.style.display = "block";
  nextBtn.style.display = "block";

  document.querySelector(".safe").disabled = true;
  document.querySelector(".phishing").disabled = true;

  if (answer === email.type) {
    score += 10;
    correct++;
    streak++;

    resultBox.className = "result correct";

    resultBox.innerHTML = `
      <strong>Correct!</strong><br><br>
      ${email.reason}
    `;
  } else {
    wrong++;
    streak = 0;

    resultBox.className = "result wrong";

    resultBox.innerHTML = `
      <strong>Wrong Answer.</strong><br><br>
      ${email.reason}
    `;
  }

  if (score > highScore) {
    highScore = score;
    localStorage.setItem("highScore", highScore);
    document.getElementById("highScore").textContent = highScore;
  }

  if (streak >= 3) {
    badge.style.display = "block";
    badge.textContent = "🔥 Cyber Security Expert Streak!";
  } else {
    badge.style.display = "none";
  }

  updateStats();
}

function nextEmail() {
  current++;

  if (current >= emails.length) {
    endGame();
    return;
  }

  loadEmail();
}

function updateStats() {
  document.getElementById("score").textContent = score;
  document.getElementById("correct").textContent = correct;
  document.getElementById("wrong").textContent = wrong;
  document.getElementById("streak").textContent = streak;
}

function updateProgress() {
  const percent = ((current + 1) / emails.length) * 100;
  progress.style.width = percent + "%";
}

function endGame() {
  header.innerHTML = "Training Completed";

  content.innerHTML = `
    Final Score: <strong>${score}</strong><br><br>
    You completed the phishing awareness training.
  `;

  document.querySelector(".buttons").style.display = "none";

  resultBox.style.display = "none";
  nextBtn.style.display = "none";

  restartBtn.style.display = "block";

  progress.style.width = "100%";
}

function restartGame() {
  current = 0;
  score = 0;
  correct = 0;
  wrong = 0;
  streak = 0;

  badge.style.display = "none";

  updateStats();

  document.querySelector(".buttons").style.display = "flex";

  restartBtn.style.display = "none";

  emails = [...allEmails[difficulty]];

  loadEmail();
}

function toggleTheme() {
  document.body.classList.toggle("light");

  if (document.body.classList.contains("light")) {
    localStorage.setItem("theme", "light");
  } else {
    localStorage.setItem("theme", "dark");
  }
}

function showHint() {
  const email = emails[current];
  hintBox.innerHTML = email.hint;
}

window.onload = function () {
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme === "light") {
    document.body.classList.add("light");
  }

  loadEmail();
};
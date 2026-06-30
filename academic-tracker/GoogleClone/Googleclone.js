const form = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");
const luckyButton = document.getElementById("luckyBtn");
const themeToggle = document.getElementById("themeToggle");
const historyBox = document.getElementById("searchHistory");

// Dark Mode
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("dark");
  themeToggle.textContent = "☀️";
}

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  if (document.body.classList.contains("dark")) {
    localStorage.setItem("theme", "dark");
    themeToggle.textContent = "☀️";
  } else {
    localStorage.setItem("theme", "light");
    themeToggle.textContent = "🌙";
  }
});

// search histo
function getHistory() {
  return JSON.parse(localStorage.getItem("searches")) || [];
}

function saveSearch(query) {
  let history = getHistory();
  if (!history.includes(query)) {
    history.unshift(query);
  }
  if (history.length > 5) history.pop();
  localStorage.setItem("searches", JSON.stringify(history));
}

function renderHistory(list) {
  historyBox.innerHTML = "";
  list.forEach(item => {
    const div = document.createElement("div");
    div.textContent = item;
    div.classList.add("history-item");
    div.addEventListener("click", () => {
      searchInput.value = item;
    });
    historyBox.appendChild(div);
  });
}

searchInput.addEventListener("focus", () => renderHistory(getHistory()));
searchInput.addEventListener("input", () => {
  const filtered = getHistory().filter(item =>
    item.toLowerCase().includes(searchInput.value.toLowerCase())
  );
  renderHistory(filtered);
});


function handleSearch(lucky = false) {
  const query = searchInput.value.trim();
  if (!query) return;

  saveSearch(query);

  // URL detect
  if (query.startsWith("http://") || query.startsWith("https://")) {
    window.location.href = query;
    return;
  }
  if (query.includes(".") && !query.includes(" ")) {
    window.location.href = "https://" + query;
    return;
  }

  let url = "https://www.google.com/search?q=" + encodeURIComponent(query);
  if (lucky) url += "&btnI=I";

  window.location.href = url;
}
form.addEventListener("submit", (e) => {
  e.preventDefault();
  handleSearch(false);
});

luckyButton.addEventListener("click", () => handleSearch(true));

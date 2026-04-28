const apiUrl = "http://127.0.0.1:8000/samples";

async function fetchSamples() {
  const response = await fetch(apiUrl);
  return response.ok ? response.json() : [];
}

function formatNumber(value) {
  return Number(value).toFixed(2);
}

function renderStats(samples) {
  const total = samples.length;
  const safe = samples.filter((item) => item.prediction === "Safe").length;
  const unsafe = total - safe;
  document.getElementById("stat-samples").textContent = total;
  document.getElementById("stat-safe").textContent = safe;
  document.getElementById("stat-unsafe").textContent = unsafe;
}

function renderAverages(samples) {
  if (!samples.length) return;
  const sums = samples.reduce(
    (acc, sample) => {
      acc.ph += Number(sample.ph || 0);
      acc.hardness += Number(sample.hardness || 0);
      acc.conductivity += Number(sample.conductivity || 0);
      acc.turbidity += Number(sample.turbidity || 0);
      return acc;
    },
    { ph: 0, hardness: 0, conductivity: 0, turbidity: 0 }
  );

  const count = samples.length;
  document.getElementById("avg-ph").textContent = formatNumber(sums.ph / count);
  document.getElementById("avg-hardness").textContent = formatNumber(sums.hardness / count);
  document.getElementById("avg-conductivity").textContent = formatNumber(sums.conductivity / count);
  document.getElementById("avg-turbidity").textContent = formatNumber(sums.turbidity / count);
}

function renderChart(samples) {
  const safeCount = samples.filter((item) => item.prediction === "Safe").length;
  const unsafeCount = samples.length - safeCount;
  const ctx = document.getElementById("predictionChart").getContext("2d");

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Safe", "Unsafe"],
      datasets: [
        {
          data: [safeCount, unsafeCount],
          backgroundColor: ["#34d399", "#fb7185"],
          borderColor: "rgba(15, 23, 42, 0.85)",
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "bottom", labels: { color: "#cbd5e1" } },
      },
    },
  });
}

async function initDashboard() {
  const samples = await fetchSamples();
  renderStats(samples);
  renderAverages(samples);
  renderChart(samples);
}

initDashboard().catch(console.error);

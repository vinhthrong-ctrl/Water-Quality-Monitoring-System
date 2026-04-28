async function loadSamples() {
  const tableBody = document.getElementById("samplesTable");

  if (!tableBody) {
    console.error("❌ samplesTable not found in HTML");
    return;
  }

  // Clear table
  tableBody.innerHTML = "";

  // Loading row
  const loadingRow = document.createElement("tr");
  loadingRow.innerHTML = `
    <td class="px-4 py-6 text-center text-slate-400" colspan="13">
      Loading...
    </td>
  `;
  tableBody.appendChild(loadingRow);

  try {
    const response = await fetch("http://127.0.0.1:8000/samples");

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const samples = await response.json();
    console.log("DATA:", samples);

    tableBody.innerHTML = "";

    // ✅ Handle empty or invalid data
    if (!Array.isArray(samples) || samples.length === 0) {
      const emptyRow = document.createElement("tr");
      emptyRow.innerHTML = `
        <td class="px-4 py-6 text-center text-slate-400" colspan="13">
          No samples available yet.
        </td>
      `;
      tableBody.appendChild(emptyRow);
      return;
    }

    // Render rows
    samples.forEach((sample) => {
      const row = document.createElement("tr");

      const prediction =
        sample.prediction ??
        (sample.potability === 1 ? "Safe" : "Unsafe");

      const suggestions = getSuggestions(sample, prediction);
      const majorSuggestions = suggestions.cleaning.slice(0, 3);

      row.innerHTML = `
        <td class="px-4 py-4">${safe(sample.id)}</td>
        <td class="px-4 py-4">${safe(sample.ph)}</td>
        <td class="px-4 py-4">${safe(sample.hardness)}</td>
        <td class="px-4 py-4">${safe(sample.solids)}</td>
        <td class="px-4 py-4">${safe(sample.chloramines)}</td>
        <td class="px-4 py-4">${safe(sample.sulfate)}</td>
        <td class="px-4 py-4">${safe(sample.conductivity)}</td>
        <td class="px-4 py-4">${safe(sample.organic_carbon)}</td>
        <td class="px-4 py-4">${safe(sample.trihalomethanes)}</td>
        <td class="px-4 py-4">${safe(sample.turbidity)}</td>

        <td class="px-4 py-4 font-semibold text-slate-100">${prediction}</td>

        <td class="px-4 py-4 text-sm leading-6 text-slate-300">
          ${majorSuggestions.map(item => `<div>• ${item}</div>`).join("")}
        </td>

        <td class="px-4 py-4">${safe(sample.potability)}</td>
      `;

      tableBody.appendChild(row);
    });

  } catch (error) {
    console.error(error);

    tableBody.innerHTML = "";

    const errorRow = document.createElement("tr");
    errorRow.innerHTML = `
      <td class="px-4 py-6 text-center text-slate-400" colspan="13">
        <p class="text-rose-300 font-semibold">Error loading samples</p>
        <p class="mt-1 text-xs text-slate-500">${error.message}</p>
      </td>
    `;

    tableBody.appendChild(errorRow);
  }
}


function getSuggestions(values, prediction) {
  const cleaning = [];
  const developing = [];

  if (prediction?.toLowerCase() === "safe") {
    cleaning.push("Water appears safe. Continue regular monitoring.");
    cleaning.push("Maintain filtration and disinfection systems.");
    cleaning.push("Check turbidity and pH regularly.");

    developing.push("Expand safe water distribution.");
    developing.push("Promote eco-friendly water usage.");
    developing.push("Educate communities on conservation.");

    return { cleaning, developing };
  }

  if (values.ph != null) {
    if (values.ph < 6.5) cleaning.push("Low pH: add lime or bicarbonate.");
    if (values.ph > 8.5) cleaning.push("High pH: use acid neutralizer.");
  }

  if (values.hardness != null && values.hardness > 200)
    cleaning.push("Use water softener.");

  if (values.solids != null && values.solids > 15000)
    cleaning.push("Use reverse osmosis.");

  if (values.chloramines != null && values.chloramines > 4)
    cleaning.push("Use activated carbon filtration.");

  if (values.sulfate != null && values.sulfate > 250)
    cleaning.push("Use RO or distillation.");

  if (values.conductivity != null && values.conductivity > 500)
    cleaning.push("Improve filtration.");

  if (values.organic_carbon != null && values.organic_carbon > 10)
    cleaning.push("Use biological filtration.");

  if (values.trihalomethanes != null && values.trihalomethanes > 80)
    cleaning.push("Use aeration + carbon filters.");

  if (values.turbidity != null && values.turbidity > 5)
    cleaning.push("Use sedimentation + filtration.");

  if (!cleaning.length) {
    cleaning.push("Improve filtration and monitor water quality.");
  }

  developing.push("Build water treatment infrastructure.");
  developing.push("Promote rainwater harvesting.");
  developing.push("Run awareness campaigns.");

  return { cleaning, developing };
}


// ✅ Prevent null/undefined showing in UI
function safe(value) {
  return value ?? "-";
}


// ✅ Load on page start
window.addEventListener("DOMContentLoaded", loadSamples);
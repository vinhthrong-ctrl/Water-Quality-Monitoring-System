function getFloat(value) {
  return value ? parseFloat(value) : null;
}

function getInt(value) {
  return value ? parseInt(value) : null;
}

const form = document.getElementById("sampleForm");
const responseMessage = document.getElementById("responseMessage");

const apiUrl = "http://127.0.0.1:8000/add-sample";

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  console.log("Form submitted ✅");

  const formData = new FormData(form);

  const payload = {
    ph: getFloat(formData.get("ph")),
    hardness: getFloat(formData.get("hardness")),
    solids: getFloat(formData.get("solids")),
    chloramines: getFloat(formData.get("chloramines")),
    sulfate: getFloat(formData.get("sulfate")),
    conductivity: getFloat(formData.get("conductivity")),
    organic_carbon: getFloat(formData.get("organic_carbon")),
    trihalomethanes: getFloat(formData.get("trihalomethanes")),
    turbidity: getFloat(formData.get("turbidity")),
    potability: getInt(formData.get("potability"))
  };

  try {
    // 🔹 Single API call (backend handles prediction + save)
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Failed to save sample (${response.status})`);
    }

    const data = await response.json();

    // 🔹 Show prediction result
    responseMessage.classList.remove("hidden");

    // Optional: generate suggestions on frontend (UI only)
    const suggestions = getSuggestions(payload, data.prediction);

    responseMessage.innerHTML = `
      <p>Prediction: <strong>${data.prediction}</strong></p>
      <p>Probability: ${data.probability}</p>
      <div style="margin-top:10px;">
        <strong>Suggestions:</strong>
        ${suggestions.cleaning.map(s => `<div>• ${s}</div>`).join("")}
      </div>
    `;

    // 🔹 Reset form
    form.reset();

    // 🔹 Optional: reload table if you have one
    if (typeof loadSamples === "function") {
      loadSamples();
    }

  } catch (err) {
    console.error(err);
    responseMessage.classList.remove("hidden");
    responseMessage.innerHTML = `<p style="color:red;">${err.message}</p>`;
  }
});


function getSuggestions(values, prediction) {
  const cleaning = [];
  const developing = [];

  if (prediction === "Safe") {
    cleaning.push("Water appears safe. Continue regular monitoring and keep source areas clean.");
    cleaning.push("Maintain filtration and disinfection systems to preserve water quality.");
    cleaning.push("Check turbidity and pH monthly to prevent contamination drift.");

    developing.push("Develop sustainable water distribution networks.");
    developing.push("Promote eco-tourism around clean water sources.");
    developing.push("Invest in community education on water conservation.");

    return { cleaning, developing };
  }

  if (values.ph !== null) {
    if (values.ph < 6.5) cleaning.push("pH too low: add lime or bicarbonate.");
    if (values.ph > 8.5) cleaning.push("pH too high: use acid dosing.");
  }

  if (values.hardness > 200) cleaning.push("Use water softener.");
  if (values.solids > 15000) cleaning.push("Use reverse osmosis.");
  if (values.chloramines > 4) cleaning.push("Use activated carbon filtration.");
  if (values.sulfate > 250) cleaning.push("Use RO or distillation.");
  if (values.conductivity > 500) cleaning.push("Improve filtration.");
  if (values.organic_carbon > 10) cleaning.push("Use biological filtration.");
  if (values.trihalomethanes > 80) cleaning.push("Use aeration + carbon filters.");
  if (values.turbidity > 5) cleaning.push("Use sedimentation + filtration.");

  if (!cleaning.length) {
    cleaning.push("Improve filtration and monitor water quality regularly.");
  }

  developing.push("Build water treatment infrastructure.");
  developing.push("Promote rainwater harvesting.");
  developing.push("Run public awareness campaigns.");

  return { cleaning, developing };
}
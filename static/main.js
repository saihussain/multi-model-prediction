// modern UI script for Multi-Model Predictor
const modelSelect = document.getElementById("modelSelect");
const inputsDiv = document.getElementById("inputs");
const resultPre = document.getElementById("result");
const predictBtn = document.getElementById("predictBtn");
const metaDiv = document.getElementById("meta");
const fillBtn = document.getElementById("fillSampleBtn");
const clearBtn = document.getElementById("clearBtn");
const csvBtn = document.getElementById("csvBtn");
const serverAddr = document.getElementById("serverAddr");
const probBars = document.getElementById("probBars");
const probContainer = document.getElementById("probContainer");

let modelMeta = {};

async function loadModels(){
  try{
    const r = await fetch("/models");
    if(!r.ok) throw new Error("failed to fetch models");
    const j = await r.json();
    const models = j.models || [];
    modelSelect.innerHTML = "";
    models.forEach(m => {
      const o = document.createElement("option");
      o.value = m; o.textContent = m;
      modelSelect.appendChild(o);
    });
    // feature counts used in this project:
    modelMeta["iris"] = {feature_count:4, display:["sepal_length","sepal_width","petal_length","petal_width"]};
    modelMeta["breast_cancer"] = {feature_count:30};
    serverAddr.textContent = window.location.origin;
    metaDiv.textContent = `Selected: ${modelSelect.value}`;
    renderInputs();
  }catch(err){
    metaDiv.textContent = "Failed to load models: " + err.message;
    console.error(err);
  }
}

function renderInputs(){
  const model = modelSelect.value;
  const count = (modelMeta[model] && modelMeta[model].feature_count) || (model==="breast_cancer"?30:4);
  inputsDiv.innerHTML = "";
  for(let i=0;i<count;i++){
    const wrapper = document.createElement("div");
    wrapper.className = "feature card-field";
    const label = document.createElement("label");
    label.textContent = modelMeta[model] && modelMeta[model].display ? modelMeta[model].display[i] : `Feature ${i}`;
    const inp = document.createElement("input");
    inp.type = "number"; inp.step = "any"; inp.id = "f"+i; inp.placeholder = "0.0";
    wrapper.appendChild(label);
    wrapper.appendChild(inp);
    inputsDiv.appendChild(wrapper);
  }
  metaDiv.textContent = `Selected: ${model} — ${count} features`;
  resultPre.textContent = "No prediction yet.";
  probContainer.style.display = "none";
  probBars.innerHTML = "";
}

modelSelect.addEventListener("change", renderInputs);

predictBtn.addEventListener("click", async ()=>{
  const model = modelSelect.value;
  const count = modelMeta[model].feature_count;
  const features = [];
  let anyEmpty = false;
  for(let i=0;i<count;i++){
    const el = document.getElementById("f"+i);
    if(!el) continue;
    const value = el.value.trim();
    if(value === "") { anyEmpty = true; }
    features.push(value === "" ? 0.0 : parseFloat(value));
  }
  if(anyEmpty){
    if(!confirm("Some fields are empty — empties will be treated as 0.0. Continue?")) return;
  }

  resultPre.textContent = "Requesting prediction…";
  probContainer.style.display = "none";
  try{
    const r = await fetch("/predict", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({model, features})
    });
    const j = await r.json();
    if(r.status !== 200){
      resultPre.textContent = "Error: " + (j.error || JSON.stringify(j));
      return;
    }
    resultPre.textContent = JSON.stringify(j, null, 2);

    // show probabilities if present
    if(j.probabilities && Array.isArray(j.probabilities[0])){
      // multi-class, take first row
      const probs = j.probabilities[0];
      showProbabilities(probs, j.class_name || "");
    } else if(j.probabilities && Array.isArray(j.probabilities)){
      // binary as [p0,p1]
      const probs = j.probabilities[0] || j.probabilities;
      showProbabilities(probs, j.class_name || "");
    } else {
      probContainer.style.display = "none";
    }
  }catch(err){
    resultPre.textContent = "Request failed: " + err.message;
    console.error(err);
  }
});

function showProbabilities(probs, predictedName){
  probBars.innerHTML = "";
  const total = probs.reduce((a,b)=>a+b,0);
  probs.forEach((p,i)=>{
    const wrapper = document.createElement("div");
    wrapper.className = "prob";
    const bar = document.createElement("div");
    bar.className = "bar";
    const frac = total ? (p/total) : 0;
    bar.style.width = `${Math.round(frac*100)}%`;
    const label = document.createElement("span");
    label.textContent = `${Math.round(frac*100)}%`;
    wrapper.appendChild(bar);
    wrapper.appendChild(label);
    probBars.appendChild(wrapper);
  });
  probContainer.style.display = "block";
}

// fill examples
fillBtn.addEventListener("click", ()=>{
  const model = modelSelect.value;
  if(model === "iris"){
    [5.1,3.5,1.4,0.2].forEach((v,i)=>document.getElementById("f"+i).value = v);
  } else {
    const vals = [17.99,10.38,122.8,1001.0,0.1184,0.2776,0.3001,0.1471,0.2419,0.07871,1.095,0.905,8.589,153.4,0.0064,0.049,0.0537,0.01585,0.03003,0.006193,25.38,17.33,184.6,2019.0,0.1622,0.6656,0.7119,0.2654,0.4601,0.1189];
    vals.forEach((v,i)=>document.getElementById("f"+i).value = v);
  }
});

// clear
clearBtn.addEventListener("click", ()=>{
  const inputs = inputsDiv.querySelectorAll("input");
  inputs.forEach(i=>i.value = "");
  resultPre.textContent = "Cleared inputs.";
  probContainer.style.display = "none";
});

// CSV upload
csvBtn.addEventListener("click", ()=>{
  const inp = document.createElement("input");
  inp.type = "file";
  inp.accept = ".csv,text/csv";
  inp.onchange = async (e)=>{
    const file = e.target.files[0];
    if(!file) return;
    const text = await file.text();
    // send raw CSV to batch endpoint
    const r = await fetch("/models", {
      method:"POST",
      headers:{"Content-Type":"text/csv"},
      body: text
    });
    const j = await r.json();
    resultPre.textContent = JSON.stringify(j, null, 2);
  };
  inp.click();
});

loadModels();

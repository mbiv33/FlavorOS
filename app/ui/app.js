const apiBase = window.FLAVOROS_API_URL || "http://127.0.0.1:8091";
const stateUrl = `${apiBase}/api/dashboard-state`;
const sampleIngestUrl = `${apiBase}/api/mock/gmail-ingest`;

const providerHealth = document.getElementById("provider-health");
const heroMetrics = document.getElementById("hero-metrics");
const inboxList = document.getElementById("inbox-list");
const workOrderList = document.getElementById("work-order-list");
const approvalList = document.getElementById("approval-list");
const outboundList = document.getElementById("outbound-list");
const sampleIngestButton = document.getElementById("sample-ingest-button");
const sampleIngestStatus = document.getElementById("sample-ingest-status");

function badge(label, tone = "") {
  const cls = tone ? `badge badge-${tone}` : "badge";
  return `<span class="${cls}">${label}</span>`;
}

function renderMetric(label, value) {
  return `
    <div class="metric">
      <strong>${value}</strong>
      <span class="meta">${label}</span>
    </div>
  `;
}

function renderCard(item) {
  const badges = (item.badges || [])
    .map((entry) => badge(entry.label, entry.tone))
    .join("");

  return `
    <div class="card">
      <strong class="card-title">${item.title}</strong>
      <div class="card-copy">${item.copy}</div>
      <div class="meta">${item.meta}</div>
      <div class="badge-row">${badges}</div>
    </div>
  `;
}

async function loadState() {
  const response = await fetch(stateUrl);
  if (!response.ok) {
    throw new Error(`Failed to load state: ${response.status}`);
  }
  return response.json();
}

async function ingestSample() {
  sampleIngestButton.disabled = true;
  sampleIngestStatus.textContent = "Ingesting sample Gmail item...";
  try {
    const response = await fetch(sampleIngestUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({})
    });
    if (!response.ok) {
      throw new Error(`Failed to ingest sample: ${response.status}`);
    }
    sampleIngestStatus.textContent = "Sample Gmail item ingested.";
    const state = await loadState();
    render(state);
  } catch (error) {
    sampleIngestStatus.textContent = error.message;
  } finally {
    sampleIngestButton.disabled = false;
  }
}

function setCount(id, count, label) {
  const el = document.getElementById(id);
  el.textContent = `${count} ${label}`;
}

function render(state) {
  providerHealth.innerHTML = state.providers
    .map((provider) => `<li><strong>${provider.name}</strong><div class="meta">${provider.status}</div></li>`)
    .join("");

  heroMetrics.innerHTML = state.metrics
    .map((metric) => renderMetric(metric.label, metric.value))
    .join("");

  inboxList.innerHTML = state.inbox.map(renderCard).join("");
  workOrderList.innerHTML = state.workOrders.map(renderCard).join("");
  approvalList.innerHTML = state.approvals.map(renderCard).join("");
  outboundList.innerHTML = state.outbound.map(renderCard).join("");

  setCount("inbox-count", state.inbox.length, "items");
  setCount("work-order-count", state.workOrders.length, "active");
  setCount("approval-count", state.approvals.length, "pending");
  setCount("outbound-count", state.outbound.length, "staged");
}

sampleIngestButton?.addEventListener("click", ingestSample);

loadState()
  .then(render)
  .catch((error) => {
    inboxList.innerHTML = `<div class="card"><strong class="card-title">App state unavailable</strong><div class="card-copy">${error.message}</div></div>`;
  });

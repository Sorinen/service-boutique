let sales = JSON.parse(localStorage.getItem("sales")) || [];

const dayTotal = document.getElementById("dayTotal");
const monthTotal = document.getElementById("monthTotal");
const yearTotal = document.getElementById("yearTotal");
const revenueTotal = document.getElementById("revenueTotal");

const tableBody = document.getElementById("salesTableBody");
const canvas = document.getElementById("chart");
const ctx = canvas.getContext("2d");

const modal = document.getElementById("saleModal");
const productInput = document.getElementById("productInput");
const qtyInput = document.getElementById("qtyInput");
const priceInput = document.getElementById("priceInput");
const paymentInput = document.getElementById("paymentInput");

/* ===============================
   ÉVÉNEMENTS
================================ */
document.querySelector(".add-btn").addEventListener("click", openModal);
document.querySelector(".cancel").addEventListener("click", closeModal);
document.querySelector(".confirm").addEventListener("click", confirmSale);

/* Supprimé : Filtrage sur clic des cartes */
// dayTotal.addEventListener("click", () => renderSales("day"));
// monthTotal.addEventListener("click", () => renderSales("month"));
// yearTotal.addEventListener("click", () => renderSales("year"));

/* Cliquer sur liste de vente pour page complète */
document.querySelector(".sales h3").addEventListener("click", () => {
  window.location.href = "/ventes";
});

document.querySelector(".stats").addEventListener("click", () => {
  window.location.href = "/ventes";
});

/* ===============================
   MODAL
================================ */
function openModal() {
  modal.classList.remove("hidden");
}

function closeModal() {
  modal.classList.add("hidden");
  productInput.value = "";
  qtyInput.value = 1;
  priceInput.value = "";
  paymentInput.value = "Carte";
}

function confirmSale() {
  const title = productInput.value.trim();
  const qty = Number(qtyInput.value);
  const price = Number(priceInput.value);
  const payment = paymentInput.value;

  if (!title || qty <= 0 || price <= 0) {
    alert("Veuillez remplir tous les champs");
    return;
  }

  const sale = {
    id: Date.now(),
    title,
    qty,
    price,
    payment,
    date: new Date()
  };

  sales.push(sale);
  saveSales();
  closeModal();
  render();
}

/* ===============================
   RENDER GLOBAL
================================ */
function render() {
  renderSales(); // Affiche toutes les ventes
  updateStats();
  drawChart();
}

/* ===============================
   TABLEAU DES VENTES
================================ */
function renderSales() {
  tableBody.innerHTML = "";

  sales.slice().reverse().forEach(sale => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${new Date(sale.date).toLocaleDateString()}</td>
      <td>${sale.title}</td>
      <td>${sale.qty}</td>
      <td>${sale.payment}</td>
      <td>${sale.price * sale.qty} €</td>
    `;
    tableBody.appendChild(tr);
  });
}

/* ===============================
   STATISTIQUES (Revenus en €)
================================ */
function updateStats() {
  const today = new Date();
  let dayRevenue = 0;
  let monthRevenue = 0;
  let yearRevenue = 0;
  let totalRevenue = 0;

  sales.forEach(sale => {
    const d = new Date(sale.date);
    const amount = sale.price * sale.qty;
    totalRevenue += amount;

    // Revenu du jour
    if (d.toDateString() === today.toDateString()) {
      dayRevenue += amount;
    }
    
    // Revenu du mois
    if (d.getMonth() === today.getMonth() && d.getFullYear() === today.getFullYear()) {
      monthRevenue += amount;
    }
    
    // Revenu de l'année
    if (d.getFullYear() === today.getFullYear()) {
      yearRevenue += amount;
    }
  });

  dayTotal.querySelector("h2").textContent = `${dayRevenue} €`;
  monthTotal.querySelector("h2").textContent = `${monthRevenue} €`;
  yearTotal.querySelector("h2").textContent = `${yearRevenue} €`;
  revenueTotal.querySelector("h2").textContent = `${totalRevenue} €`;
}

/* ===============================
   GRAPHIQUE (GRAND ET LISIBLE)
================================ */
function drawChart() {
  // Grande taille pour bien voir
  canvas.width = canvas.parentElement.offsetWidth - 16;
  canvas.height = 350;
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const days = Array(31).fill(0);

  sales.forEach(sale => {
    const d = new Date(sale.date);
    days[d.getDate() - 1] += sale.price * sale.qty;
  });

  // Max adaptatif (minimum 100€)
  const maxValue = Math.max(...days, 1);
  const max = Math.max(100, Math.ceil(maxValue / 50) * 50);
  
  // Marges généreuses pour les axes
  const marginLeft = 55;
  const marginBottom = 45;
  const marginTop = 25;
  const marginRight = 20;
  
  const chartWidth = canvas.width - marginLeft - marginRight;
  const chartHeight = canvas.height - marginBottom - marginTop;

  // ===== FOND =====
  ctx.fillStyle = '#fafafa';
  ctx.fillRect(marginLeft, marginTop, chartWidth, chartHeight);

  // ===== AXE Y (Prix en €) =====
  const stepY = max <= 100 ? 20 : 50;
  
  for (let value = 0; value <= max; value += stepY) {
    const y = marginTop + chartHeight - (value / max) * chartHeight;
    
    // Ligne horizontale
    ctx.beginPath();
    ctx.moveTo(marginLeft, y);
    ctx.lineTo(canvas.width - marginRight, y);
    ctx.strokeStyle = '#e8e8e8';
    ctx.lineWidth = 1;
    ctx.stroke();
    
    // Label prix
    ctx.fillStyle = '#555';
    ctx.font = 'bold 13px -apple-system, sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(value + ' €', marginLeft - 8, y + 5);
  }

  // ===== AXE X (Jours : 1, 5, 10, 15, 20, 25, 30) =====
  const daysToShow = [1, 5, 10, 15, 20, 25, 30];
  
  daysToShow.forEach(day => {
    const x = marginLeft + ((day - 1) / 30) * chartWidth;
    
    // Ligne verticale
    ctx.beginPath();
    ctx.moveTo(x, marginTop);
    ctx.lineTo(x, marginTop + chartHeight);
    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = 1;
    ctx.stroke();
    
    // Label jour
    ctx.fillStyle = '#555';
    ctx.font = 'bold 13px -apple-system, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(day, x, canvas.height - 25);
  });
  
  // Label "Jours du mois"
  ctx.font = '12px -apple-system, sans-serif';
  ctx.fillStyle = '#888';
  ctx.textAlign = 'center';
  ctx.fillText('📅 Jours du mois', marginLeft + chartWidth / 2, canvas.height - 5);

  // ===== ZONE REMPLIE SOUS LA COURBE =====
  const gradient = ctx.createLinearGradient(0, marginTop, 0, canvas.height - marginBottom);
  gradient.addColorStop(0, 'rgba(108, 92, 231, 0.5)');
  gradient.addColorStop(1, 'rgba(108, 92, 231, 0.1)');

  ctx.beginPath();
  ctx.moveTo(marginLeft, marginTop + chartHeight);

  days.forEach((value, index) => {
    const x = marginLeft + (index / 30) * chartWidth;
    const y = marginTop + chartHeight - (value / max) * chartHeight;
    ctx.lineTo(x, y);
  });

  ctx.lineTo(marginLeft + chartWidth, marginTop + chartHeight);
  ctx.closePath();
  ctx.fillStyle = gradient;
  ctx.fill();

  // ===== LIGNE DE LA COURBE =====
  ctx.beginPath();
  days.forEach((value, index) => {
    const x = marginLeft + (index / 30) * chartWidth;
    const y = marginTop + chartHeight - (value / max) * chartHeight;
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });

  ctx.strokeStyle = "#6C5CE7";
  ctx.lineWidth = 3.5;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.stroke();

  // ===== POINTS UNIQUEMENT SUR LES JOURS AVEC VENTES =====
  days.forEach((value, index) => {
    if (value > 0) {
      const x = marginLeft + (index / 30) * chartWidth;
      const y = marginTop + chartHeight - (value / max) * chartHeight;
      
      // Gros point
      ctx.beginPath();
      ctx.arc(x, y, 8, 0, Math.PI * 2);
      ctx.fillStyle = "#6C5CE7";
      ctx.fill();
      ctx.strokeStyle = "#fff";
      ctx.lineWidth = 3;
      ctx.stroke();
      
      // Montant au-dessus
      ctx.fillStyle = '#333';
      ctx.font = 'bold 14px -apple-system, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(value + ' €', x, y - 15);
    }
  });

  // ===== BORDURES DES AXES =====
  ctx.beginPath();
  ctx.moveTo(marginLeft, marginTop);
  ctx.lineTo(marginLeft, marginTop + chartHeight);
  ctx.lineTo(canvas.width - marginRight, marginTop + chartHeight);
  ctx.strokeStyle = '#bbb';
  ctx.lineWidth = 2;
  ctx.stroke();
}

/* ===============================
   STOCKAGE
================================ */
function saveSales() {
  localStorage.setItem("sales", JSON.stringify(sales));
}

/* ===============================
   SYNCHRONISATION TEMPS RÉEL
================================ */
function syncData() {
  // Recharger les données depuis localStorage
  sales = JSON.parse(localStorage.getItem("sales")) || [];
  render();
}

// Écouter les changements dans d'autres onglets
window.addEventListener('storage', (e) => {
  if (e.key === 'sales') {
    syncData();
  }
});

// Rafraîchir automatiquement toutes les 5 secondes
setInterval(syncData, 5000);

/* ===============================
   INIT
================================ */
render();
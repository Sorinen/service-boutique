let sales = JSON.parse(localStorage.getItem("sales")) || [];
let currentFilter = "all";

const tableBody = document.getElementById("fullSalesTableBody");
const backBtn = document.getElementById("backBtn");
const filterBtns = document.querySelectorAll(".filters button");
const totalValueSpan = document.getElementById('totalValue');
const downloadBtn = document.getElementById("downloadBtn");

// Retour au dashboard
backBtn.addEventListener("click", () => {
  window.location.href = "/";
});

// Filtres avec indication visuelle
filterBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    // Retirer la classe active de tous les boutons
    filterBtns.forEach(b => b.classList.remove("filter-active"));
    // Ajouter la classe active au bouton cliqué
    btn.classList.add("filter-active");
    // Appliquer le filtre
    currentFilter = btn.dataset.filter;
    renderSales(currentFilter);
  });
});

// Fonction pour afficher les ventes filtrées
function renderSales(filter) {
  tableBody.innerHTML = "";
  const today = new Date();
  
  // Début de la semaine (lundi)
  const startOfWeek = new Date(today);
  const dayOfWeek = today.getDay();
  const diff = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
  startOfWeek.setDate(today.getDate() - diff);
  startOfWeek.setHours(0, 0, 0, 0);

  let filteredSales = sales;

  if (filter === "day") {
    filteredSales = sales.filter(sale => {
      const d = new Date(sale.date);
      return d.toDateString() === today.toDateString();
    });
  } else if (filter === "week") {
    filteredSales = sales.filter(sale => {
      const d = new Date(sale.date);
      return d >= startOfWeek && d <= today;
    });
  } else if (filter === "month") {
    filteredSales = sales.filter(sale => {
      const d = new Date(sale.date);
      return d.getMonth() === today.getMonth() && d.getFullYear() === today.getFullYear();
    });
  } else if (filter === "year") {
    filteredSales = sales.filter(sale => {
      const d = new Date(sale.date);
      return d.getFullYear() === today.getFullYear();
    });
  }

  let total = 0;
  const count = filteredSales.length;

  if (filteredSales.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="5" style="text-align: center; color: #999; padding: 30px;">Aucune vente pour cette période</td>`;
    tableBody.appendChild(tr);
  } else {
    filteredSales.slice().reverse().forEach(sale => {
      const tr = document.createElement("tr");
      const totalSale = sale.price * sale.qty;
      tr.innerHTML = `
        <td>${new Date(sale.date).toLocaleDateString('fr-FR')}</td>
        <td>${sale.title}</td>
        <td>${sale.qty}</td>
        <td>${sale.payment}</td>
        <td>${totalSale} €</td>
      `;
      tableBody.appendChild(tr);
      total += totalSale;
    });
  }

  // Mettre à jour le total avec le nombre de ventes
  totalValueSpan.textContent = `${total} € (${count} vente${count > 1 ? 's' : ''})`;
}

// Synchronisation temps réel
function syncData() {
  sales = JSON.parse(localStorage.getItem("sales")) || [];
  renderSales(currentFilter);
}

// Écouter les changements dans d'autres onglets
window.addEventListener('storage', (e) => {
  if (e.key === 'sales') {
    syncData();
  }
});

// Rafraîchir automatiquement toutes les 5 secondes
setInterval(syncData, 5000);

// Affichage initial
renderSales("all");
// Marquer le bouton "Tout" comme actif par défaut
document.querySelector('[data-filter="all"]').classList.add("filter-active");

// Télécharger CSV (filtré)
downloadBtn.addEventListener("click", () => {
  const today = new Date();
  const startOfWeek = new Date(today);
  const dayOfWeek = today.getDay();
  const diff = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
  startOfWeek.setDate(today.getDate() - diff);
  startOfWeek.setHours(0, 0, 0, 0);

  let filteredSales = sales;

  if (currentFilter === "day") {
    filteredSales = sales.filter(sale => new Date(sale.date).toDateString() === today.toDateString());
  } else if (currentFilter === "week") {
    filteredSales = sales.filter(sale => {
      const d = new Date(sale.date);
      return d >= startOfWeek && d <= today;
    });
  } else if (currentFilter === "month") {
    filteredSales = sales.filter(sale => {
      const d = new Date(sale.date);
      return d.getMonth() === today.getMonth() && d.getFullYear() === today.getFullYear();
    });
  } else if (currentFilter === "year") {
    filteredSales = sales.filter(sale => new Date(sale.date).getFullYear() === today.getFullYear());
  }

  let csv = "Date,Produit,Quantité,Paiement,Total (€)\n";
  filteredSales.forEach(sale => {
    const row = [
      new Date(sale.date).toLocaleDateString('fr-FR'),
      `"${sale.title}"`,
      sale.qty,
      sale.payment,
      sale.price * sale.qty
    ];
    csv += row.join(",") + "\n";
  });

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `ventes_${currentFilter}.csv`;
  a.click();
  URL.revokeObjectURL(url);
});

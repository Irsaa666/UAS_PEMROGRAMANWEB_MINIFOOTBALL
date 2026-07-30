/* ============================================================
   Mini Football Manager - charts.js
   Chart.js rendering for Dashboard and Finance pages.
   Called after Chart.js CDN is loaded on the page.
   ============================================================ */

/**
 * Render the Dashboard Match Goals Bar Chart.
 * @param {string[]} labels  - e.g. ["vs Arsenal", "vs Chelsea"]
 * @param {number[]} gf      - Goals For per match
 * @param {number[]} ga      - Goals Against per match
 */
function renderMatchChart(labels, gf, ga) {
  const ctx = document.getElementById('matchChart');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Goals For',
          data: gf,
          backgroundColor: 'rgba(26, 107, 60, 0.8)',
          borderColor: '#1a6b3c',
          borderWidth: 2,
          borderRadius: 6,
        },
        {
          label: 'Goals Against',
          data: ga,
          backgroundColor: 'rgba(153, 27, 27, 0.7)',
          borderColor: '#991b1b',
          borderWidth: 2,
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: { font: { family: 'Inter', size: 12 }, padding: 16 },
        },
        tooltip: {
          callbacks: {
            title: (items) => items[0].label,
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { family: 'Inter', size: 11 } },
        },
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1, font: { family: 'Inter', size: 11 } },
          grid: { color: 'rgba(0,0,0,0.05)' },
        },
      },
    },
  });
}

/**
 * Render the Finance Monthly Income vs Expense Line Chart.
 * @param {string[]} labels   - e.g. ["2025-01", "2025-02"]
 * @param {number[]} income   - Monthly income totals
 * @param {number[]} expenses - Monthly expense totals
 */
function renderFinanceChart(labels, income, expenses) {
  const ctx = document.getElementById('financeChart');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Income',
          data: income,
          borderColor: '#1a6b3c',
          backgroundColor: 'rgba(26,107,60,0.08)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#1a6b3c',
          pointRadius: 5,
        },
        {
          label: 'Expenses',
          data: expenses,
          borderColor: '#991b1b',
          backgroundColor: 'rgba(153,27,27,0.07)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#991b1b',
          pointRadius: 5,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: { font: { family: 'Inter', size: 12 }, padding: 16 },
        },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.dataset.label}: $${ctx.parsed.y.toLocaleString()}`,
          },
        },
      },
      scales: {
        x: { grid: { display: false }, ticks: { font: { family: 'Inter', size: 11 } } },
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(0,0,0,0.05)' },
          ticks: {
            font: { family: 'Inter', size: 11 },
            callback: (v) => '$' + v.toLocaleString(),
          },
        },
      },
    },
  });
}

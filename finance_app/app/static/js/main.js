document.addEventListener('DOMContentLoaded', () => {
  const expenseForm = document.getElementById('expense-form');
  if (expenseForm) {
    expenseForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const form = new FormData(expenseForm);
      const payload = Object.fromEntries(form.entries());
      payload.amount = Number(payload.amount);
      const res = await fetch('/finance/expenses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      console.log('added', data);
    });
  }

  const planForm = document.getElementById('plan-form');
  if (planForm) {
    planForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const form = new FormData(planForm);
      const payload = { income: Number(form.get('income') || 0), goals: [] };
      const res = await fetch('/ai/generate-plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      const out = document.getElementById('plan-output');
      if (out) out.textContent = JSON.stringify(data, null, 2);
    });
  }
});






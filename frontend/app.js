const API_URL = "http://127.0.0.1:5001/api";

let token = null;
let currentTab = 'login';
let accountInfo = null;

// Tab Switching
function switchTab(tab) {
    currentTab = tab;
    document.querySelector('.tab.active').classList.remove('active');
    event.target.classList.add('active');
    document.getElementById('auth-btn').textContent = tab === 'login' ? 'Access Account' : 'Create Account';
    document.getElementById('auth-msg').textContent = '';
}

// Authentication (Login/Register)
document.getElementById('auth-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('auth-btn');
    const msg = document.getElementById('auth-msg');
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    btn.textContent = 'Processing...';
    btn.disabled = true;

    try {
        if (currentTab === 'register') {
            const res = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();
            
            if (!res.ok) throw new Error(data.error || 'Registration failed');
            
            // Auto login after register
            await login(username, password);
        } else {
            await login(username, password);
        }
    } catch (err) {
        msg.textContent = err.message;
        btn.textContent = currentTab === 'login' ? 'Access Account' : 'Create Account';
        btn.disabled = false;
    }
});

async function login(username, password) {
    const res = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    
    if (!res.ok) throw new Error(data.error || 'Login failed');
    
    token = data.access_token;
    document.getElementById('dash-username').textContent = username;
    
    // Switch Views
    document.getElementById('auth-view').classList.add('hidden');
    document.getElementById('dashboard-view').classList.remove('hidden');
    
    await loadDashboard();
}

function logout() {
    token = null;
    accountInfo = null;
    document.getElementById('auth-form').reset();
    document.getElementById('auth-btn').disabled = false;
    document.getElementById('auth-btn').textContent = 'Access Account';
    
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('auth-view').classList.remove('hidden');
}

// Account Logic
async function loadDashboard() {
    try {
        const res = await fetch(`${API_URL}/accounts/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const accounts = await res.json();
        
        if (accounts.length === 0) {
            document.getElementById('dash-balance').textContent = "$0.00";
            document.getElementById('no-acc-msg').classList.remove('hidden');
            document.querySelector('.actions-grid').classList.add('hidden');
            return;
        }

        document.getElementById('no-acc-msg').classList.add('hidden');
        document.querySelector('.actions-grid').classList.remove('hidden');
        
        accountInfo = accounts[0]; // Assume first account for simplicity
        updateDashboardUI();
        await loadTransactions();
    } catch (err) {
        console.error(err);
    }
}

async function createAccount() {
    try {
        await fetch(`${API_URL}/accounts/`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        await loadDashboard();
    } catch (err) {
        alert("Failed to create account");
    }
}

function updateDashboardUI() {
    document.getElementById('dash-acc-num').textContent = accountInfo.account_number;
    document.getElementById('dash-balance').textContent = `$${parseFloat(accountInfo.balance).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
}

// Transactions
async function loadTransactions() {
    try {
        const res = await fetch(`${API_URL}/transactions/history/${accountInfo.account_id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const txs = await res.json();
        
        const list = document.getElementById('tx-list');
        list.innerHTML = '';
        
        if (txs.length === 0) {
            list.innerHTML = '<p style="color:var(--text-muted); font-size: 0.9rem;">No recent transactions.</p>';
            return;
        }

        // Reverse to show newest first
        txs.reverse().forEach(tx => {
            const isPositive = tx.type === 'DEPOSIT' || tx.type === 'TRANSFER_IN';
            const sign = isPositive ? '+' : '-';
            const colorClass = isPositive ? 'tx-pos' : 'tx-neg';
            const date = new Date(tx.timestamp).toLocaleString();
            
            list.innerHTML += `
                <div class="tx-item">
                    <div class="tx-info">
                        <span class="tx-type">${tx.description}</span>
                        <span class="tx-date">${date}</span>
                    </div>
                    <span class="tx-amount ${colorClass}">${sign}$${parseFloat(tx.amount).toLocaleString('en-US', {minimumFractionDigits: 2})}</span>
                </div>
            `;
        });
    } catch (err) {
        console.error("Failed to load history");
    }
}

async function submitTransaction(type) {
    const amountInput = document.getElementById(`${type}-amount`);
    const amount = parseFloat(amountInput.value);
    
    if (!amount || amount <= 0) {
        alert("Please enter a valid amount");
        return;
    }

    let payload = { account_id: accountInfo.account_id, amount: amount };
    let endpoint = `/transactions/${type}`;

    if (type === 'transfer') {
        const toAcc = document.getElementById('transfer-to').value;
        if (!toAcc) {
            alert("Please provide recipient account number");
            return;
        }
        // The API expects 'from_account_id' instead of 'account_id' for transfers
        payload = { 
            from_account_id: accountInfo.account_id, 
            to_account_number: toAcc, 
            amount: amount 
        };
    }

    try {
        const res = await fetch(API_URL + endpoint, {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Transaction failed");
        
        // Refresh balance & history
        await loadDashboard();
        closeModal(`${type}-modal`);
        amountInput.value = '';
        if (type === 'transfer') document.getElementById('transfer-to').value = '';
        
    } catch (err) {
        alert(err.message);
    }
}

// Modal logic
function openModal(id) { document.getElementById(id).classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id).classList.add('hidden'); }

// AXIOM CALC — Main JS with localStorage persistence

const expressionPreview = document.getElementById('expression-preview');
const resultDisplay = document.getElementById('result-display');
const displayMeta = document.getElementById('display-meta');
const historyList = document.getElementById('history-list');
const sciRow = document.getElementById('sci-row');
const btnGrid = document.getElementById('btn-grid');

let expression = '';
let history = [];
let activeConvKey = null;
let sciMode = false;

// ===================== STORAGE =====================
const STORAGE_KEYS = {
    HISTORY: 'axiom_calc_history',
    MODE: 'axiom_calc_mode'
};

function saveHistory() {
    try {
        localStorage.setItem(STORAGE_KEYS.HISTORY, JSON.stringify(history.slice(0, 100)));
    } catch (e) {
        console.warn('Failed to save history to localStorage:', e);
    }
}

function loadHistory() {
    try {
        const stored = localStorage.getItem(STORAGE_KEYS.HISTORY);
        if (stored) {
            history = JSON.parse(stored);
        }
    } catch (e) {
        console.warn('Failed to load history from localStorage:', e);
        history = [];
    }
}

function saveMode() {
    try {
        localStorage.setItem(STORAGE_KEYS.MODE, sciMode ? 'sci' : 'basic');
    } catch (e) {
        console.warn('Failed to save mode to localStorage:', e);
    }
}

function loadMode() {
    try {
        const stored = localStorage.getItem(STORAGE_KEYS.MODE);
        if (stored === 'sci') {
            sciMode = true;
            document.querySelectorAll('.mode-btn').forEach(btn => {
                if (btn.dataset.mode === 'sci') {
                    btn.classList.add('active');
                    sciRow.classList.add('visible');
                } else {
                    btn.classList.remove('active');
                }
            });
        }
    } catch (e) {
        console.warn('Failed to load mode from localStorage:', e);
    }
}

// ===================== DISPLAY =====================
function updateDisplay() {
    expressionPreview.textContent = expression || '_';
    expressionPreview.style.opacity = expression ? '0.8' : '0.3';
}

function setResult(val, isError = false) {
    resultDisplay.textContent = val;
    resultDisplay.className = 'result-display' + (isError ? ' error' : '');
    if (!isError) {
        resultDisplay.classList.add('flash');
        setTimeout(() => resultDisplay.classList.remove('flash'), 400);
    }
}

function setMeta(txt) {
    displayMeta.textContent = txt;
}

// ===================== EXPRESSION OPS =====================
function appendToExpr(val) {
    // Map display chars to real operators
    const map = { '÷': '/', '×': '*', '−': '-' };
    expression += (map[val] !== undefined ? map[val] : val);
    resultDisplay.textContent = expression.length ? evaluateLive() || resultDisplay.textContent : '0';
    updateDisplay();
}

function clearExpr() {
    expression = '';
    setResult('0');
    setMeta('');
    updateDisplay();
}

function backspace() {
    expression = expression.slice(0, -1);
    updateDisplay();
    resultDisplay.textContent = expression ? evaluateLive() || resultDisplay.textContent : '0';
}

function copyResult() {
    const result = resultDisplay.textContent;
    if (result && result !== '0') {
        navigator.clipboard.writeText(result).then(() => {
            setMeta('✓ Copied to clipboard');
            setTimeout(() => setMeta(''), 1500);
        }).catch(err => {
            console.warn('Failed to copy:', err);
            setMeta('Failed to copy');
        });
    }
}

// Live preview (no side effects)
function evaluateLive() {
    try {
        let e = expression
            .replace(/\^/g, '**')
            .replace(/÷/g, '/')
            .replace(/×/g, '*');
        // Don't eval incomplete expressions
        if (/[\+\-\*\/\^]$/.test(e) || /\($/.test(e)) return null;
        const r = Function('"use strict"; return (' + e + ')')();
        if (typeof r === 'number' && isFinite(r)) {
            return r % 1 === 0 ? String(r) : parseFloat(r.toFixed(8)).toString();
        }
    } catch { }
    return null;
}

// ===================== CALCULATE =====================
async function calculate() {
    if (!expression.trim()) return;

    try {
        const resp = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression })
        });
        const data = await resp.json();

        if (!resp.ok || data.error) {
            setResult(data.error || 'Calculation error', true);
            setMeta('');
            console.warn('Calculation error:', data.error);
        } else {
            setResult(data.result);
            setMeta(`= ${data.expression}`);
            addToHistory(data.expression, data.result);
            expression = data.result;
            updateDisplay();
        }
    } catch (e) {
        console.error('Network error:', e);
        setResult('CONNECTION ERROR', true);
        setMeta('Failed to reach server');
    }
}

// ===================== HISTORY =====================
function addToHistory(expr, result) {
    const now = new Date();
    const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    history.unshift({ expr, result, time });
    if (history.length > 100) history.pop();
    renderHistory();
    saveHistory();
}

function renderHistory() {
    if (history.length === 0) {
        historyList.innerHTML = '<div class="history-empty">No calculations yet.<br>Start computing to see your history.</div>';
        return;
    }
    historyList.innerHTML = history.map((h, i) => `
    <div class="history-item" onclick="recallHistory(${i})" role="button" tabindex="0" aria-label="Recall calculation: ${h.expr} = ${h.result}">
      <div class="hist-expr">${escHtml(h.expr)}</div>
      <div class="hist-result">${escHtml(h.result)}</div>
      <div class="hist-time">${h.time}</div>
    </div>
  `).join('');
}

function recallHistory(i) {
    const h = history[i];
    expression = h.result;
    updateDisplay();
    setResult(h.result);
    setMeta(`↑ recalled: ${h.expr}`);
    // Switch to calc tab
    document.querySelector('[data-tab="calc"]').click();
}

function escHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function clearHistoryConfirm() {
    if (confirm('Are you sure you want to clear all calculation history?')) {
        history = [];
        renderHistory();
        saveHistory();
        setMeta('History cleared');
    }
}

const clearHistBtn = document.getElementById('clear-history');
if (clearHistBtn) {
    clearHistBtn.addEventListener('click', clearHistoryConfirm);
}

// ===================== TABS =====================
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    });
});

// ===================== MODE SWITCH =====================
document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        sciMode = btn.dataset.mode === 'sci';
        sciRow.classList.toggle('visible', sciMode);
        saveMode();
    });
});

// ===================== BUTTON CLICKS =====================
btnGrid.addEventListener('click', e => {
    const btn = e.target.closest('.calc-btn');
    if (!btn) return;

    const action = btn.dataset.action;
    const val = btn.dataset.val;

    if (action === 'clear') clearExpr();
    else if (action === 'backspace') backspace();
    else if (action === 'equals') calculate();
    else if (action === 'copy') copyResult();
    else if (val !== undefined) appendToExpr(val);
});

// ===================== KEYBOARD =====================
document.addEventListener('keydown', e => {
    // Only active on calc tab
    if (!document.getElementById('tab-calc').classList.contains('active')) return;

    const key = e.key;
    if (key >= '0' && key <= '9') appendToExpr(key);
    else if (key === '.') appendToExpr('.');
    else if (key === '+') appendToExpr('+');
    else if (key === '-') appendToExpr('-');
    else if (key === '*') appendToExpr('×');
    else if (key === '/') { e.preventDefault(); appendToExpr('÷'); }
    else if (key === '(') appendToExpr('(');
    else if (key === ')') appendToExpr(')');
    else if (key === '^') appendToExpr('^');
    else if (key === '%') appendToExpr('%');
    else if (key === 'Enter') { e.preventDefault(); calculate(); }
    else if (key === 'Backspace') backspace();
    else if (key === 'Escape') clearExpr();
    else if (key === 'c' || key === 'C') copyResult();
});

// ===================== CONVERTER =====================
const convValueInput = document.getElementById('conv-value');
const convResult = document.getElementById('conv-result');
const convLabel = document.getElementById('conv-label');

async function runConversion() {
    const val = convValueInput.value;
    if (!activeConvKey || val === '') { convResult.textContent = '—'; return; }

    try {
        const resp = await fetch('/convert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversion: activeConvKey, value: parseFloat(val) })
        });
        const data = await resp.json();
        if (!resp.ok || data.error) {
            convResult.textContent = 'ERR';
            console.warn('Conversion error:', data.error);
            return;
        }
        convResult.textContent = data.result;
        convLabel.textContent = data.label;
    } catch (e) {
        console.error('Conversion error:', e);
        convResult.textContent = 'ERR';
    }
}

if (convValueInput) {
    convValueInput.addEventListener('input', runConversion);
}

document.querySelectorAll('.conv-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.conv-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeConvKey = btn.dataset.key;
        runConversion();
    });
});

// ===================== INIT =====================
loadMode();
loadHistory();
updateDisplay();
renderHistory();

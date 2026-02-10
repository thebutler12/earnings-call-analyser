// Main application JavaScript

// State
let currentTranscripts = [];
let currentAnalysis = null;

// DOM Elements
const transcriptSelect = document.getElementById('transcriptSelect');
const customTranscript = document.getElementById('customTranscript');
const companyName = document.getElementById('companyName');
const quarter = document.getElementById('quarter');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const quickScanResult = document.getElementById('quickScanResult');

// Sidebar elements
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const sidebarClose = document.getElementById('sidebarClose');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const rawResponse = document.getElementById('rawResponse');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTranscripts();
    setupEventListeners();
    checkHealth();
});

// Load available transcripts
async function loadTranscripts() {
    try {
        const response = await fetch('/api/transcripts');
        const data = await response.json();
        
        if (data.success) {
            currentTranscripts = data.transcripts;
            populateTranscriptSelect(data.transcripts);
        }
    } catch (error) {
        console.error('Error loading transcripts:', error);
    }
}

// Populate transcript dropdown
function populateTranscriptSelect(transcripts) {
    transcriptSelect.innerHTML = '<option value="">Choose a sample transcript...</option>';
    
    transcripts.forEach(t => {
        const option = document.createElement('option');
        option.value = t.key;
        option.textContent = `${t.company} - ${t.quarter} (${t.date})`;
        transcriptSelect.appendChild(option);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Transcript selection
    transcriptSelect.addEventListener('change', handleTranscriptSelect);
    
    // Analyze button
    analyzeBtn.addEventListener('click', handleAnalyze);
    
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });
    
    // Sidebar controls
    sidebarToggle.addEventListener('click', openSidebar);
    sidebarClose.addEventListener('click', closeSidebar);
    sidebarOverlay.addEventListener('click', closeSidebar);
    
    // Close sidebar on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sidebar.classList.contains('open')) {
            closeSidebar();
        }
    });
}

// Handle transcript selection
async function handleTranscriptSelect(e) {
    const key = e.target.value;
    
    if (!key) {
        customTranscript.value = '';
        companyName.value = '';
        quarter.value = '';
        return;
    }
    
    try {
        const response = await fetch(`/api/transcript/${key}`);
        const data = await response.json();
        
        if (data.success) {
            const t = data.transcript;
            customTranscript.value = t.transcript;
            companyName.value = t.company;
            quarter.value = t.quarter;
        }
    } catch (error) {
        console.error('Error loading transcript:', error);
        showError('Failed to load transcript');
    }
}

// Handle analyze button
async function handleAnalyze() {
    const transcript = customTranscript.value.trim();
    const company = companyName.value.trim() || 'Unknown Company';
    const qtr = quarter.value.trim() || 'Unknown Quarter';
    
    if (!transcript) {
        showError('Please select or paste a transcript');
        return;
    }
    
    // Hide previous results and errors
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    quickScanResult.style.display = 'none';
    
    // Show loading state
    setLoading(true);
    
    try {
        // Perform analysis
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                transcript_text: transcript,
                company_name: company,
                quarter: qtr
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentAnalysis = data;
            displayResults(data);
            updateRawResponse(data.raw_anthropic_response);
        } else {
            showError(data.error || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Error during analysis:', error);
        showError('Failed to analyze transcript. Please check your API key and try again.');
    } finally {
        setLoading(false);
    }
}

// Display analysis results
function displayResults(data) {
    const { analysis, stats, highlighted_transcript } = data;
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Update stats
    document.getElementById('confidenceScore').textContent = 
        analysis.confidence_score || '--';
    document.getElementById('riskLevel').textContent = 
        analysis.risk_level || '--';
    document.getElementById('healthScore').textContent = 
        Math.round(stats.health_score) || '--';
    
    // Filter out N/A entries from question dodging
    const validQuestionDodging = (analysis.question_dodging || []).filter(item => 
        item && 
        item.question && 
        item.answer && 
        item.analysis &&
        item.question.toLowerCase() !== 'n/a' &&
        item.answer.toLowerCase() !== 'n/a' &&
        item.analysis.toLowerCase() !== 'n/a'
    );
    
    // Update counts in tabs
    document.getElementById('hedgingCount').textContent = 
        (analysis.hedging_language || []).length;
    document.getElementById('concernsCount').textContent = 
        (analysis.key_concerns || []).length;
    document.getElementById('dodgingCount').textContent = 
        validQuestionDodging.length;
    
    // Overall assessment
    document.getElementById('overallAssessment').textContent = 
        analysis.overall_assessment || 'No assessment available';
    
    // Populate findings
    displayHedgingLanguage(analysis.hedging_language || []);
    displayKeyConcerns(analysis.key_concerns || []);
    displayQuestionDodging(validQuestionDodging);
    displayPositiveSignals(analysis.positive_signals || []);
    displayHighlightedTranscript(highlighted_transcript);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display hedging language
function displayHedgingLanguage(items) {
    const container = document.getElementById('hedgingList');
    
    if (items.length === 0) {
        container.innerHTML = '<p style="color: var(--text-secondary);">No significant hedging language detected. This is a positive sign!</p>';
        return;
    }
    
    // Sort items by severity: High -> Medium -> Low
    const severityOrder = { 'high': 3, 'medium': 2, 'low': 1 };
    const sortedItems = [...items].sort((a, b) => {
        const severityA = severityOrder[a.severity?.toLowerCase()] || 2; // Default to medium
        const severityB = severityOrder[b.severity?.toLowerCase()] || 2; // Default to medium
        return severityB - severityA; // Descending order (high to low)
    });
    
    container.innerHTML = sortedItems.map(item => `
        <div class="finding-item ${item.severity || 'medium'}">
            <div class="finding-header">
                <span><strong>Phrase:</strong> "${item.phrase}"</span>
                <span class="severity-badge ${item.severity || 'medium'}">${(item.severity || 'medium').toUpperCase()}</span>
            </div>
            <div class="finding-context">${escapeHtml(item.context)}</div>
            <div class="finding-reason">${item.reason || 'May indicate uncertainty or lack of commitment'}</div>
        </div>
    `).join('');
}

// Display key concerns
function displayKeyConcerns(items) {
    const container = document.getElementById('concernsList');
    
    if (items.length === 0) {
        container.innerHTML = '<p style="color: var(--text-secondary);">No major concerns identified. Management appears transparent.</p>';
        return;
    }
    
    container.innerHTML = items.map(item => `
        <div class="concern-card">
            <div class="concern-title">⚠️ ${item.concern}</div>
            <p>${item.description}</p>
            ${item.evidence ? `<div class="concern-evidence">"${escapeHtml(item.evidence)}"</div>` : ''}
            <p style="margin-top: 10px; color: var(--text-secondary);"><strong>Potential Impact:</strong> ${item.impact}</p>
        </div>
    `).join('');
}

// Display question dodging
function displayQuestionDodging(items) {
    const container = document.getElementById('dodgingList');
    
    if (items.length === 0) {
        container.innerHTML = '<p style="color: var(--text-secondary);">No obvious question dodging detected. Management appears to answer directly.</p>';
        return;
    }
    
    container.innerHTML = items.map(item => `
        <div class="finding-item high">
            <div class="finding-header">
                <span><strong>Question:</strong></span>
            </div>
            <div class="finding-context">${escapeHtml(item.question)}</div>
            <div style="margin: 10px 0;"><strong>Response:</strong></div>
            <div class="finding-context">${escapeHtml(item.answer)}</div>
            <div class="finding-reason"><strong>Analysis:</strong> ${item.analysis}</div>
        </div>
    `).join('');
}

// Display positive signals
function displayPositiveSignals(items) {
    const container = document.getElementById('positiveList');
    
    if (items.length === 0) {
        container.innerHTML = '<p style="color: var(--text-secondary);">No specific positive signals highlighted, but absence of red flags is itself positive.</p>';
        return;
    }
    
    container.innerHTML = items.map(item => `
        <div class="positive-item">
            ✅ ${item}
        </div>
    `).join('');
}

// Display highlighted transcript
function displayHighlightedTranscript(html) {
    const container = document.getElementById('highlightedTranscript');
    container.innerHTML = html || 'No transcript available';
}

// Switch tabs
function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    
    // Update panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.toggle('active', pane.id === `${tabName}-tab`);
    });
}

// Show error
function showError(message) {
    errorSection.style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Set loading state
function setLoading(isLoading) {
    analyzeBtn.disabled = isLoading;
    
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');
    
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Check API health
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (!data.analyzer_ready) {
            showError('⚠️ API key not configured. Please add your ANTHROPIC_API_KEY to .env file.');
        }
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

// Utility: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Sidebar Functions
function openSidebar() {
    sidebar.classList.add('open');
    sidebarOverlay.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeSidebar() {
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('show');
    document.body.style.overflow = '';
}

function updateRawResponse(responseData) {
    if (!responseData) {
        rawResponse.innerHTML = '<p class="placeholder">No raw response data available.</p>';
        return;
    }
    
    // Create formatted display
    const timestamp = new Date().toLocaleString();
    const content = typeof responseData === 'string' ? responseData : JSON.stringify(responseData, null, 2);
    
    rawResponse.innerHTML = `
        <div class="response-meta">
            <h4>Response Metadata</h4>
            <p><strong>Timestamp:</strong> ${timestamp}</p>
            <p><strong>Model:</strong> Claude 3 Haiku</p>
            <p><strong>Length:</strong> ${content.length} characters</p>
        </div>
        <div class="response-content">
            ${escapeHtml(content)}
        </div>
    `;
    
    // Show toggle button if hidden
    sidebarToggle.style.display = 'block';
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        displayResults,
        switchTab,
        escapeHtml
    };
}

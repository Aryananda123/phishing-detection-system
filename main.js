document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('scan-form');
    const urlInput = document.getElementById('url-input');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.spinner');
    const scanBtn = document.getElementById('scan-btn');
    const resultsContainer = document.getElementById('results-container');
    
    // Result elements
    const riskBadge = document.getElementById('risk-badge');
    const riskScoreValue = document.getElementById('risk-score-value');
    const riskProgress = document.getElementById('risk-progress');
    const featuresList = document.getElementById('features-list');

    // Feature formatting helpers
    const featureLabels = {
        'url_length': 'URL Length',
        'domain_length': 'Domain Length',
        'has_ip': 'IP Address Used',
        'count_at': "'@' Symbol Count",
        'count_dash_domain': "'-' in Domain",
        'has_shortener': 'URL Shortener',
        'https_in_domain': "'https' in Domain",
        'keyword_count': 'Suspicious Keywords'
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        if (!url) return;

        // UI Loading state
        setLoadingState(true);
        resultsContainer.classList.add('hidden');

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to analyze URL');
            }

            displayResults(data);

        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            setLoadingState(false);
        }
    });

    function setLoadingState(isLoading) {
        if (isLoading) {
            btnText.classList.add('hidden');
            spinner.classList.remove('hidden');
            scanBtn.disabled = true;
        } else {
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            scanBtn.disabled = false;
        }
    }

    function displayResults(data) {
        // Show container
        resultsContainer.classList.remove('hidden');

        // Update Badge
        riskBadge.className = 'badge';
        if (data.is_phishing) {
            riskBadge.textContent = 'Phishing Detected';
            riskBadge.classList.add('phishing');
        } else {
            riskBadge.textContent = 'Safe Website';
            riskBadge.classList.add('safe');
        }

        // Update Risk Meter
        const score = data.risk_score;
        riskScoreValue.textContent = `${score.toFixed(1)}%`;
        
        // Reset progress bar width to 0 then animate to value
        riskProgress.style.width = '0%';
        
        // Use timeout to allow CSS transition to trigger
        setTimeout(() => {
            riskProgress.style.width = `${score}%`;
            
            // Set color based on risk
            if (score < 30) {
                riskProgress.style.backgroundColor = 'var(--success)';
            } else if (score < 70) {
                riskProgress.style.backgroundColor = 'var(--warning)';
            } else {
                riskProgress.style.backgroundColor = 'var(--danger)';
            }
        }, 50);

        // Populate Features
        featuresList.innerHTML = '';
        const features = data.features_analyzed;
        
        for (const [key, value] of Object.entries(features)) {
            const label = featureLabels[key] || key;
            const li = document.createElement('li');
            
            // Highlight suspicious feature values
            let valueClass = '';
            let displayValue = value;
            
            if (key === 'has_ip' && value === 1) { displayValue = 'Yes'; valueClass = 'high'; }
            if (key === 'has_ip' && value === 0) displayValue = 'No';
            
            if (key === 'has_shortener' && value === 1) { displayValue = 'Yes'; valueClass = 'high'; }
            if (key === 'has_shortener' && value === 0) displayValue = 'No';
            
            if (key === 'https_in_domain' && value === 1) { displayValue = 'Yes'; valueClass = 'high'; }
            if (key === 'https_in_domain' && value === 0) displayValue = 'No';
            
            if (key === 'count_at' && value > 0) valueClass = 'high';
            if (key === 'keyword_count' && value > 0) valueClass = 'high';
            if (key === 'url_length' && value > 75) valueClass = 'high';

            li.innerHTML = `
                <span class="feature-name">${label}</span>
                <span class="feature-value ${valueClass}">${displayValue}</span>
            `;
            featuresList.appendChild(li);
        }
    }
});

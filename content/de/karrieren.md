---
title: Karrieren
---

{{< brick_wide >}}

# Karrieren
{{< breadcrumbs >}}

{{< /brick_wide >}}

{{< brick_jobs >}}

{{< /brick_jobs >}}

<p class="application-note">📝 <strong>Hinweis:</strong> Nach dem Klick auf "Jetzt bewerben" öffnet sich Ihr E-Mail-Programm. Bitte senden Sie uns Ihren Lebenslauf und ein Anschreiben zu.</p>

<style>
.jobs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
    gap: 30px;
    margin: 30px 0;
}

.job-box {
    background: #f8f9fa;
    border: 2px solid #e9ecef;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.job-box:hover {
    border-color: #ffc107;
    box-shadow: 0 6px 12px rgba(255, 193, 7, 0.15);
    transform: translateY(-2px);
}

.job-box h3 {
    color: #2c3e50;
    margin-bottom: 15px;
    border-bottom: 2px solid #ffc107;
    padding-bottom: 10px;
    font-size: 1.4em;
    font-weight: 600;
    text-align: center;
}

.job-box .job-details {
    background: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
}

.job-box .job-detail-item {
    text-align: center;
    flex: 1;
    min-width: 120px;
}

.job-box .job-detail-label {
    font-size: 0.85em;
    font-weight: 600;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 5px;
    display: block;
}

.job-box .job-detail-value {
    font-size: 0.95em;
    font-weight: 500;
    color: #2c3e50;
    display: block;
}

.job-box p {
    margin-bottom: 15px;
    line-height: 1.6;
}

.job-box ul {
    margin-bottom: 20px;
}

.job-box li {
    margin-bottom: 8px;
}

.job-apply {
    text-align: center;
    margin-top: auto;
    padding-top: 20px;
    border-top: 1px solid #dee2e6;
}

.job-apply .button {
    display: inline-block;
    padding: 12px 30px;
    font-size: 16px;
    font-weight: 600;
    text-decoration: none;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.job-apply .button.primary {
    background: #ffc107;
    color: #2c3e50;
    border: 2px solid #ffc107;
    border-radius: 8px;
}

.job-apply .button.primary:hover {
    background: #e0a800;
    border-color: #e0a800;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(255, 193, 7, 0.3);
}

.application-note {
    text-align: center;
    color: #6c757d;
    font-size: 0.95em;
    margin: 30px 0;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #ffc107;
}

@media (max-width: 768px) {
    .jobs-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .job-box {
        padding: 20px;
    }
    
    .job-box .job-details {
        flex-direction: column;
        gap: 15px;
    }
    
    .job-box .job-detail-item {
        min-width: auto;
    }
}
</style>
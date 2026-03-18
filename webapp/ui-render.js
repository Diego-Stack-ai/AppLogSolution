/**
 * Gestione rendering UI dinamica per liste viaggi e componenti visualizzazione.
 */
export function renderTripList(trips, containerId, isAdmin = false) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '';
    
    if (trips.length === 0) {
        const emptyState = document.getElementById('emptyState');
        if (emptyState) emptyState.style.display = 'block';
        return;
    } else {
        const emptyState = document.getElementById('emptyState');
        if (emptyState) emptyState.style.display = 'none';
    }

    trips.forEach(r => {
        const card = document.createElement('div');
        card.className = 'data-card';
        
        // Formattazione data
        const dataStr = r.data ? new Date(r.data).toLocaleDateString('it-IT') : '-';
        
        card.innerHTML = `
            <div class="card-header">
                <div>
                    <span style="font-weight: 700; color: var(--primary); font-size: 16px;">${dataStr}</span>
                    <span style="margin-left: 12px; color: var(--text-muted); font-size: 13px;">${r.autista || 'Sconosciuto'}</span>
                </div>
                <div style="display:flex; align-items:center; gap:12px;">
                    <span class="status-badge badge-success">${r.automezzo}</span>
                    ${(isAdmin) ? `<button onclick="confirmDeleteTrip('${r.id}')" style="border:none; background:none; color: #f87171; cursor:pointer; display:flex;" title="Elimina Viaggio"><span class="material-icons-round" style="font-size:20px;">delete_outline</span></button>` : ''}
                </div>
            </div>
            <div class="card-grid">
                <div class="data-item">
                    <span class="data-label">Cliente</span>
                    <span class="data-value">${(r.cliente || '-').toUpperCase()}</span>
                </div>
                <div class="data-item">
                    <span class="data-label">Km Percorsi</span>
                    <span class="data-value">${r.delta_km || '-'} km</span>
                </div>
                <div class="data-item">
                    <span class="data-label">Ore Totali</span>
                    <span class="data-value">${r.ore_totali || '-'}h</span>
                </div>
                <div class="data-item">
                    <span class="data-label">Viaggio</span>
                    <span class="data-value" style="font-size:11px;">${r.viaggio || '-'}</span>
                </div>
            </div>
            ${r.nota ? `
                <div style="margin-top: 16px; padding-top: 12px; border-top: 1px dashed #e2e8f0;">
                    <span class="data-label">Note</span>
                    <p style="font-size: 13px; color: #475569; margin-top: 4px;">${r.nota}</p>
                </div>
            ` : ''}
            <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid #f1f5f9; display: flex; gap: 12px;">
                <button class="btn-primary" onclick="loadAndShowLogs('${r.id}')" 
                    style="padding: 8px 12px; font-size: 12px; height: auto; background: #f8fafc; color: #475569; border: 1px solid #e2e8f0; box-shadow: none;">
                    <span class="material-icons-round" style="font-size: 16px;">list_alt</span> Log GPS
                </button>
                <button class="btn-primary" onclick="loadAndShowPath('${r.id}')" 
                    style="padding: 8px 12px; font-size: 12px; height: auto; background: #f8fafc; color: #475569; border: 1px solid #e2e8f0; box-shadow: none;">
                    <span class="material-icons-round" style="font-size: 16px;">map</span> Percorso
                </button>
            </div>
        `;
        container.appendChild(card);
    });
}

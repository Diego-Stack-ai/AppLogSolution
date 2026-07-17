
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    


document.addEventListener("DOMContentLoaded", () => {
        let mezzi = (window.appData && window.appData.lista_mezzi && window.appData.lista_mezzi.length > 0) ? window.appData.lista_mezzi : [];

        let editIndex = -1;
        window.storico_corrente = [];
        let editStoricoIndex = -1;
        
        let viewMode = localStorage.getItem('ls_mezzi_view_mode') || 'list';

        window.setViewMode = function(mode) {
            viewMode = mode;
            localStorage.setItem('ls_mezzi_view_mode', mode);
            const btnList = document.getElementById('btnViewList');
            const btnGrid = document.getElementById('btnViewGrid');
            const btnHist = document.getElementById('btnViewHistory');
            
            const activeStyle = { bg: 'white', col: 'var(--primary)', shadow: '0 1px 3px rgba(0,0,0,0.1)' };
            const inactiveStyle = { bg: 'transparent', col: '#64748b', shadow: 'none' };
            
            btnList.style.background = mode === 'list' ? activeStyle.bg : inactiveStyle.bg;
            btnList.style.color = mode === 'list' ? activeStyle.col : inactiveStyle.col;
            btnList.style.boxShadow = mode === 'list' ? activeStyle.shadow : inactiveStyle.shadow;
            
            btnGrid.style.background = mode === 'grid' ? activeStyle.bg : inactiveStyle.bg;
            btnGrid.style.color = mode === 'grid' ? activeStyle.col : inactiveStyle.col;
            btnGrid.style.boxShadow = mode === 'grid' ? activeStyle.shadow : inactiveStyle.shadow;

            if (btnHist) {
                btnHist.style.background = mode === 'history' ? activeStyle.bg : inactiveStyle.bg;
                btnHist.style.color = mode === 'history' ? activeStyle.col : inactiveStyle.col;
                btnHist.style.boxShadow = mode === 'history' ? activeStyle.shadow : inactiveStyle.shadow;
            }

            if (typeof window.renderLista === "function") window.renderLista();
        };

        // Initialize button UI state
        window.setViewMode(viewMode);

        // Campi form
        const targaInput = document.getElementById('targaInput');
        const modelloInput = document.getElementById('modelloInput');
        const patenteInput = document.getElementById('patenteInput');
        const attivoInput = document.getElementById('attivoInput');
        const tipologiaInput = document.getElementById('tipologiaInput');
        const proprietarioInput = document.getElementById('proprietarioInput');
        
        const assicInput = document.getElementById('assicurazioneInput');
        const scAssicInput = document.getElementById('scadenzaAssicurazioneInput');
        const scRevInput = document.getElementById('scadenzaRevisioneInput');
        const scAtpInput = document.getElementById('scadenzaATPInput');
        const scTachInput = document.getElementById('scadenzaTachigrafoInput');
        const immInput = document.getElementById('immatricolazioneInput');
        
        const tesseraInput = document.getElementById('tesseraCarburanteInput');
        const pinInput = document.getElementById('pinTesseraInput');
        const noteInput = document.getElementById('noteInput');

        const btnSalvaMezzo = document.getElementById('btnSalvaMezzo');

        // Helpers Scadenze
        function formattaData(dateStr) {
            if(!dateStr) return 'N/D';
            const d = new Date(dateStr);
            if(isNaN(d)) return dateStr;
            return d.toLocaleDateString('it-IT');
        }

        function getBadgeColor(dateStr) {
            if(!dateStr) return 'badge-gray';
            const d = new Date(dateStr);
            if(isNaN(d)) return 'badge-gray';
            const diffDays = Math.ceil((d - new Date()) / (1000 * 60 * 60 * 24));
            if (diffDays < 0) return 'badge-red';
            if (diffDays <= 30) return 'badge-yellow';
            return 'badge-green';
        }

        window.toggleDetails = function(idx) {
            const el = document.getElementById('mezzo-details-' + idx);
            if (el) {
                const isOpening = el.style.display === 'none';
                el.style.display = isOpening ? 'block' : 'none';
                
                if (isOpening && window.innerWidth > 768) {
                    renderPDFThumbnails(idx);
                }
            }
        };

        window.renderPDFThumbnails = async function(mezzoIdx) {
            const el = document.getElementById('mezzo-details-' + mezzoIdx);
            if (!el) return;
            const canvases = el.querySelectorAll('.pdf-thumbnail-canvas');
            
            for (let i = 0; i < canvases.length; i++) {
                const canvas = canvases[i];
                if (canvas.dataset.rendered === 'true') continue;
                
                const url = canvas.dataset.pdfUrl;
                const iconContainer = document.getElementById(canvas.dataset.iconId);
                
                try {
                    const loadingTask = pdfjsLib.getDocument(url);
                    const pdf = await loadingTask.promise;
                    const page = await pdf.getPage(1);
                    
                    const viewport = page.getViewport({ scale: 1.0 });
                    const scale = 120 / viewport.width;
                    const scaledViewport = page.getViewport({ scale: scale });
                    
                    canvas.height = scaledViewport.height;
                    canvas.width = scaledViewport.width;
                    
                    const renderContext = {
                        canvasContext: canvas.getContext('2d'),
                        viewport: scaledViewport
                    };
                    
                    await page.render(renderContext).promise;
                    
                    if (iconContainer) iconContainer.style.display = 'none';
                    canvas.style.display = 'block';
                    canvas.dataset.rendered = 'true';
                } catch (error) {
                    console.error('Error rendering PDF thumbnail', error);
                }
            }
        };

        window.renderLista = function () {
            let currentMezzi = (window.appData && window.appData.lista_mezzi) ? window.appData.lista_mezzi : [];
            const isFornitore = window.appData && window.appData.currentUser && window.appData.currentUser.ruolo === 'fornitore';
            let permFornitoreRaw = window.appData && window.appData.permessiDashboard && window.appData.permessiDashboard['gestione_mezzi'] && window.appData.permessiDashboard['gestione_mezzi']['fornitore'] ? window.appData.permessiDashboard['gestione_mezzi']['fornitore'] : 'none';
            let permFornitore = permFornitoreRaw;
            let advModules = null;
            if (typeof permFornitoreRaw === 'object' && permFornitoreRaw.access === 'advanced') {
                permFornitore = 'advanced';
                advModules = permFornitoreRaw.modules || {};
            }

            const getModPerm = (modName) => {
                if (!isFornitore) return 'write'; // Default x admin/impiegata (gestito altrove)
                if (permFornitore === 'write') return 'write';
                if (permFornitore === 'read' || permFornitore === 'read_docs') return 'read';
                if (permFornitore === 'advanced' && advModules) return advModules[modName] || 'none';
                return 'none';
            };

            const permAnagrafica = getModPerm('anagrafica');
            const permScadenze = getModPerm('scadenze');
            const permCarburante = getModPerm('carburante');
            const permManutenzioni = getModPerm('manutenzioni');
            const permMedia = getModPerm('media');
            
            // Nascondi pulsante aggiungi se fornitore
            const addBtn = document.querySelector('button[onclick="apriNuovoMezzo()"]');
            if (isFornitore && addBtn) addBtn.style.display = 'none';

            if (viewMode === 'history') {
                currentMezzi = currentMezzi.filter(m => m.attivo === false || (m.stato && m.stato.toLowerCase() !== 'attivo'));
            } else {
                currentMezzi = currentMezzi.filter(m => m.attivo !== false && (!m.stato || m.stato.toLowerCase() === 'attivo'));
            }
            
            mezzi = currentMezzi;

            const listaDiv = document.getElementById('listaMezzi');
            listaDiv.innerHTML = '';
            
            // Definisco le categorie
            const categorie = [
                { id: 'patenteB', titolo: 'Mezzi Patente B' },
                { id: 'patenteC', titolo: 'Mezzi Patente C' },
                { id: 'treAssi', titolo: 'Mezzi Tre Assi' },
                { id: 'trattori', titolo: 'Trattori' },
                { id: 'rimorchi', titolo: 'Semirimorchi o Rimorchi' },
                { id: 'altri', titolo: 'Altri Mezzi' }
            ];

            function getCategoria(m) {
                let tipo = (m.tipologia || '').toLowerCase();
                if (tipo.includes('rimorchio') || tipo.includes('semi')) return 'rimorchi';
                if (tipo.includes('trattore')) return 'trattori';
                if (tipo.includes('tre assi') || tipo.includes('3 assi')) return 'treAssi';
                if (m.patente === 'B') return 'patenteB';
                if (m.patente === 'C') return 'patenteC';
                return 'altri';
            }

            categorie.forEach(cat => {
                let mezziInCat = currentMezzi.filter(m => getCategoria(m) === cat.id);
                if (mezziInCat.length === 0) return;

                mezziInCat.sort((a,b) => a.targa.localeCompare(b.targa));

                const titleEl = document.createElement('h3');
                titleEl.textContent = cat.titolo;
                titleEl.style.cssText = 'color: var(--primary); margin: 32px 0 16px 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; font-size: 18px; width: 100%;';
                listaDiv.appendChild(titleEl);

                const containerCat = document.createElement('div');
                if (viewMode === 'grid') {
                    containerCat.style.display = 'grid';
                    containerCat.style.gridTemplateColumns = 'repeat(auto-fill, minmax(320px, 1fr))';
                    containerCat.style.gap = '20px';
                } else {
                    containerCat.style.display = 'flex';
                    containerCat.style.flexDirection = 'column';
                    containerCat.style.gap = '0';
                }
                
                mezziInCat.forEach(m => {
                    const globalIdx = mezzi.indexOf(m);
                    const idx = globalIdx; // alias per mantenere il codice sottostante invariato
                const r = document.createElement('div');
                r.className = 'mezzo-card';
                if (viewMode === 'grid') {
                    r.style.marginBottom = '0';
                    r.style.display = 'flex';
                    r.style.flexDirection = 'column';
                    r.style.background = 'rgba(255, 255, 255, 0.6)';
                    r.style.backdropFilter = 'blur(12px)';
                    r.style.WebkitBackdropFilter = 'blur(12px)';
                    r.style.border = '1px solid rgba(255, 255, 255, 0.8)';
                    r.style.boxShadow = '0 8px 32px rgba(31, 38, 135, 0.07)';
                    r.style.borderRadius = '16px';
                }
                
                const title = m.modello ? `${m.targa} <span style="font-weight:400; color:#64748b; font-size:15px; margin-left:8px;">${m.modello}</span>` : m.targa;
                const patenteLabel = m.patente === 'C' ? '<span class="badge badge-yellow">CAT C</span>' : '<span class="badge badge-blue">CAT B</span>';
                const statusBadge = (m.attivo === false || (m.stato && m.stato.toLowerCase() !== 'attivo')) ? '<span class="badge badge-gray">Non Attivo</span>' : '<span class="badge badge-green">Attivo</span>';
                
                let htmlFiles = '<div style="font-size:13px; color:#64748b; margin-bottom:8px;">Nessun media presente.</div>';
                let hasDocs = false;
                let filesGrid = '<div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap:12px;">';
                
                if (permMedia !== 'none') {
                    if (m.fotoUrls && m.fotoUrls.length > 0) {
                        hasDocs = true;
                        m.fotoUrls.forEach(f => {
                            filesGrid += `<a href="${f.url}" target="_blank" onclick="event.stopPropagation();" style="display:flex; flex-direction:column; align-items:center; padding:8px; background:rgba(255, 255, 255, 0.5); border:1px solid rgba(255, 255, 255, 0.4); border-radius:12px; text-decoration:none; color:#1e293b; font-size:11px; text-align:center; box-shadow:0 4px 15px rgba(0,0,0,0.03); transition:transform 0.2s;" onmouseover="this.style.transform='translateY(-3px)';" onmouseout="this.style.transform='translateY(0)';">
                                <img src="${f.url}" alt="${f.name}" style="width:100%; height:80px; object-fit:cover; border-radius:6px; margin-bottom:6px;">
                                <span style="overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">${f.name}</span>
                            </a>`;
                        });
                    }
                    if (m.documentiUrls && m.documentiUrls.length > 0) {
                        hasDocs = true;
                        m.documentiUrls.forEach((f, fileIdx) => {
                            const isPdf = f.name.toLowerCase().endsWith('.pdf');
                            const uniqueId = `pdf-${idx}-${fileIdx}`;
                            let visualElement = `<div id="icon-${uniqueId}" style="width:100%; height:80px; display:flex; align-items:center; justify-content:center; background:rgba(241, 245, 249, 0.7); border-radius:6px; margin-bottom:6px;"><span class="material-icons-round" style="font-size:36px; color:${isPdf?'#ef4444':'#3b82f6'};">${isPdf?'picture_as_pdf':'description'}</span></div>`;
                            if (isPdf) visualElement += `<canvas id="canvas-${uniqueId}" class="pdf-thumbnail-canvas" style="display:none; width:100%; height:80px; object-fit:contain; border-radius:6px; margin-bottom:6px;" data-pdf-url="${f.url}" data-icon-id="icon-${uniqueId}"></canvas>`;

                            filesGrid += `<a href="${f.url}" target="_blank" onclick="event.stopPropagation();" style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:8px; background:rgba(255, 255, 255, 0.5); border:1px solid rgba(255, 255, 255, 0.4); border-radius:12px; text-decoration:none; color:#1e293b; font-size:11px; text-align:center; box-shadow:0 4px 15px rgba(0,0,0,0.03); transition:transform 0.2s;" onmouseover="this.style.transform='translateY(-3px)';" onmouseout="this.style.transform='translateY(0)';">
                                ${visualElement}
                                <span style="overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">${f.name}</span>
                            </a>`;
                        });
                    }
                }
                filesGrid += '</div>';
                if (hasDocs) htmlFiles = filesGrid;

                let htmlStorico = '<div style="font-size:13px; color:#64748b;">Nessuna manutenzione registrata.</div>';
                if (permManutenzioni !== 'none' && m.storico_manutenzioni && m.storico_manutenzioni.length > 0) {
                    htmlStorico = `<table class="storico-table" style="background:white; border-radius:8px; overflow:hidden;">
                        <thead><tr><th>Data</th><th>KM</th><th>Interventi</th></tr></thead><tbody>`;
                    m.storico_manutenzioni.sort((a,b)=> new Date(b.data || 0) - new Date(a.data || 0)).forEach(s => {
                        const info = [s.lavorazioni, s.freni, s.batteria, s.pneumatici].filter(x => x).join(' | ');
                        htmlStorico += `<tr><td>${formattaData(s.data)}</td><td>${s.km || '-'}</td><td>${info}</td></tr>`;
                    });
                    htmlStorico += `</tbody></table>`;
                }

                let detailsHtml = `<div class="details-grid">`;
                
                if (permAnagrafica !== 'none') {
                    detailsHtml += `
                            <div class="detail-item"><span class="detail-label">Targa</span><span class="detail-value">${m.targa || '-'}</span></div>
                            <div class="detail-item"><span class="detail-label">Modello</span><span class="detail-value">${m.modello || '-'}</span></div>
                            <div class="detail-item"><span class="detail-label">Proprietà</span><span class="detail-value">${m.proprietario || '-'}</span></div>
                            <div class="detail-item"><span class="detail-label">Tipologia</span><span class="detail-value">${m.tipologia || '-'}</span></div>
                            <div class="detail-item"><span class="detail-label">Patente</span><span class="detail-value">${m.patente === 'C' ? 'C (Camion)' : 'B (Furgone)'}</span></div>
                            <div class="detail-item"><span class="detail-label">Immatricolazione</span><span class="detail-value">${formattaData(m.immatricolazione)}</span></div>
                            <div class="detail-item"><span class="detail-label">Stato</span><span class="detail-value">${(m.attivo===false || (m.stato && m.stato.toLowerCase() !== 'attivo')) ? 'Inattivo' : 'Attivo'}</span></div>
                    `;
                }
                
                if (permScadenze !== 'none') {
                    detailsHtml += `
                            <div class="detail-item"><span class="detail-label">Compagnia Assic.</span><span class="detail-value">${m.assicurazione || '-'}</span></div>
                            <div class="detail-item"><span class="detail-label">Scad. Assicurazione</span><span class="detail-value">${formattaData(m.scadenza_assicurazione)}</span></div>
                            <div class="detail-item"><span class="detail-label">Scad. Revisione</span><span class="detail-value">${formattaData(m.scadenza_revisione)}</span></div>
                            <div class="detail-item"><span class="detail-label">Scad. ATP</span><span class="detail-value">${formattaData(m.scadenza_atp)}</span></div>
                            ${m.patente === 'C' ? `<div class="detail-item"><span class="detail-label">Scad. Tachigrafo</span><span class="detail-value">${formattaData(m.scadenza_tachigrafo)}</span></div>` : ''}
                    `;
                }

                if (permCarburante !== 'none') {
                    detailsHtml += `
                            <div class="detail-item"><span class="detail-label">Tessera Carburante</span><span class="detail-value">${m.tessera_carburante || '-'} (PIN: ${m.pin_tessera || '-'})</span></div>
                            <div class="detail-item" style="grid-column: span 2;"><span class="detail-label">Note</span><span class="detail-value" style="color:#ef4444;">${m.note || '-'}</span></div>
                    `;
                }
                
                detailsHtml += `</div>`;
                
                if (permMedia !== 'none' || (permFornitore === 'read_docs' && permMedia === 'none')) {
                    detailsHtml += htmlFiles;
                }
                
                if (permManutenzioni !== 'none') {
                    detailsHtml += `
                            <h4 style="margin:20px 0 10px; color:#475569; border-bottom:1px solid #e2e8f0; padding-bottom:4px; display:flex; justify-content:space-between; align-items:center;">
                                <span>Storico Manutenzioni</span>
                                ${permManutenzioni === 'write' ? `<button type="button" class="action-btn" style="padding:4px 8px; font-size:12px; color:var(--primary); border-color:var(--primary);" onclick="apriFormManutenzione(${idx})">
                                    <span class="material-icons-round" style="font-size:14px; margin-right:4px;">build</span> Aggiungi Intervento
                                </button>` : ''}
                            </h4>
                            ${htmlStorico}
                    `;
                }

                const coverUrl = m.copertinaUrl || (m.fotoUrls && m.fotoUrls.length > 0 ? m.fotoUrls[0].url : null);
                
                if (viewMode === 'grid') {
                    r.style.background = 'radial-gradient(circle at 0% 10%, rgba(14, 165, 233, 0.3) 0%, transparent 60%), linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(2, 6, 23, 1) 100%)';
                    r.style.backdropFilter = 'blur(16px)';
                    r.style.WebkitBackdropFilter = 'blur(16px)';
                    r.style.border = '1px solid rgba(255, 255, 255, 0.1)';
                    r.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.1)';
                    r.style.borderRadius = '24px';
                    r.style.color = '#fff';
                    r.style.overflow = 'hidden';
                    r.style.position = 'relative';

                    let heroImage = `<div style="width:100%; height:240px; display:flex; align-items:center; justify-content:center; border-bottom:1px solid rgba(6,182,212,0.3); box-shadow:0 2px 15px rgba(6,182,212,0.15);">
                        <span class="material-icons-round" style="color:rgba(255,255,255,0.2); font-size:80px;">local_shipping</span>
                    </div>`;
                    
                    if (coverUrl) {
                        heroImage = `<div style="width:100%; height:240px; overflow:hidden; border-bottom:1px solid rgba(6,182,212,0.4); box-shadow:0 2px 15px rgba(6,182,212,0.2); position:relative; display:flex; align-items:center; justify-content:center;">
                            <img src="${coverUrl}" style="width:100%; height:100%; object-fit:cover; opacity:0.9;" alt="Foto mezzo">
                            <div style="position:absolute; inset:0; background:linear-gradient(to top, rgba(10,15,25,0.9) 0%, transparent 40%, rgba(10,15,25,0.5) 100%); pointer-events:none;"></div>
                        </div>`;
                    }
                    
                    const getScadenzaStyle = (dateStr, defaultColor, defaultBg) => {
                        if(!dateStr) return { color: defaultColor, bg: defaultBg, border: defaultColor, shadow: defaultColor, alert: false };
                        const d = new Date(dateStr);
                        if(isNaN(d)) return { color: defaultColor, bg: defaultBg, border: defaultColor, shadow: defaultColor, alert: false };
                        const diffDays = Math.ceil((d - new Date()) / (1000 * 60 * 60 * 24));
                        if (diffDays <= 30) {
                            return { color: '#fca5a5', bg: 'rgba(239,68,68,0.2)', border: '#ef4444', shadow: 'rgba(239,68,68,0.8)', alert: true };
                        }
                        return { color: defaultColor, bg: defaultBg, border: defaultColor, shadow: defaultColor, alert: false };
                    };

                    const styleAss = getScadenzaStyle(m.scadenza_assicurazione, '#93c5fd', 'rgba(59,130,246,0.1)');
                    const styleRev = getScadenzaStyle(m.scadenza_revisione, '#d8b4fe', 'rgba(168,85,247,0.1)');
                    const styleAtp = getScadenzaStyle(m.scadenza_atp, '#86efac', 'rgba(34,197,94,0.1)');
                    const styleTach = getScadenzaStyle(m.scadenza_tachigrafo, '#fcd34d', 'rgba(251,191,36,0.1)');

                    const badgeAss = `<span style="border: 1px solid ${styleAss.border}; box-shadow: 0 0 ${styleAss.alert ? '15px' : '10px'} ${styleAss.shadow}; color: ${styleAss.color}; padding:6px 12px; font-size:12px; border-radius:12px; font-weight:600; background:${styleAss.bg}; animation: ${styleAss.alert ? 'pulse 2s infinite' : 'none'};"><span class="material-icons-round" style="font-size:14px; vertical-align:text-bottom; margin-right:4px;">calendar_month</span>Assic: ${formattaData(m.scadenza_assicurazione)}</span>`;
                    const badgeRev = `<span style="border: 1px solid ${styleRev.border}; box-shadow: 0 0 ${styleRev.alert ? '15px' : '10px'} ${styleRev.shadow}; color: ${styleRev.color}; padding:6px 12px; font-size:12px; border-radius:12px; font-weight:600; background:${styleRev.bg}; animation: ${styleRev.alert ? 'pulse 2s infinite' : 'none'};"><span class="material-icons-round" style="font-size:14px; vertical-align:text-bottom; margin-right:4px;">build</span>Rev: ${formattaData(m.scadenza_revisione)}</span>`;
                    const badgeAtp = `<span style="border: 1px solid ${styleAtp.border}; box-shadow: 0 0 ${styleAtp.alert ? '15px' : '10px'} ${styleAtp.shadow}; color: ${styleAtp.color}; padding:6px 12px; font-size:12px; border-radius:12px; font-weight:600; background:${styleAtp.bg}; animation: ${styleAtp.alert ? 'pulse 2s infinite' : 'none'};"><span class="material-icons-round" style="font-size:14px; vertical-align:text-bottom; margin-right:4px;">ac_unit</span>ATP: ${formattaData(m.scadenza_atp)}</span>`;
                    const badgeTach = (!m.patente || m.patente === 'B') ? '' : `<span style="border: 1px solid ${styleTach.border}; box-shadow: 0 0 ${styleTach.alert ? '15px' : '10px'} ${styleTach.shadow}; color: ${styleTach.color}; padding:6px 12px; font-size:12px; border-radius:12px; font-weight:600; background:${styleTach.bg}; animation: ${styleTach.alert ? 'pulse 2s infinite' : 'none'};"><span class="material-icons-round" style="font-size:14px; vertical-align:text-bottom; margin-right:4px;">speed</span>Tachigrafo: ${formattaData(m.scadenza_tachigrafo)}</span>`;
                    
                    r.innerHTML = `
                        <div style="cursor:pointer; position:relative; z-index:1;" onclick="toggleDetails(${idx})">
                            <div style="position:absolute; top:20px; left:20px; right:20px; display:flex; justify-content:space-between; align-items:flex-start; z-index:10; pointer-events:none;">
                                <div>
                                    <div style="font-size:12px; color:${m.patente === 'C' || m.patente === 'CE' ? '#fde047' : '#93c5fd'}; text-transform:uppercase; letter-spacing:1px; margin-bottom:2px; text-shadow:0 1px 5px rgba(0,0,0,0.5);">Targa</div>
                                    <div style="font-size:32px; font-weight:900; color:${m.patente === 'C' || m.patente === 'CE' ? '#fde047' : '#93c5fd'}; text-shadow:0 2px 10px rgba(0,0,0,0.8); letter-spacing:1px; line-height:1; display:flex; align-items:center; gap:12px;">
                                        ${m.targa}
                                    </div>
                                </div>
                                <div style="display:flex; flex-direction:column; gap:8px; align-items:flex-end;">
                                    ${badgeAss}
                                    ${badgeRev}
                                    ${badgeAtp}
                                    ${badgeTach}
                                </div>
                            </div>
                            
                            ${heroImage}
                            
                            <div style="padding:24px;">
                                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:16px; margin-bottom:24px;">
                                    <div style="border-right:1px solid rgba(255,255,255,0.1); padding-right:16px;">
                                        <div style="display:flex; align-items:center; gap:6px; color:#67e8f9; font-weight:600; font-size:14px; margin-bottom:4px;">
                                            <span class="material-icons-round" style="font-size:18px;">business</span> Proprietà
                                        </div>
                                        <div style="font-size:13px; color:rgba(255,255,255,0.7); line-height:1.4;">${m.proprietario || 'N/D'}</div>
                                    </div>
                                    <div style="border-right:1px solid rgba(255,255,255,0.1); padding-right:16px;">
                                        <div style="display:flex; align-items:center; gap:6px; color:#67e8f9; font-weight:600; font-size:14px; margin-bottom:4px;">
                                            <span class="material-icons-round" style="font-size:18px;">check_circle</span> Stato
                                        </div>
                                        <div style="font-size:13px; color:rgba(255,255,255,0.7); line-height:1.4;">${(m.attivo===false)?'Inattivo':'Attivo'}</div>
                                    </div>
                                    <div>
                                        <div style="display:flex; align-items:center; gap:6px; color:#67e8f9; font-weight:600; font-size:14px; margin-bottom:4px;">
                                            <span class="material-icons-round" style="font-size:18px;">local_shipping</span> Tipologia
                                        </div>
                                        <div style="font-size:13px; color:rgba(255,255,255,0.7); line-height:1.4;">${m.tipologia || 'N/D'}</div>
                                    </div>
                                </div>
                                
                                <div style="display:flex; gap:16px;">
                                    <button onclick="editMezzo(${idx}); event.stopPropagation();" style="flex:1; padding:12px; background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); border-radius:12px; color:white; font-weight:600; font-size:14px; cursor:pointer; display:flex; justify-content:center; align-items:center; gap:8px; transition:all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'"><span class="material-icons-round" style="font-size:18px;">edit</span> Modifica Mezzo</button>
                                </div>
                            </div>
                        </div>
                    `;
                } else {
                    let thumbnailHtml = `<div style="width:56px; height:56px; border-radius:12px; background:rgba(0,0,0,0.04); display:flex; align-items:center; justify-content:center; margin-right:16px; flex-shrink:0; border:1px dashed rgba(0,0,0,0.1);">
                        <span class="material-icons-round" style="color:#cbd5e1; font-size:28px;">local_shipping</span>
                    </div>`;
                    if (m.fotoUrls && m.fotoUrls.length > 0) {
                        thumbnailHtml = `<div style="width:56px; height:56px; border-radius:12px; margin-right:16px; flex-shrink:0; overflow:hidden; border:1px solid rgba(0,0,0,0.05); box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                            <img src="${m.fotoUrls[0].url}" style="width:100%; height:100%; object-fit:cover;" alt="Foto mezzo">
                        </div>`;
                    }
                    r.innerHTML = `
                        <div class="mezzo-header" onclick="toggleDetails(${idx})">
                            <div style="display:flex; align-items:center; width:100%;">
                                ${thumbnailHtml}
                                <div style="flex:1;">
                                    <div style="font-size:18px; font-weight:700; color:#1e293b; margin-bottom:6px; display:flex; align-items:center; gap:8px;">
                                        ${title} ${statusBadge} ${patenteLabel}
                                    </div>
                                    <div style="display:flex; gap:6px; flex-wrap:wrap;">
                                        <span class="badge ${getBadgeColor(m.scadenza_assicurazione)}">🛡️ Ass: ${formattaData(m.scadenza_assicurazione)}</span>
                                        <span class="badge ${getBadgeColor(m.scadenza_revisione)}">🔧 Rev: ${formattaData(m.scadenza_revisione)}</span>
                                        <span class="badge ${getBadgeColor(m.scadenza_atp)}">❄️ ATP: ${formattaData(m.scadenza_atp)}</span>
                                        ${(!m.patente || m.patente === 'B') ? '' : `<span class="badge ${getBadgeColor(m.scadenza_tachigrafo)}">⏱️ Tach: ${formattaData(m.scadenza_tachigrafo)}</span>`}
                                    </div>
                                </div>
                            </div>
                            <div style="display:flex; gap:8px; align-items:center;">
                                <button onclick="editMezzo(${idx}); event.stopPropagation();" class="action-btn" title="Modifica"><span class="material-icons-round">edit</span></button>
                                <button onclick="deleteMezzo(${idx}); event.stopPropagation();" class="action-btn delete-btn" title="Elimina"><span class="material-icons-round">delete</span></button>
                            </div>
                        </div>
                        <div id="mezzo-details-${idx}" style="display:none; padding:20px; background:rgba(255,255,255,0.4);">
                            ${detailsHtml}
                        </div>
                    `;
                }
                containerCat.appendChild(r);
                });
                listaDiv.appendChild(containerCat);
            });
        };

        window.renderMezzoFiles = function(mezzo) {
            const fotoContainer = document.getElementById('fotoMezzoPreview');
            const docContainer = document.getElementById('documentiMezzoPreview');
            if (fotoContainer) fotoContainer.innerHTML = '';
            if (docContainer) docContainer.innerHTML = '';
            if (mezzo && mezzo.fotoUrls) {
                mezzo.fotoUrls.forEach((f, idx) => {
                    const div = document.createElement('div');
                    div.style.cssText = "display:flex; justify-content:space-between; align-items:center; background:#f8fafc; padding:8px; border-radius:6px; font-size:12px; border:1px solid #e2e8f0;";
                    div.innerHTML = `<a href="${f.url}" target="_blank" style="color:var(--primary); text-decoration:none; display:flex; align-items:center; gap:4px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:70%;"><span class="material-icons-round" style="font-size:16px;">image</span> ${f.name}</a>
                    <div style="display:flex; gap:4px;">
                        <button type="button" class="action-btn" style="padding:2px; min-width:24px; min-height:24px; border:none; color:#eab308;" onclick="setCopertina('${mezzo.targa}', '${f.url}')" title="Imposta come foto del front"><span class="material-icons-round" style="font-size:16px;">star</span></button>
                        <button type="button" class="action-btn delete-btn" style="padding:2px; min-width:24px; min-height:24px; border:none;" onclick="removeMezzoFile('fotoUrls', ${idx})"><span class="material-icons-round" style="font-size:14px; color:#ef4444;">close</span></button>
                    </div>`;
                    fotoContainer.appendChild(div);
                });
            }
            if (mezzo && mezzo.documentiUrls) {
                mezzo.documentiUrls.forEach((f, idx) => {
                    const div = document.createElement('div');
                    div.style.cssText = "display:flex; justify-content:space-between; align-items:center; background:#f8fafc; padding:8px; border-radius:6px; font-size:12px; border:1px solid #e2e8f0;";
                    div.innerHTML = `<a href="${f.url}" target="_blank" style="color:var(--primary); text-decoration:none; display:flex; align-items:center; gap:4px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:85%;"><span class="material-icons-round" style="font-size:16px;">description</span> ${f.name}</a><button type="button" class="action-btn delete-btn" style="padding:2px; min-width:24px; min-height:24px; border:none;" onclick="removeMezzoFile('documentiUrls', ${idx})"><span class="material-icons-round" style="font-size:14px; color:#ef4444;">close</span></button>`;
                    docContainer.appendChild(div);
                });
            }
        };

        window.removeMezzoFile = function(arrayName, idx) {
            if (!confirm("Sicuro di voler rimuovere questo file? La rimozione sarà definitiva dopo il salvataggio.")) return;
            const mezzo = (editIndex >= 0) ? mezzi[editIndex] : null;
            if(mezzo && mezzo[arrayName]) {
                const fileItem = mezzo[arrayName][idx];
                if (fileItem.path) window.filesToDeleteFromStorage.push(fileItem.path);
                mezzo[arrayName].splice(idx, 1);
                window.renderMezzoFiles(mezzo);
            }
        };

        window.setCopertina = async function(targa, url) {
            try {
                const { doc, updateDoc } = await import("https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js");
                const m = mezzi.find(x => x.targa === targa);
                if (!m) throw new Error("Mezzo non trovato in memoria");
                
                const docId = m.id || targa;
                const db = window.db; // inizializzato globalmente in script.js / realtime-sync.js
                
                await updateDoc(doc(db, 'mezzi', docId), { copertinaUrl: url });
                
                m.copertinaUrl = url;
                if (typeof window.appData !== 'undefined' && window.appData.lista_mezzi) {
                    const globalM = window.appData.lista_mezzi.find(x => x.targa === targa);
                    if (globalM) globalM.copertinaUrl = url;
                }
                Swal.fire({ title: 'Foto del front impostata', icon: 'success', toast: true, position: 'top-end', showConfirmButton: false, timer: 2000 });
                window.renderLista();
            } catch (error) {
                console.error("Errore impostazione foto del front:", error);
                Swal.fire({ title: 'Errore', text: 'Impossibile impostare la foto del front.', icon: 'error' });
            }
        };

        // --- GESTIONE MANUTENZIONI CRUD ---
        window.renderStoricoTable = function() {
            const tbody = document.getElementById('storicoTbody');
            tbody.innerHTML = '';
            window.storico_corrente.forEach((s, idx) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${formattaData(s.data)}</td>
                    <td>${s.km || ''}</td>
                    <td>${s.lavorazioni || ''}</td>
                    <td>${s.freni || ''}</td>
                    <td>${s.batteria || ''}</td>
                    <td>${s.pneumatici || ''}</td>
                    <td style="display:flex; gap:4px;">
                        <button type="button" class="action-btn" onclick="modificaManutenzione(${idx})" style="padding:4px;"><span class="material-icons-round" style="font-size:16px;">edit</span></button>
                        <button type="button" class="action-btn delete-btn" onclick="eliminaManutenzione(${idx})" style="padding:4px;"><span class="material-icons-round" style="font-size:16px;">delete</span></button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        };

        window.apriFormManutenzione = function() {
            editStoricoIndex = -1;
            document.getElementById('manutData').value = '';
            document.getElementById('manutKm').value = '';
            document.getElementById('manutLavorazioni').value = '';
            document.getElementById('manutFreni').value = '';
            document.getElementById('manutBatteria').value = '';
            document.getElementById('manutPneumatici').value = '';
            document.getElementById('manutenzioneTitle').textContent = 'Nuovo Intervento';
            document.getElementById('formManutenzioneContainer').style.display = 'block';
        };

        window.modificaManutenzione = function(idx) {
            editStoricoIndex = idx;
            const s = window.storico_corrente[idx];
            document.getElementById('manutData').value = s.data || '';
            document.getElementById('manutKm').value = s.km || '';
            document.getElementById('manutLavorazioni').value = s.lavorazioni || '';
            document.getElementById('manutFreni').value = s.freni || '';
            document.getElementById('manutBatteria').value = s.batteria || '';
            document.getElementById('manutPneumatici').value = s.pneumatici || '';
            document.getElementById('manutenzioneTitle').textContent = 'Modifica Intervento';
            document.getElementById('formManutenzioneContainer').style.display = 'block';
        };

        window.chiudiFormManutenzione = function() {
            document.getElementById('formManutenzioneContainer').style.display = 'none';
        };

        window.salvaManutenzione = function() {
            const m = {
                data: document.getElementById('manutData').value,
                km: document.getElementById('manutKm').value,
                lavorazioni: document.getElementById('manutLavorazioni').value,
                freni: document.getElementById('manutFreni').value,
                batteria: document.getElementById('manutBatteria').value,
                pneumatici: document.getElementById('manutPneumatici').value
            };
            if(editStoricoIndex >= 0) {
                m.id = window.storico_corrente[editStoricoIndex].id;
                window.storico_corrente[editStoricoIndex] = m;
            } else {
                m.id = Date.now().toString(); // fake guid
                window.storico_corrente.push(m);
            }
            window.renderStoricoTable();
            window.chiudiFormManutenzione();
        };

        window.eliminaManutenzione = function(idx) {
            if(confirm('Eliminare questo intervento?')) {
                window.storico_corrente.splice(idx, 1);
                window.renderStoricoTable();
            }
        };
        // ----------------------------------

        window.applyFormPermissions = function() {
            const isFornitore = window.appData && window.appData.currentUser && window.appData.currentUser.ruolo === 'fornitore';
            let permFornitoreRaw = window.appData && window.appData.permessiDashboard && window.appData.permessiDashboard['gestione_mezzi'] && window.appData.permessiDashboard['gestione_mezzi']['fornitore'] ? window.appData.permessiDashboard['gestione_mezzi']['fornitore'] : 'none';
            let permFornitore = permFornitoreRaw;
            let advModules = null;
            if (typeof permFornitoreRaw === 'object' && permFornitoreRaw.access === 'advanced') {
                permFornitore = 'advanced';
                advModules = permFornitoreRaw.modules || {};
            }

            const getModPerm = (modName) => {
                if (!isFornitore) return 'write';
                if (permFornitore === 'write') return 'write';
                if (permFornitore === 'read' || permFornitore === 'read_docs') return 'read';
                if (permFornitore === 'advanced' && advModules) return advModules[modName] || 'none';
                return 'none';
            };

            const toggleSection = (containerId, contentId, perm) => {
                const container = document.getElementById(containerId);
                const content = document.getElementById(contentId);
                if (!container || !content) return;
                
                container.style.display = (perm === 'none') ? 'none' : 'block';
                
                const inputs = content.querySelectorAll('input, select, textarea, button');
                inputs.forEach(input => {
                    input.disabled = (perm === 'read');
                    if(perm === 'read') {
                        if (input.tagName === 'BUTTON' && !input.classList.contains('action-btn')) {
                            input.style.display = 'none'; // hide generic buttons like upload if readonly
                        }
                    } else {
                        if (input.tagName === 'BUTTON' && input.style.display === 'none') {
                            input.style.display = ''; 
                        }
                    }
                });
            };

            const permAnagrafica = getModPerm('anagrafica');
            const permScadenze = getModPerm('scadenze');
            const permCarburante = getModPerm('carburante');
            const permManutenzioni = getModPerm('manutenzioni');
            const permMedia = getModPerm('media');

            toggleSection('sec-anagrafica-container', 'sec-anagrafica', permAnagrafica);
            toggleSection('sec-scadenze-container', 'sec-scadenze', permScadenze);
            toggleSection('sec-carburante-container', 'sec-carburante', permCarburante);
            toggleSection('sec-manutenzioni-container', 'sec-manutenzioni-container', permManutenzioni);
            toggleSection('sec-media-container', 'sec-media', permMedia);

            const btnAggiungiManut = document.getElementById('btnAggiungiManutenzioneForm');
            if (btnAggiungiManut) btnAggiungiManut.style.display = (permManutenzioni === 'write') ? 'inline-flex' : 'none';

            // nascondiamo tutti i bottoni action-btn della tabella storico se readonly
            const actionBtns = document.querySelectorAll('#storicoTbody .action-btn');
            actionBtns.forEach(b => b.style.display = (permManutenzioni === 'write') ? 'inline-flex' : 'none');

            // nascondiamo bottoni upload/cancella foto e documenti se readonly
            const hideMediaBtns = (permMedia !== 'write');
            document.getElementById('fotoMezzoInput').disabled = hideMediaBtns;
            document.getElementById('documentiMezzoInput').disabled = hideMediaBtns;
            
            const actionMediaBtns = document.querySelectorAll('#fotoMezzoPreview .action-btn, #documentiMezzoPreview .action-btn');
            actionMediaBtns.forEach(b => b.style.display = hideMediaBtns ? 'none' : 'inline-flex');

            // Hide the main save button if absolutely EVERYTHING is read-only or none
            const canWriteAnything = [permAnagrafica, permScadenze, permCarburante, permManutenzioni, permMedia].includes('write');
            document.getElementById('btnSalvaMezzo').style.display = canWriteAnything ? 'inline-flex' : 'none';
        };

        window.apriNuovoMezzo = function() {
            editIndex = -1;
            document.getElementById('formTitle').textContent = "Aggiungi Nuovo Mezzo";
            targaInput.value = '';
            modelloInput.value = '';
            patenteInput.value = 'B';
            attivoInput.checked = true;
            tipologiaInput.value = '';
            proprietarioInput.value = '';
            assicInput.value = '';
            scAssicInput.value = '';
            scRevInput.value = '';
            scAtpInput.value = '';
            scTachInput.value = '';
            immInput.value = '';
            tesseraInput.value = '';
            pinInput.value = '';
            noteInput.value = '';
            
            window.storico_corrente = [];
            window.renderStoricoTable();
            
            document.getElementById('fotoMezzoInput').value = '';
            document.getElementById('documentiMezzoInput').value = '';
            window.filesToDeleteFromStorage = [];
            window.renderMezzoFiles(null);
            
            btnSalvaMezzo.textContent = "Salva Nuovo Mezzo";
            document.getElementById('formMezziContainer').style.display = 'block';
            window.applyFormPermissions();
            targaInput.focus();
        };

        window.editMezzo = function (idx) {
            if (editIndex !== -1 && editIndex !== idx) {
                if (!confirm("Hai una targa in modifica. Vuoi abbandonarla per modificare questa?")) return;
            }
            document.getElementById('formTitle').textContent = "Modifica Mezzo";
            document.getElementById('formMezziContainer').style.display = 'block';
            editIndex = idx;
            const mezzo = mezzi[idx];
            
            targaInput.value = mezzo.targa;
            modelloInput.value = mezzo.modello || '';
            patenteInput.value = mezzo.patente || 'B';
            attivoInput.checked = mezzo.attivo !== false;
            tipologiaInput.value = mezzo.tipologia || '';
            proprietarioInput.value = mezzo.proprietario || '';
            assicInput.value = mezzo.assicurazione || '';
            scAssicInput.value = mezzo.scadenza_assicurazione || '';
            scRevInput.value = mezzo.scadenza_revisione || '';
            scAtpInput.value = mezzo.scadenza_atp || '';
            scTachInput.value = mezzo.scadenza_tachigrafo || '';
            immInput.value = mezzo.immatricolazione || '';
            tesseraInput.value = mezzo.tessera_carburante || '';
            pinInput.value = mezzo.pin_tessera || '';
            noteInput.value = mezzo.note || '';

            window.storico_corrente = Array.isArray(mezzo.storico_manutenzioni) ? JSON.parse(JSON.stringify(mezzo.storico_manutenzioni)) : [];
            window.renderStoricoTable();

            document.getElementById('fotoMezzoInput').value = '';
            document.getElementById('documentiMezzoInput').value = '';
            window.filesToDeleteFromStorage = [];
            window.renderMezzoFiles(mezzo);
            
            btnSalvaMezzo.textContent = "Aggiorna Mezzo";
            window.applyFormPermissions();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };

        window.chiudiForm = function() {
            document.getElementById('formMezziContainer').style.display = 'none';
            editIndex = -1;
        };

        window.deleteMezzo = async function (idx) {
            const m = mezzi[idx];
            if (confirm('Eliminare definitivamente ' + m.targa + '? (I file su Storage non verranno eliminati automaticamente)')) {
                try {
                    if (window.deleteFromFirebase && m.id) {
                        await window.deleteFromFirebase("mezzi", m.id);
                    }
                    alert("Mezzo eliminato dal Cloud!");
                } catch (e) {
                    alert("Errore eliminazione: " + e.message);
                }
            }
        };

        btnSalvaMezzo.onclick = async () => {
            const targa = targaInput.value.trim().toUpperCase();
            if (!targa) return alert("Inserire la targa");

            btnSalvaMezzo.disabled = true;
            btnSalvaMezzo.textContent = "Upload e Salvataggio...";

            const isFornitore = window.appData && window.appData.currentUser && window.appData.currentUser.ruolo === 'fornitore';
            const mezzoData = { 
                targa: targa, 
                modello: isFornitore && editIndex >= 0 ? mezzi[editIndex].modello : modelloInput.value.trim(), 
                patente: isFornitore && editIndex >= 0 ? mezzi[editIndex].patente : (patenteInput.value || 'B'),
                attivo: isFornitore && editIndex >= 0 ? mezzi[editIndex].attivo : attivoInput.checked,
                tipologia: isFornitore && editIndex >= 0 ? mezzi[editIndex].tipologia : tipologiaInput.value.trim(),
                proprietario: isFornitore && editIndex >= 0 ? mezzi[editIndex].proprietario : proprietarioInput.value.trim(),
                assicurazione: isFornitore && editIndex >= 0 ? mezzi[editIndex].assicurazione : assicInput.value.trim(),
                scadenza_assicurazione: isFornitore && editIndex >= 0 ? mezzi[editIndex].scadenza_assicurazione : scAssicInput.value,
                scadenza_revisione: isFornitore && editIndex >= 0 ? mezzi[editIndex].scadenza_revisione : scRevInput.value,
                scadenza_atp: isFornitore && editIndex >= 0 ? mezzi[editIndex].scadenza_atp : scAtpInput.value,
                scadenza_tachigrafo: isFornitore && editIndex >= 0 ? mezzi[editIndex].scadenza_tachigrafo : scTachInput.value,
                immatricolazione: isFornitore && editIndex >= 0 ? mezzi[editIndex].immatricolazione : immInput.value,
                tessera_carburante: isFornitore && editIndex >= 0 ? mezzi[editIndex].tessera_carburante : tesseraInput.value.trim(),
                pin_tessera: isFornitore && editIndex >= 0 ? mezzi[editIndex].pin_tessera : pinInput.value.trim(),
                note: isFornitore && editIndex >= 0 ? mezzi[editIndex].note : noteInput.value.trim(),
                storico_manutenzioni: [...window.storico_corrente]
            };
            
            const id = editIndex >= 0 ? mezzi[editIndex].id : null;
            mezzoData.fotoUrls = (editIndex >= 0 && mezzi[editIndex].fotoUrls) ? [...mezzi[editIndex].fotoUrls] : [];
            mezzoData.documentiUrls = (editIndex >= 0 && mezzi[editIndex].documentiUrls) ? [...mezzi[editIndex].documentiUrls] : [];

            try {
                const storage = window.firebaseStorage || (typeof firebaseStorage !== 'undefined' ? firebaseStorage : null);
                if (storage) {
                    const { ref: sRef, uploadBytes, getDownloadURL, deleteObject } = await import("https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js");
                    const uploadFiles = async (inputId, arrayRef, folder) => {
                        const files = document.getElementById(inputId).files;
                        for (let i = 0; i < files.length; i++) {
                            const file = files[i];
                            const safeName = file.name.replace(/\s+/g, '_');
                            const path = `MEZZI/${targa}/${folder}/${Date.now()}_${safeName}`;
                            const snap = await uploadBytes(sRef(storage, path), file);
                            const url = await getDownloadURL(snap.ref);
                            arrayRef.push({ name: file.name, url, path });
                        }
                    };
                    await uploadFiles('fotoMezzoInput', mezzoData.fotoUrls, 'foto');
                    await uploadFiles('documentiMezzoInput', mezzoData.documentiUrls, 'documenti');
                    if (window.filesToDeleteFromStorage && window.filesToDeleteFromStorage.length > 0) {
                        for (const p of window.filesToDeleteFromStorage) {
                            try { await deleteObject(sRef(storage, p)); } catch(e) { console.warn('[Storage] Errore eliminazione', p, e); }
                        }
                        window.filesToDeleteFromStorage = [];
                    }
                }
                
                if (window.updateMezzo) await window.updateMezzo(id, mezzoData);
                else {
                    // Fallback
                    const mRef = doc(window.db, "mezzi", id || targa);
                    await setDoc(mRef, mezzoData, {merge: true});
                }
                
                alert("Mezzo salvato correttamente su Firebase!");
                chiudiForm();
            } catch (err) {
                alert("Errore durante il salvataggio: " + err.message);
            } finally {
                btnSalvaMezzo.disabled = false;
                btnSalvaMezzo.textContent = editIndex >= 0 ? "Aggiorna Mezzo" : "Salva Nuovo Mezzo";
            }
        };

    if (typeof window.renderLista === "function") window.renderLista();
});

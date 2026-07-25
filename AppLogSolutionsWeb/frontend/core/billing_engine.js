/**
 * BillingEngine - Motore puro per la fatturazione (V2)
 * Calcola l'importo della fatturazione basandosi su UNA SINGOLA sorgente di dati alla volta.
 */
export class BillingEngine {
    constructor(config) {
        this.config = config || {};
    }

    /**
     * Elabora il mese usando il metodo impostato per il cliente.
     * Non fa controlli incrociati: la sorgente dati passata è l'unica fonte di verità.
     * 
     * @param {Object} clienteData - Le impostazioni del cliente (tariffe, metodo)
     * @param {String} mese - 'YYYY-MM'
     * @param {Array} datiSorgente - Array dei dati (presenze, viaggi o kpi)
     * @param {Object} mezziMap - Mappa targhe -> patenti (opzionale)
     */
    elaboraMese(clienteData, mese, datiSorgente, mezziMap = {}) {
        let totali = {
            importo_totale: 0,
            conteggio_elementi: datiSorgente.length,
            dettaglio_giornaliero: {}
        };

        const metodo = clienteData.metodo_fatturazione || 'PRESENZE';

        // Estrazione tariffe cliente (con fallback a 0)
        const t_patB = parseFloat(clienteData.patente_b) || 0;
        const t_patC = parseFloat(clienteData.patente_c) || 0;
        const navetteCustom = clienteData.navette_personalizzate || [];
        const t_collo = parseFloat(clienteData.cattel_collo) || 0;
        const t_forfait = parseFloat(clienteData.viaggio_forfait) || 0;

        datiSorgente.forEach(item => {
            let dateKey = '';
            let importoItem = 0;
            
            if (metodo === 'PRESENZE') {
                dateKey = item.data;
                const targa = (item.targa || "").toUpperCase();
                const viaggioStr = (item.viaggio || "").toUpperCase();
                const patente = mezziMap[targa] || 'B';
                
                importoItem = patente === 'C' ? t_patC : t_patB;
                
                // Controlla se  una navetta custom
                if (navetteCustom && navetteCustom.length > 0) {
                    const nav = navetteCustom.find(n => viaggioStr.includes((n.nome || "").toUpperCase()));
                    if (nav && parseFloat(nav.tariffa)) {
                        importoItem = parseFloat(nav.tariffa);
                    }
                }
            } 
            else if (metodo === 'VIAGGI') {
                dateKey = item.data_lavoro || item.data_consegna || item.data;
                
                if (t_forfait > 0) {
                    importoItem = t_forfait;
                } else {
                    const targa = (item.targa || "").toUpperCase();
                    const patente = mezziMap[targa] || 'B';
                    importoItem = patente === 'C' ? t_patC : t_patB;
                }
                
                // Eventuale costo a collo (se presente nei viaggi ddt)
                if (t_collo > 0 && item.colli) {
                    const numColli = parseInt(item.colli) || 0;
                    importoItem = numColli * t_collo; 
                }
            } 
            else if (metodo === 'KPI') {
                dateKey = item.data_lavoro || item.Data || item.data;
                // Ipotizziamo che il KPI abbia gi un importo, o usiamo un forfait, o conteggiamo colli
                const importoKpi = parseFloat(item.Importo) || parseFloat(item.importo) || 0;
                importoItem = importoKpi;
                // Se non c' importo ma ci sono colli e abbiamo la tariffa collo:
                if (importoItem === 0 && t_collo > 0 && item.Colli) {
                    importoItem = (parseInt(item.Colli) || 0) * t_collo;
                }
            }

            if (dateKey) {
                if (!totali.dettaglio_giornaliero[dateKey]) {
                    totali.dettaglio_giornaliero[dateKey] = {
                        elementi: 0,
                        importo_giornaliero: 0
                    };
                }
                totali.dettaglio_giornaliero[dateKey].elementi++;
                totali.dettaglio_giornaliero[dateKey].importo_giornaliero += importoItem;
                totali.importo_totale += importoItem;
            }
        });

        return {
            cliente: clienteData.nome,
            mese,
            metodo_utilizzato: metodo,
            totali,
            dati_processati: datiSorgente
        };
    }
}

const projectId = "log-solutions-cantiere";
const url = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/(default)/documents/clienti_fatturazione`;

fetch(url)
  .then(res => res.json())
  .then(data => {
    if(!data.documents) {
        console.log("Nessun cliente trovato o errore:", data);
        return;
    }
    data.documents.forEach(doc => {
      const fields = doc.fields;
      const nome = fields.nome ? fields.nome.stringValue : 'Sconosciuto';
      console.log(`CLIENTE: ${nome}`);
      
      if (fields.magazzini && fields.magazzini.arrayValue && fields.magazzini.arrayValue.values) {
        fields.magazzini.arrayValue.values.forEach(m => {
            const mag = m.mapValue.fields;
            const mNome = mag.nome ? mag.nome.stringValue : '';
            const mIndirizzo = mag.indirizzo ? mag.indirizzo.stringValue : '';
            const mLat = mag.lat && mag.lat.doubleValue ? mag.lat.doubleValue : (mag.lat && mag.lat.integerValue ? mag.lat.integerValue : null);
            const mLon = mag.lon && mag.lon.doubleValue ? mag.lon.doubleValue : (mag.lon && mag.lon.integerValue ? mag.lon.integerValue : null);
            console.log(`  - Magazzino: ${mNome} | Indirizzo: ${mIndirizzo} | Coordinate: ${mLat}, ${mLon}`);
        });
      } else {
        console.log("  - Nessun magazzino configurato");
      }
      console.log("-----------------------");
    });
  })
  .catch(err => console.error(err));

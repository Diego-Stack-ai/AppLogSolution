
function parseTime(val) {
    if (!val || val.trim() === "") return 0.0;
    const cleanVal = val.trim().replace(",", ".");
    if (cleanVal.includes(":")) {
        const parts = cleanVal.split(":");
        const h = parseInt(parts[0]) || 0;
        const m = parseInt(parts[1]) || 0;
        return h + m / 60.0;
    }
    const f = parseFloat(cleanVal);
    return isNaN(f) ? 0.0 : f;
}

const valInizioM = "07:30";
const valFineM = "";
const valInizioP = "";
const valFineP = "18:30";

const decInizioM = parseTime(valInizioM);
const decFineM = parseTime(valFineM);
const decInizioP = parseTime(valInizioP);
const decFineP = parseTime(valFineP);

let totalHours = 0.0;

if (valInizioM && !valFineM && !valInizioP && valFineP) {
    let diff = decFineP >= decInizioM ? decFineP - decInizioM : (24 - decInizioM) + decFineP;
    if (decFineP === 0 && decInizioM === 0) diff = 0;
    totalHours = diff;
} else {
    let mornHours = 0.0;
    if (valInizioM && valFineM) {
        mornHours = decFineM >= decInizioM ? decFineM - decInizioM : (24 - decInizioM) + decFineM;
        if (decFineM === 0 && decInizioM === 0) mornHours = 0;
    }
    let aftHours = 0.0;
    if (valInizioP && valFineP) {
        aftHours = decFineP >= decInizioP ? decFineP - decInizioP : (24 - decInizioP) + decFineP;
        if (decFineP === 0 && decInizioP === 0) aftHours = 0;
    }
    totalHours = mornHours + aftHours;
}

console.log("Total hours: ", totalHours);


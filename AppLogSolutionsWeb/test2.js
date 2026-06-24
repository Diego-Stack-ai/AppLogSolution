
let input = { value: "7.30" };
let val = input.value.trim();
if (val) {
    val = val.replace(",", ".");
    if (val.includes(".")) {
        let parts = val.split(".");
        let h = parts[0].padStart(2, "0");
        let m = parts[1].padEnd(2, "0").substring(0, 2);
        input.value = `${h}:${m}`;
    } else if (!val.includes(":") && !isNaN(val)) {
        if (val.length === 3 || val.length === 4) {
            let h = val.length === 3 ? "0" + val[0] : val.substring(0,2);
            let m = val.substring(val.length - 2);
            input.value = `${h}:${m}`;
        } else {
            let h = val.padStart(2, "0");
            input.value = `${h}:00`;
        }
    } else if (val.includes(":")) {
        let parts = val.split(":");
        let h = parts[0].padStart(2, "0");
        let m = parts[1].padEnd(2, "0").substring(0, 2);
        input.value = `${h}:${m}`;
    }
}
console.log(input.value);


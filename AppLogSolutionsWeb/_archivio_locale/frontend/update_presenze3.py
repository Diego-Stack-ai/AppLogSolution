import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

functions_to_inject = """
        window.setViewMode = function(mode) {
            currentViewMode = mode;
            currentSubFilter = null; // reset
            
            document.querySelectorAll('.view-mode-btn').forEach(b => {
                b.classList.remove('active');
                if (b.dataset.mode === mode) b.classList.add('active');
            });
            
            renderSubFilters();
            renderCalendar(currentPresenzeData);
        };

        window.setSubFilter = function(val) {
            currentSubFilter = val;
            document.querySelectorAll('.sub-filter-btn').forEach(b => {
                b.classList.remove('active');
                if (b.dataset.val === String(val)) b.classList.add('active');
            });
            renderCalendar(currentPresenzeData);
        };

        function renderSubFilters() {
            const container = document.getElementById('subFilterContainer');
            container.innerHTML = '';
            if (!selectedMonth) return;

            const [year, month] = selectedMonth.split('-').map(Number);
            const numDays = new Date(year, month, 0).getDate();

            if (currentViewMode === 'giorno') {
                for (let d = 1; d <= numDays; d++) {
                    const dt = new Date(year, month - 1, d);
                    const isWeekend = dt.getDay() === 0 || dt.getDay() === 6;
                    const btn = document.createElement('button');
                    btn.className = 'sub-filter-btn' + (isWeekend ? ' weekend' : '');
                    btn.dataset.val = d;
                    btn.textContent = d;
                    btn.onclick = () => setSubFilter(d);
                    if (currentSubFilter === d) btn.classList.add('active');
                    container.appendChild(btn);
                }
            } else if (currentViewMode === 'settimana') {
                let currentWeek = 1;
                let startDay = 1;
                for (let d = 1; d <= numDays; d++) {
                    const dt = new Date(year, month - 1, d);
                    // If it's sunday or the last day of month
                    if (dt.getDay() === 0 || d === numDays) {
                        const btn = document.createElement('button');
                        btn.className = 'sub-filter-btn';
                        btn.dataset.val = currentWeek;
                        // Format: Sett 1 (1-7)
                        btn.textContent = `Sett ${currentWeek} (${startDay}-${d})`;
                        
                        // store the range in the dataset so renderCalendar can read it
                        btn.dataset.start = startDay;
                        btn.dataset.end = d;
                        
                        btn.onclick = (e) => {
                            setSubFilter(e.target.dataset.val);
                        };
                        if (String(currentSubFilter) === String(currentWeek)) btn.classList.add('active');
                        container.appendChild(btn);
                        
                        startDay = d + 1;
                        currentWeek++;
                    }
                }
            }
        }
"""

if "window.setViewMode =" not in content:
    content = content.replace("function resetSummary() {", functions_to_inject + "\n        function resetSummary() {")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Part 3 injected.")

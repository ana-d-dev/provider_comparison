// Sorting, keyboard support and "best value" highlighting for comparison tables.
// Any table with the .comparison-table class is handled. Sortable headers are
// declared in the HTML with data-col (cell index) and an optional data-best
// ("min" or "max") used to highlight the winning value per column.

document.addEventListener("DOMContentLoaded", () => {
    // Turns "1.5 GB" / "12,90" into a number, or NaN when there is none.
    const parseNumber = (text) =>
        parseFloat(text.replace(/[^\d.,-]/g, "").replace(",", "."));

    document.querySelectorAll(".comparison-table").forEach((table) => {
        const tbody = table.tBodies[0];
        if (!tbody) return;

        const headers = Array.from(table.querySelectorAll("th.sortable[data-col]"));
        if (headers.length === 0) return; // e.g. the API reference table

        const originalRows = Array.from(tbody.rows); // remember the initial order
        const sortState = {}; // columnIndex -> 0(original), 1(asc), 2(desc)

        const sortBy = (columnIndex) => {
            if (sortState[columnIndex] === undefined) sortState[columnIndex] = 0;

            // cycle: 0(original) -> 1(asc) -> 2(desc) -> 0(original)
            sortState[columnIndex] = (sortState[columnIndex] + 1) % 3;
            const state = sortState[columnIndex];

            headers.forEach((th) => th.setAttribute("aria-sort", "none"));

            let rows;
            if (state === 0) {
                rows = originalRows.slice(); // back to original order
            } else {
                rows = Array.from(tbody.rows);
                const ascending = state === 1;

                rows.sort((a, b) => {
                    const aText = a.cells[columnIndex].innerText.trim();
                    const bText = b.cells[columnIndex].innerText.trim();
                    const aNum = parseNumber(aText);
                    const bNum = parseNumber(bText);

                    if (!isNaN(aNum) && !isNaN(bNum)) {
                        return ascending ? aNum - bNum : bNum - aNum;
                    }
                    // fallback to string comparison
                    return ascending
                        ? aText.localeCompare(bText)
                        : bText.localeCompare(aText);
                });
            }

            rows.forEach((row) => tbody.appendChild(row));

            if (state !== 0) {
                const th = headers.find((h) => Number(h.dataset.col) === columnIndex);
                if (th) {
                    th.setAttribute("aria-sort", state === 1 ? "ascending" : "descending");
                }
            }
        };

        headers.forEach((th) => {
            const columnIndex = Number(th.dataset.col);
            th.setAttribute("aria-sort", "none");

            th.addEventListener("click", () => sortBy(columnIndex));
            th.addEventListener("keydown", (event) => {
                if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    sortBy(columnIndex);
                }
            });
        });

        // Highlight the best value (cheapest / largest) in each marked column,
        // add a tooltip on the green cells, and show a legend above the table.
        let highlighted = 0;

        headers.forEach((th) => {
            const best = th.dataset.best;
            if (best !== "min" && best !== "max") return;

            const columnIndex = Number(th.dataset.col);
            const label = th.textContent.trim();
            const values = [];
            Array.from(tbody.rows).forEach((row) => {
                const cell = row.cells[columnIndex];
                if (!cell) return;
                const value = parseNumber(cell.innerText.trim());
                if (!isNaN(value)) values.push({ cell, value });
            });

            if (values.length === 0) return;

            const numbers = values.map((v) => v.value);
            const target = best === "min" ? Math.min(...numbers) : Math.max(...numbers);
            if (Math.min(...numbers) === Math.max(...numbers)) return; // all equal

            const tooltip =
                "Best " + label.toLowerCase() + " in the table (" +
                (best === "min" ? "lowest" : "highest") + ")";

            values
                .filter((v) => v.value === target)
                .forEach((v) => {
                    v.cell.classList.add("best");
                    v.cell.title = tooltip;
                    highlighted += 1;
                });
        });

        if (highlighted > 0) {
            const legend = document.createElement("p");
            legend.className = "table-legend";
            legend.innerHTML =
                '<span class="legend-swatch" aria-hidden="true"></span>' +
                "<span>Green = best value in that column " +
                "(lowest price, most GB / minutes / SMS / units).</span>";

            const wrapper = table.closest(".table-responsive") || table;
            wrapper.parentNode.insertBefore(legend, wrapper);
        }
    });
});

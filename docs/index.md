---
title: Crédito Orçamentário
toc: false
---

# Crédito Orçamentário

```js
const factCredito = FileAttachment("data/fact_credito.csv").csv({typed: true});
const filterIndex = FileAttachment("data/credito-filters.json").json();
```

```js
const filterInputs = Object.fromEntries(
  filterIndex.columns.map((col) => [
    col,
    Inputs.select([null, ...filterIndex.options[col]], {
      label: col,
      format: (d) => (d === null ? "(todos)" : d)
    })
  ])
);
const filtersForm = view(Inputs.form(filterInputs));
```

```js
const filteredRows = factCredito.filter((row) => {
  const facets = filterIndex.facets[row.key_credito] ?? {};
  return filterIndex.columns.every((col) => {
    const selected = filtersForm[col];
    if (selected === null || selected === undefined) return true;
    return (facets[col] ?? []).includes(selected);
  });
});
```

${filteredRows.length} de ${factCredito.length} registros

```js
Inputs.table(filteredRows)
```

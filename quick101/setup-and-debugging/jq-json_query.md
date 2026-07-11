# JQ - JSON Query
The `jq` command is the "Swiss Army knife" for JSON in the terminal. Whether you're debugging a Kubernetes pod or
scraping an API, here is a cheatsheet ordered from the most essential (everyday use) to the more specialized (power
user) filters.

---

## 1. The Essentials (90% of Use Cases)

These are the commands you'll use almost every time you touch a JSON file.

| Command             | Action                                                                              | Example                            |
|:--------------------|:------------------------------------------------------------------------------------|:-----------------------------------|
| **`.`**             | **Pretty-print** entire JSON                                                        | `jq '.' file.json`                 |
| **`.field`**        | Access a **key**                                                                    | `jq '.name' file.json`             |
| **`.field.nested`** | Access **nested** keys                                                              | `jq '.user.id' file.json`          |
| **`.[]`**           | **Unpack** an array                                                                 | `jq '.items[]' file.json`          |
| **`-r`**            | Output **Raw** (no quotes)                                                          | `jq -r '.id' file.json`            |
| **\|**              | exactly like the pipe, unpacks .user[] and hands off each individual object in user | `jq '.users[] \| .name' file.json` |

---

## 2. Selection & Filtering

Used to find specific needles in the JSON haystack.

### Filter by Condition (`select`)

The most powerful tool for searching.
> `jq '.[] | select(.age > 25)'`

### Slicing Arrays

* **First element:** `.[0]`
* **Range (indices 0 to 2):** `.[0:3]`
* **Last two:** `.[-2:]`

### Dealing with Nulls

Use the **`?`** operator to avoid errors if a key is missing:
> `jq '.items[].metadata?'`

---

## 3. Transformation & Construction

Use these when you need to change the JSON shape into something else.

### Building New Objects

If you only want specific fields, wrap them in `{}`.
> `jq '.[] | {user_name: .name, user_id: .id}'`

### Building New Arrays

Wrap your filter in `[]` to collect results back into a single list.
> `jq '[.users[].name]'`

### Arithmetic & Length

* **Count items:** `jq '.items | length'`
* **Sum a field:** `jq '[.items[].price] | add'`
* **Min/Max:** `jq '[.items[].score] | max'`

---

## 4. Power User Tools (Least Frequent)

For when you're writing complex scripts or cleaning messy data.

* **`keys`**: Lists all keys in an object.
    * `jq 'keys'`
* **`map()`**: Apply a filter to every element in an array.
    * `jq 'map(.name | ascii_upcase)'`
* **`del()`**: Remove a specific key from the output.
    * `jq 'del(.password)'`
* **`unique`**: Remove duplicates from an array.
    * `jq '.tags | unique'`
* **`--slurp` (`-s`)**: Read multiple JSON objects into one big array.
    * `cat log.json | jq -s '.'`

---

### Pro Tip: The "Identity" Shortcut

If you want to extract multiple non-nested keys at once without building a new object, use a comma:
`jq '.name, .email' file.json`

> On windows use PowerShell
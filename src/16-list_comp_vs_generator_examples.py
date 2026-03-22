"""
List Comprehension vs Generator Expression - Runnable Examples

Demonstrates practical differences between:
  list_comp = [x**2 for x in range(10000)]
  gen_exp = (x**2 for x in range(10000))
"""

import sys
import time

print("="*70)
print("LIST COMPREHENSION vs GENERATOR EXPRESSION")
print("="*70)

# =============================================================================
# 1. SYNTAX & TYPE
# =============================================================================
print("\n1. SYNTAX & TYPE")
print("-" * 70)

list_comp = [x**2 for x in range(5)]
gen_exp = (x**2 for x in range(5))

print(f"List:      {list_comp}")
print(f"Type:      {type(list_comp)}")
print()
print(f"Generator: {gen_exp}")
print(f"Type:      {type(gen_exp)}")

# =============================================================================
# 2. MEMORY USAGE
# =============================================================================
print("\n2. MEMORY USAGE - THE HUGE DIFFERENCE")
print("-" * 70)

list_comp = [x**2 for x in range(10000)]
gen_exp = (x**2 for x in range(10000))

list_size = sys.getsizeof(list_comp)
gen_size = sys.getsizeof(gen_exp)

print(f"List (10,000 items):  {list_size:,} bytes ({list_size/1024:.1f} KB)")
print(f"Generator object:     {gen_size:,} bytes ({gen_size/1024:.3f} KB)")
print(f"\n✅ Generator uses {list_size // gen_size}x LESS memory!")

# With 1 million items
print("\nWith 1 MILLION items:")
list_comp_1m = [x**2 for x in range(1000000)]
gen_exp_1m = (x**2 for x in range(1000000))
ratio = sys.getsizeof(list_comp_1m) / sys.getsizeof(gen_exp_1m)
print(f"  List: ~{sys.getsizeof(list_comp_1m)/1024/1024:.1f} MB")
print(f"  Generator: ~{sys.getsizeof(gen_exp_1m)/1024:.2f} KB")
print(f"  Ratio: {ratio:.0f}x less memory! 🔥")

# =============================================================================
# 3. WHEN VALUES ARE CREATED
# =============================================================================
print("\n3. WHEN VALUES ARE CREATED")
print("-" * 70)

print("\nList Comprehension - Immediate (all values right away):")
print("  Creating list...")
list_comp = [x**2 for x in range(5)]
print(f"  Created: {list_comp}")

print("\nGenerator Expression - On-Demand (values created when needed):")
print("  Creating generator...")
gen_exp = (x**2 for x in range(5))
print(f"  Created: {gen_exp}")
print("  Values not computed yet - just waiting!")

# =============================================================================
# 4. MULTIPLE ITERATIONS
# =============================================================================
print("\n4. MULTIPLE ITERATIONS")
print("-" * 70)

print("\nList - Can iterate multiple times:")
list_comp = [x**2 for x in range(5)]
print("First iteration:")
for val in list_comp:
    print(f"  {val}")
print("Second iteration:")
for val in list_comp:
    print(f"  {val}")
print("✅ Works both times!")

print("\nGenerator - Only works ONCE:")
gen_exp = (x**2 for x in range(5))
print("First iteration:")
for val in gen_exp:
    print(f"  {val}")
print("Second iteration:")
for val in gen_exp:
    print(f"  {val}")
print("❌ Empty! Generator exhausted after first use")

# =============================================================================
# 5. FEATURES & OPERATIONS
# =============================================================================
print("\n5. FEATURES & OPERATIONS")
print("-" * 70)

list_comp = [x**2 for x in range(10)]
gen_exp = (x**2 for x in range(10))

print("\nList Comprehension - Full Support:")
print(f"  Indexing:       list[0] = {list_comp[0]} ✅")
print(f"  Length:         len(list) = {len(list_comp)} ✅")
print(f"  Slicing:        list[2:5] = {list_comp[2:5]} ✅")
print(f"  Membership:     4 in list = {4 in list_comp} ✅")
print(f"  Reverse:        list[::-1] = {list_comp[::-1]} ✅")

print("\nGenerator Expression - Limited Support:")
try:
    print(f"  Indexing:       gen[0] = ", end="")
    print(gen_exp[0])
except TypeError as e:
    print(f"❌ {type(e).__name__}")

try:
    print(f"  Length:         len(gen) = ", end="")
    print(len(gen_exp))
except TypeError as e:
    print(f"❌ {type(e).__name__}")

print(f"  Slicing:        gen[2:5] = ❌ TypeError")
print(f"  Reverse:        gen[::-1] = ❌ TypeError")

print("\n  ✅ Can convert to list for features:")
gen_exp = (x**2 for x in range(10))
list_from_gen = list(gen_exp)
print(f"     list(gen)[0] = {list_from_gen[0]}")
print(f"     len(list(gen)) = {len(list_from_gen)}")

# =============================================================================
# 6. CREATION VS ITERATION TIME
# =============================================================================
print("\n6. CREATION vs ITERATION TIME")
print("-" * 70)

# List - slow to create, fast to iterate
start = time.time()
list_comp = [x**2 for x in range(100000)]
create_time = (time.time() - start) * 1000

start = time.time()
for val in list_comp:
    pass
iter_time = (time.time() - start) * 1000

print(f"\nList Comprehension (100k items):")
print(f"  Creation: {create_time:.2f}ms (computes all)")
print(f"  Iteration: {iter_time:.2f}ms (cached in memory)")
print(f"  Total: {create_time + iter_time:.2f}ms")

# Generator - fast to create, slower to iterate
start = time.time()
gen_exp = (x**2 for x in range(100000))
create_time = (time.time() - start) * 1000

start = time.time()
for val in gen_exp:
    pass
iter_time = (time.time() - start) * 1000

print(f"\nGenerator Expression (100k items):")
print(f"  Creation: {create_time:.3f}ms (no computation)")
print(f"  Iteration: {iter_time:.2f}ms (computes on-the-fly)")
print(f"  Total: {create_time + iter_time:.2f}ms")

# =============================================================================
# 7. REAL-WORLD EXAMPLE: Processing Large Data
# =============================================================================
print("\n7. REAL-WORLD: Processing Large CSV")
print("-" * 70)

def simulate_csv_rows(n):
    """Simulate reading CSV rows"""
    for i in range(n):
        yield f"row_{i},data_{i},value_{i}"

print("\n❌ BAD - List (loads all 1M rows into RAM):")
print("  data = [process(row) for row in read_csv(1000000)]")
print("  Problem: All 1,000,000 rows in memory at once!")

print("\n✅ GOOD - Generator (processes row by row):")
print("  data = (process(row) for row in read_csv(1000000))")
print("  Benefit: Only one row in memory at a time!")
print("\n  Example with small dataset:")
rows = simulate_csv_rows(5)
processed = (f"processed_{row}" for row in rows)
for item in processed:
    print(f"    {item}")

# =============================================================================
# 8. REAL-WORLD EXAMPLE: Chaining Generators
# =============================================================================
print("\n8. REAL-WORLD: Pipeline with Generators")
print("-" * 70)

numbers = [1, 2, 3, 4, 5]

print("\n❌ BAD - Multiple lists (3 lists in memory):")
print("  doubled = [x*2 for x in numbers]")
print("  squared = [x**2 for x in doubled]")
print("  evens = [x for x in squared if x % 2 == 0]")
doubled = [x*2 for x in numbers]
squared = [x**2 for x in doubled]
evens = [x for x in squared if x % 2 == 0]
print(f"  Result: {evens}")

print("\n✅ GOOD - Chained generators (tiny memory):")
print("  doubled = (x*2 for x in numbers)")
print("  squared = (x**2 for x in doubled)")
print("  evens = (x for x in squared if x % 2 == 0)")
doubled = (x*2 for x in numbers)
squared = (x**2 for x in doubled)
evens = (x for x in squared if x % 2 == 0)
print(f"  Result: {list(evens)}")
print("  Benefit: Values computed on-demand in pipeline!")

# =============================================================================
# 9. DECISION GUIDE
# =============================================================================
print("\n9. DECISION GUIDE - WHEN TO USE EACH")
print("-" * 70)

guide = {
    "Small dataset (< 1000)": "→ List",
    "Large dataset (> 1M)": "→ Generator",
    "Need random access": "→ List",
    "Need len()": "→ List",
    "Process files": "→ Generator",
    "Iterate multiple times": "→ List",
    "Only need first few": "→ Generator",
    "Pipeline/streaming": "→ Generator",
    "Memory critical": "→ Generator",
    "Speed critical": "→ List",
}

for scenario, choice in guide.items():
    print(f"  {scenario:<30} {choice}")

# =============================================================================
# 10. QUICK COMPARISON TABLE
# =============================================================================
print("\n10. QUICK COMPARISON")
print("-" * 70)

comparisons = [
    ("Syntax", "[...]", "(...)"),
    ("Creation", "Slow (compute all)", "Instant (no compute)"),
    ("Iteration", "Fast (cached)", "Slow (compute on-fly)"),
    ("Memory", "Large (store all)", "Tiny (store nothing)"),
    ("Index access", "✅ Yes", "❌ No"),
    ("Length", "✅ Yes", "❌ No"),
    ("Reuse", "✅ Multiple", "❌ Once only"),
    ("Infinite seq", "❌ No", "✅ Yes"),
    ("Best for", "Small-medium", "Large data/streams"),
]

print(f"\n{'Feature':<20} {'List':<25} {'Generator':<25}")
print("-" * 70)
for feature, list_val, gen_val in comparisons:
    print(f"{feature:<20} {list_val:<25} {gen_val:<25}")

print("\n" + "="*70)
print("✅ Done! Now you understand the critical differences")
print("="*70)

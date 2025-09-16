# Stack

Does computer have limited stack memory and does stack use main memory

## Short answer

* **The stack *does* live in main memory (RAM).** It’s just a special, per-thread region the OS carves out of your
  process’s virtual address space.
* **It’s limited on purpose** (and must be mostly contiguous) so the OS can detect bugs, keep things predictable/fast,
  and avoid one runaway thread from eating all memory.

## Why the stack is limited

1. **Per-thread allocation:** Every thread gets its own stack. If stacks were unbounded, a few deep recursions could
   wipe out RAM or starve other threads.
2. **Contiguous growth:** Stacks grow (typically downward) as a *contiguous* block. Contiguous regions can’t grow
   forever without colliding with other mappings (heap, libraries, memory-mapped files).
3. **Fast, deterministic access:** Function calls push/pop fixed-layout frames at an address held in a CPU register (the
   stack pointer). Keeping a fixed max size and a guard page makes overflow detection cheap and call/return very fast.
4. **Protection & safety:** OS places **guard pages** at stack boundaries so an overflow immediately traps (stack
   overflow) instead of silently corrupting other memory.
5. **Resource policy:** OSes set sane defaults so typical programs run reliably (e.g., many threads) without manual
   tuning. You can raise it, but not to “infinite.”

## “Why not use main memory?”

Stack **is** using main memory. The stack is just a RAM-backed region with stricter rules:

* **Stack:** automatic storage, LIFO discipline, contiguous, fast, small/medium objects with short lifetimes (return
  addresses, locals).
* **Heap:** general-purpose pool in RAM, not necessarily contiguous, grows/shrinks on demand, for large/long-lived or
  variable-size objects.

### Practical takeaways

* Put **big arrays/objects on the heap** (`new`/`malloc`) instead of the stack.
* Avoid very deep recursion; convert to iteration or use tail-recursion optimization if your compiler guarantees it.
* If you truly need more stack, you can increase it:
    * **Linux/macOS (shell):** `ulimit -s 16384` (size in KB for the current shell), or set thread stack
      via `pthread_attr_setstacksize`.
    * **Windows:** set at link time (`/STACK:...`) or per thread in `CreateThread`.
    * **JVM:** `-Xss2m` (per-thread stack size).
* If you hit “stack overflow,” it’s usually a sign to **rethink the algorithm or move storage to the heap**, not just
  crank the limit.

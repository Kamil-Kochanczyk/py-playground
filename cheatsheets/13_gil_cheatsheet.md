# Prerequisites

## Garbage collection

> [!NOTE]
> Types of garbage collection:
> 
> * **reference counting**
>   * release the memory taken by an object when the ref count of this object falls to zero
>   * problem - cyclic references are invisible in this process
> * **tracing garbage collector**
>   * trace the objects step by step to see which ones are reachable from the program
>   * start with the most immediate objects reachable from the program (local function variables, global program variables, etc.), then go to the objects they're pointing to, then repeat, then repeat, then reapeat, ..., until you have no more objects, those objects that have not been reached can be deleted

> [!TIP]
> Python primarily uses reference counting for garbage collection.

> [!WARNING]
> Programming languages with automatic garbage collection are slower because they have additional garbage collection system running in the background, which consumes CPU cycles.

## Race conditions

> [!NOTE]
> **Race condition:**
>
> * a situation when a state of a variable is corrupted due to two independent flows of execution accessing the variable at the same time
> * for example, `thread 1` reads `x = 1` and doubles it getting `x = 2`, but `thread 2` at the same time also reads `x = 1` and halves it getting `x = 1/2`; the final result is the result of whatever thread finishes last and is therefore corrupted
> * note that the final result depends on the order of the threads accessing the data and finishing the operation
> * for example, `x + 2 * 2` is not the same as `x * 2 + 2`

## Compiled vs Interpreted

The source of the confusion is that people often confuse **the programming language itself** with **how an implementation of that language executes code**. A language is just a set of grammar rules; how it runs comes down to the tool executing it.

### 1. Compiled Languages

In a traditional compiled language (e.g., C, C++, Rust, Go), a compiler translates the human-readable source code directly into **machine code** (binary zeros and ones specific to your computer's CPU architecture).

* **How it works:** `Source Code (.c) → Compiler → Machine Code Executable (.exe / binary)`
* **Execution:** You run the binary file directly on the hardware. No extra translation happens at runtime.
* **Pros:** Extremely fast execution speed and low resource usage.
* **Cons:** Slower build times, and the binary is non-portable (an executable built for Windows x86 won't run on a Mac ARM chip).

### 2. Interpreted Languages

In a pure interpreted language (e.g., early Bash, original JavaScript, early BASIC), an interpreter reads the source code line by line (or statement by statement) and executes the requested actions on the fly.

* **How it works:** `Source Code → Interpreter (translates & executes line-by-line in real time)`
* **Pros:** Highly portable and easy to run immediately without a separate build step.
* **Cons:** Much slower because every line must be analyzed and translated every single time it runs.

### 3. Hybrid Languages (Bytecode + VM)

Most modern "interpreted" languages—including Python, Java, and C#—are actually **hybrid languages**. They combine compilation and interpretation into a two-step process to get the best of both worlds.

#### How Python Works (The "a little bit compiled" part):

When you run a Python file:

1. **Compilation Phase:** Python compiles your human-readable source code (`.py`) into an intermediate representation called **Bytecode** (`.pyc` files or cached in memory). Bytecode is an idealized, platform-independent instruction set—not machine code for your actual CPU.
2. **Interpretation Phase:** Python passes that Bytecode to the **Python Virtual Machine (PVM)** (specifically CPython, the standard Python interpreter). The PVM reads the bytecode step by step and translates it into native CPU instructions.

> **Why call Python "interpreted" then?**
> Because to the end user, there is no explicit compilation step (like running `gcc` in C). You type `python main.py`, and it executes immediately. The bytecode compilation happens seamlessly under the hood.

### 4. Just-In-Time (JIT) Compilation

Pure bytecode interpretation is faster than source code interpretation, but still significantly slower than native machine code. **JIT compilation** solves this gap.

A **JIT compiler** sits inside the virtual machine during execution and performs real-time optimizations:

1. As the bytecode runs through the interpreter, the JIT engine monitors which parts of the code are run most frequently (called **"hot spots"**, like long loops or heavy functions).
2. It takes those hot spots and **compiles them into native CPU machine code right on the fly** (just-in-time) in memory.
3. The next time that loop or function executes, the virtual machine skips the interpreter entirely and runs the lightning-fast native machine code directly.

| Language / Implementation | Intermediate Step | Runtime Engine / JIT |
| --- | --- | --- |
| **Java** | Source → Java Bytecode (`.class`) | Java Virtual Machine (JVM) + JIT (HotSpot) |
| **C#** | Source → CIL Bytecode | .NET Common Language Runtime (CLR) + JIT |
| **JavaScript** | Source → AST / Bytecode | V8 Engine (Node.js/Chrome) with JIT |
| **Standard Python (CPython)** | Source → Python Bytecode | PVM (Standard Interpreter, no full JIT*) |
| **PyPy (Alternative Python)** | Source → Python Bytecode | JIT-enabled Python Engine (up to 4–5x faster) |

**Note: CPython 3.11+ introduced a "specializing adaptive interpreter" that performs lightweight micro-JIT optimizations, but PyPy remains the primary full-JIT Python implementation.*

### Summary

* **Compiled:** Translated directly to native machine code *before* execution.
* **Interpreted:** Source code translated line-by-line *during* execution.
* **Hybrid:** Compiled first into intermediate **Bytecode**, then executed by a **Virtual Machine**.
* **Python:** A **hybrid** language. It compiles code into bytecode, then interprets that bytecode on its virtual machine.
* **JIT:** An enhancement in hybrid virtual machines that compiles heavily used bytecode into native machine code *while the program is running*.

# GIL

Most typical Python programs are single-threaded.

Even single-threaded program can perform concurrent tasks thanks to concurrency and async programming.

However, you can also perform concurrent tasks by assigning them to separate threads.

In theory, having a multi-core CPU with Y cores and X **software threads (threads defined in a program)** allows OS to map those X software threads to Y CPU cores such that Y **hardware threads (threads working on physical CPU cores)** actually work in parallel on Y different CPU cores.

In practice, Python (or should we say, CPython) has **GIL = Global Intepreter Lock**.

> [!IMPORTANT]
> **GIL is a mutex assigned to Python interpreter.**
> 
> Every software thread defined in Python source code has to acquire this mutex to get access to CPU to actually execute its code.
> 
> Interpreter is after all responsible for translating Python bytecode to CPU code.

> [!IMPORTANT]
> **This means that GIL, at any time, allows only one Python software thread to execute on the CPU which can be an undesirable restriction.**
> 
> It prevents several threads from executing at the same time and makes multi-threaded programs single-threaded in practice and also adds overhead (due to acquiring and releasing the lock on the interpreter).

> [!TIP]
> One way to get rid of GIL restriction is to create multiple Python processes instead of multiple Python software threads.
> 
> In your Python code you can create multiple Python processes where each process will get its own Python interpreter, i.e. its own GIL, and all processes will be able to run in parallel (assuming you have multiple CPU cores).
> 
> Processes are heavier and harder to manage than threads, though.

In CPython, for each Python thread the interpreter spawns a new C thread which has to run on the OS. All those C threads often have to access the shared data describing the state of the program, e.g. a table of variables (variable name -> variable value), reference counts, etc., Having a mutex for each single resource would be troublesome because it would be less performant and pose deadlock risks, so it was decided to use one, single, global mutex for all shared resources such that race conditions are prevented. After all, one mutex is faster than many mutexes and deadlock is impossible with only one lock.

> [!TIP]
> This global mutex is GIL and it was a design choice to use it instead of many local mutexes.

GIL prevents some race conditions related to interpreter and memory management (but not all race conditions). Without GIL (or without some other mechanism preventing race conditions), Python could for example wrongly conclude that an object needs to be deleted (due to corrupted reference count of this object).

Because GIL allows only one thread at a time and thus only one CPU core at a time, it is a performance bottleneck for programs which are CPU-bound (perform heavy CPU calculations), because normally such programs would be written as multi-threaded to take advantage of multiple CPU cores. But GIL effectively prevents multi-threaded programs in practice by making such programs single-threaded and running on a single CPU core. So, in practice, in multi-threaded programs, the threads basically have to switch and acquire GIL (mutex) one at a time and thus run one after another, not in parallel. Switching adds overhead in terms of additional operations performed.

> [!NOTE]
> For I/O-bound programs, the threads usually release the GIL when they are waiting, so GIL is not a performance bottleneck.
>
> In fact, many CPU heavy functions, e.g. numpy operations, I/O network operations (sleeping, sockets, etc.), voluntarily release GIL when they start executing operations.
> 
> This proves that Python's multi-threaded programs can be good for I/O-bound tasks, similarly as async programs.

*"The Python GIL is often regarded as a mysterious and difficult topic. But keep in mind that as a Pythonista you’re usually only affected by it if you are writing C extensions or if you’re using CPU-bound multi-threading in your programs."*

> [!IMPORTANT]
> GIL is being slowly removed from CPython (`v3.13` -> `v3.14` -> ...).

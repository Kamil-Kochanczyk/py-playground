# Low-level intro

> [!IMPORTANT]
> Program defines the sequence of instructions that CPU should execute.
>
> **Execution state** describes what is currently being executed.
> 
> It includes things such as:
> * **instruction pointer** (next instruction to execute)
> * **registers** (data buffers built directly into CPU, store temporary data related to the execution state, e.g. results of math operations)
> * **call stack** and **stack frames** (dedicated blocks of memory stored on the LIFO data structure that are used to store the information about the current function being executed, e.g. args/params, local vars, caller return address, caller's registers)
> * ...

> [!IMPORTANT]
> **Stack memory**:
> * structured memory (LIFO) usef for function calls, local and temporary data
> * automatically managed by CPU
> * fast (requires moving a pointer up or down the stack) but requires the size to be known at compile time (to adjust the pointer)
> * risk of stack overflow (exceeding the fixed size limit, e.g. due to recursion)
>
> **Heap memory**:
> * unstructured memory used for objects and global and persisting data (can be requested at any time and be basically of any size, limited only by RAM)
> * managed by a programmer (faster, requesting a memory block of size dynamically calculated at runtime based on things such as user input or reading a file) or by a system of garbage collection (slower, requires a background garbage collection system to run alongside your program)
> * slow (requires searching for a free block)
> * risk of memory leaks (if you forget to tell CPU that you're done with the particular memory block and don't need it anymore) and fragmentation
>
> Usually (for example in Python):
> * heap -> actual persisting data
> * stack -> temporary pointers to that actual persisting data

> [!IMPORTANT]
> **The Memory Hierarchy Levels** (Fastest to Slowest):
> 
> * **CPU Registers:** Built directly into the processor core, these hold data the CPU is actively processing right now. They offer near-zero latency (a fraction of a nanosecond) but have tiny capacity, usually measured in bytes.
> * **L1 Cache:** The fastest and smallest dedicated cache level, typically split into instruction and data caches. It takes less than 1 nanosecond to access and holds a few hundred kilobytes.
> * **L2 & L3 Caches:** Larger, slightly slower caches. L2 is usually dedicated to a single core, while L3 is larger and shared across all cores on the processor. Sizes range from a few megabytes (L2) to dozens or hundreds of megabytes (L3).
> * **Main Memory (RAM):** Dynamic RAM (DRAM) serves as the working memory for active programs and the operating system. It holds gigabytes of data (e.g., 16GB to 64GB+) with access times in the tens of nanoseconds. Contains stack and heap for program execution.
> * **Secondary Storage (SSD / HDD):** Non-volatile storage holding files and operating systems permanently. Solid-State Drives (SSDs) with electronic memory chips offer gigabytes to terabytes at microsecond speeds, while traditional Hard Disk Drives (HDDs) are slower mechanical devices.

> [!IMPORTANT]
> **Process**
>
> Process is an independent execution environment allocated by the operating system kernel, representing a running instance of a program.
>
> * **Virtual Address Space:** A process has its own isolated, private virtual memory space managed by the OS Memory Management Unit (MMU). It cannot directly access memory belonging to another process. This address space typically includes:
>   * **Text segment:** Compiled machine code (the actual instructions of the program).
>   * **Stack:** Function call frames and local variables (for the initial thread).
>   * **Heap:** Dynamically allocated memory requested on the fly.
> * **System Resources:** Owns a dedicated set of system resources, including file descriptors, network sockets, and environment variables.
>   * **File descriptors**: Integers, e.g. `0` for `stdin`, `1` for `stdout`, `2` for `stderr`, used by OS to keep track of what different processes (distinguished by their PIDs) do with the given file, if several processes want to write to the same file, a race condition can occur and locks are needed.
>   * **Network sockets**: They are also file descriptors, the pair `(IP, port)` should be managed by just one process at a time, otherwise multiple processes would get uncomplete parts of the full data being sent through the socket.
>   * **Environment variables**: Because a new child process being spawned (forked) from its parent process gets their own and independent and exact copy of the parent's system resources (or, actually, this "copy" is achieved via copy-on-write method), the env vars from the parent are passed to the child and can be overriden by the child at any time without affecting the parent's env vars.
> * **Kernel Data Structure:** Tracked by the kernel via a **Process Control Block (PCB)**, which stores its PID, state, priority, and resource pointers.
> * **Context Switch Overhead:** High. Switching between processes requires saving the CPU register state, etc.
> 
> The isolation of processes prevents the bug in one process to crash the other process or even the entire system.

> [!IMPORTANT]
> **Thread**
> 
> A **thread** (often called a lightweight process or LWP) is the smallest unit of execution that an operating system's scheduler can dispatch.
> 
> * **Shared Address Space:** All threads within a process share that process’s virtual memory space (text, data, and heap). This means pointers, global variables, and heap-allocated objects can be accessed directly by any thread in the same process.
> * **Private Execution Context:** While memory is shared, each thread maintains its own private execution state, which includes:
>   * **Thread ID (TID)**: Analogical to process's Process ID (PID).
>   * **Program Counter (PC):** Tracks the current instruction pointer.
>   * **Register Set:** CPU registers holding active values.
>   * **Private Stack:** Separate memory allocation for local variables, function parameters, and return addresses, preventing threads from overwriting each other's execution paths.
> * **Kernel Data Structure:** Represented by a **Thread Control Block (TCB)** linked to the parent PCB.
> * **Context Switch Overhead:** Low. Switching between threads of the same process does not require changing page tables (which are used in processes to map their virtual addresses to real physical addresses) or flushing the TLB (Translation Lookaside Buffer is a cache for looking up recent mappings between virtual and physical addresses), making thread context switches significantly faster than process switches.

> [!TIP]
> **Program** - passive, static set of textual instructions.
> 
> **Process** - active, running instance of a program managed by OS.

> [!TIP]
> **Process** = execution environment
> 
> **Thread** = execution flow

> [!TIP]
> **Process**:
> 
> * always has at least one thread (the main thread)
> * can have many threads (more than one)
> * sharing memory with other processes requires some data structures, such as pipes, queues, shared memory, etc., as well as mutual exlusion mechanisms, such as locks, mutexes, etc.

> [!TIP]
> **Thread**:
> 
> * shares some data with other threads inside the same process
> * has problems with race conditions and deadlocks as well as with blocking operations
> * instead of creating new thread for each task, you can predefine a fixed number of threads and assigned them to tasks stored in a FIFO queue

> [!IMPORTANT]
> **Segmentation fault (segfault)** is an access violation, an error raised by hardware when software tries to access a memory area that it is not allowed to touch
> 
> Typically, all processes are assigned their own allowed memory addresses. If the process tries to read or write outside those bounds—or tries to modify read-only memory—the hardware catches the illegal action and immediately stops the program by sending a signal.
>
> Typical causes: accessing the memory address pointed by a null pointer, accessing the memory of a non-initialized or a dangling pointer, stack overflow.

> [!IMPORTANT]
> A typical Python application cannot simply manipulate hardware however it wants. It request operations from the kernel.
> 
> Therefore the privileges for a typical Python application are lower (**user space**) than the privileges of the kernel (**kernel space**).

> [!IMPORTANT]
> **Scheduler**:
> * an OS program that decides which process or thread runs next on the CPU
> * **Long-Term Scheduler** (Job Scheduler): the slowest one, selects programs from the job queue (job pool) residing on secondary storage (SSD/HDD) and loads them into physical RAM (to the so-called ready queue) to create active processes, it controls the degree of multiprogramming (how many processes reside in RAM simultaneously), a balance of I/O-bound and CPU-bound processes is chosen here to maximize system efficiency (neither I/O devices nor CPU should be idle)
> * **Short-Term Scheduler** (CPU Scheduler): the fastest one, selects processes that are already loaded in the ready queue in physical RAM and assigns them a CPU core to execute their instructions, calls the dispatcher wchich is responsible for context switching
> * **Medium-Term Scheduler** (Swapper): temporarily removes active processes from physical RAM and writes them to a dedicated partition on secondary storage (known as swap space or a page file), reversing the process later, triggered when RAM is overloaded and needs to be temporarily freed up to accomodate for the needs of higher-priority tasks
>
> **Context switch**:
> * a mechanism that pauses one task (e.g. a process or a thread or a coroutine) and resumes another
> * happens when the **time slice** (**quanta**, the time period during which the task is assigned to the CPU) of the current task is expired or when the task blocks, or when a higher-priority task arrives, or when the control is voluntarily yielded (e.g. in asynchronous programming)
> * "context" refers to all the information the CPU needs to remember where a program left off, stored in a data structure called a Process Control Block (PCB) or Thread Control Block (TCB), including CPU Registers (active working values and data), Program Counter (the memory address of the next instruction to execute), and Stack Pointer (reference to local variables and function calls)
> * expensive (requires CPU overhead and is susceptible to cache misses due to caches being filled with data from the previous contexts)
>
> **Dispatcher**:
> * program which is resposible for performing the context switch (saving the state of the old task and loading the state of the new task)
> * triggered by short-term scheduler
> * it also transitions from kernel space (more hardware privileges) into user space (less hardware privileges)
>
> Together, they allow the CPU to create the illusion of executing many different programs simultaneously.

> [!IMPORTANT]
> **Preemptive scheduling**:
> 
> * OS can interrupt the current task and this task has nothing to say about it (the suspension of the task isn't voluntary)
> * The suspension is usually done via **hardware interrupt**, an electrical signal sent to the CPU by an external device.
> * Preemptive scheduling applies to threads managed by OS.

> [!IMPORTANT]
> **Cooperative scheduling**:
> 
> * The task voluntarily suspends its execution and yields the control to other tasks because it knows it can't continue right now but rather has to wait for sth before moving on.
> * Cooperative scheduling applies to async tasks managed by event loop (described later in the notes).

> [!IMPORTANT]
> **CPU-bound:**
> 
> * A task or program whose speed is limited by the **processing power of the CPU**. It spends most of its time performing heavy calculations, logic, or data manipulation, meaning performance improves directly with a faster or more powerful processor.

> [!IMPORTANT]
> **I/O-bound:**
> 
> * A task or program whose speed is limited by the **speed of input/output operations** (such as reading/writing to a disk, network requests, or database queries). The CPU spends most of its time idle, waiting for data to be transferred from external sources.

> [!IMPORTANT]
> **Blocking**:
>
> * blocking is a property of the execution mechanism, not simply of the fact that something takes time
> * for example, you can have a `sync_sleep(1000s)` function which puts the entire process's main thread to sleep and prevents it from doing any other tasks, or you can have a `async_sleep(1000s)` function which doesn't put the main thread to sleep and allows it to do other things until it gets a notification that the `async_sleep(1000s)` function finished its countdown
> * considering another example, performing heavy CPU calculations which take much time isn't usually "blocking", while performing the I/O operation from a socket which needs much time to get data from an external source can be "blocking" but doesn't have to be, i.e. can also be "non-blocking"

> [!IMPORTANT]
> **Blocking operation**:
>
> * in the context of I/O operations, it is an operation which makes the kernel put the thread to sleep so that it is paused and can't advance and doesn't do any other operations whatsoever until the operation gets what it needs to continue (the CPU can then switch from the blocked thread to other threads instead of doing **busy waiting**, i.e. constantly checking `while not_read(): is_ready()` and thus wasting CPU cycles)

> [!IMPORTANT]
> **Non-blocking operation**:
>
> * in the context of I/O operations, it is an operation where kernel immediately returns, either a result or an error indicating that sth is not ready yet (instead of halting the entire thread and putting it to sleep until it gets what it needs)

> [!TIP]
> "Waiting" can be understood differently. It can be a long CPU computation, a blocked thread, or an async suspension. These aren't equivalent.

> [!TIP]
> Creating a separate process or a separate thread for each task which is I/O-bound is an overkill - those processes/threads will spend most of their time waiting for the external data and doing nothing. Instead, a better approach would be to have one thread switching between multiple I/O-bound tasks.

> [!TIP]
> A **multiplexer** (**MUX**) combines multiple input signals into a single output line, while a **demultiplexer** (**DEMUX**) takes a single input signal and routes it to one of many output lines. 

> [!IMPORTANT]
> **I/O multiplexing** is a mechanism that allows single application to monitor multiple I/O sources for certain events, i.e. wait for certain events to occur on certain file descriptors. It's event-driven and controlled by hardware interrupts.
>
> An example of I/O multiplexing mechanisms is called **epoll**. It's a high-performance Linux kernel system call for scalable I/O event notification that allows a program to monitor thousands of file descriptors (such as network sockets) simultaneously to see if data can be read or written.
>
> It works like this:
> * first, create an **epoll instance** where you register all file descriptors that you want to monitor, this epoll instance consists of two data structures (red-black tree and linked list)
>   * **red-black tree** is a self-balancing binary tree and in the context of epoll instance it's used to store all monitored file descriptors and efficiently (with logarithmic time complexity) look up the specific file descriptor in case it's been marked as having a pending I/O event and should be added to the ready list, apart from that red-black tree also allows efficient (again, with logarithmic time complexity) addition and removal of monitored file descriptors
>   * **linked list** is also called **ready list** in this context and is used to store all file descriptors from the red-black tree which have a pending I/O event and can be processed by the interested processes/threads
> * after  that, you call epoll's wait function in the loop again and again
>   * every time you call this wait function the kernel checks if there are any file descriptors currently stored inside the ready list and if there are some (if the list isn't empty) it returns them all immediately (you can specify the max number, though), without waiting, i.e. it drains the ready list by simply copying the ready file descriptors to your program's main process/thread
>   * this copying operation involves moving the ready file descriptors from the kernel space (where epoll is handled) into the user space of your program (where epoll is used as an I/O multiplexing mechanism) without any linear-time-complexity scanning of all registered file descriptors
>   * if the ready list is empty, the main process/thread is put to sleep and added to the wait queue corresponding to the epoll's wait function
>   * this wait queue isn't the same wait queue as the wait queue described in the next paragraph which corresponds to a single file descriptor and not to epoll's wait function
>   * in the wait queue corresponding to epoll's wait function the callback function is the main process/thread itself, in the other wait queue the callback function is the epoll's custom callback function which works on the ready list, as will be described in the next paragraph
> * now whenever a data arrives on the monitored file descriptor (network socket), a hardware interrupt is sent and a callback function is executed via hardware interrupt handler, this callback function simply checks if the given file descriptor is already in the ready list and if it's not there, it's added to the ready list
>   * by default all file descriptors in Linux have an associated wait queue containing all user space processes/threads waiting (sleeping) for an I/O event related to this file descriptor and the callback function is a function which wakes the user space processes/threads in that wait queue
>   * in the case of epoll, this default user space callback function is replaced with epoll's kernel space callback function which operates on epoll instance's ready list and thus never leaves kernel space which makes it very efficient
>   * note that when many network sockets receive data at approximately the same time, the ready list can contain multiple file descriptors (`[socketA, socketB, socketC, ...]`) and the callback function which drains the ready list and wakes up the main process/thread waiting on epoll's wait function can therefore provide those multiple ready file descriptors to the main process/thread in one go, in a batch of a given size
>   * even though each callback function which appends items to the ready list also tries to immediately wake up the main process/thread, it doesn't mean that ready list will always contain only one item when it's requested by the main process/thread
>     * this is because even though the main process/thread becomes possible to run, it doesn't mean it'll run immediately (because of non-deterministic scheduling of OS's scheduler) and thus when the main process/thread waits for its execution, the ready list can grow larger and larger in the meantime
>     * another reason for this is that while your main process/thread does its work and tries to eventually reach the next call of the epoll's wait function in the loop, the kernel can still work in the background and add multiple items to the ready list which will all be returned the next time the epoll's wait function is called

> [!TIP]
> **Readiness notification model**:
>
> ```
> Application:
>     "Can I read from this?"
> 
> OS:
>     "Yes."
> 
> Application:
>     read()  # non-blocking
> ```

> [!TIP]
> **Completion notification model**:
>
> ```
> Application:
>     "Read this data."
> 
> OS:
>     "Okay."
> 
> ...
> 
> OS:
>     "The read completed. Here's the result."
> 
> Application:
>     get_result()  # non-blocking
> ```

> [!IMPORTANT]
> **Race Condition:**
> 
> * An undesirable situation that occurs when a system or program attempts to perform two or more operations at the same time, but the outcome depends on the improper or unpredictable sequence/timing of those operations (e.g., two threads modifying the same variable without proper synchronization, leading to corrupted data).
> 
> **Atomicity (Atomic Operation):**
> 
> * The property of an operation being entirely completed or not performed at all, with no intermediate state visible to other threads or processes. It is indivisible and interrupt-safe, meaning it cannot be partially executed. Prevents race conditions and data corruption.
>
> To prevent race conditions atomicity is achieved by mechanisms such as **locks** or **mutexes** (mutexes are one type of locks) which mark the **critical sections** of the code as undivisible units of execution. This, however, causes problems such as **deadlocks** (neither task can proceed because they are all waiting for one another) or **starvation** (one task is CPU-greedy and doesn't let other tasks to proceed).

> [!IMPORTANT]
> **Concurrency**:
>
> * **rapid switching between different, multiple tasks on one CPU core**
> * **typically managed by one thread** (many threads also possible)
> * imagine you're a CPU thread: you execute `Task A` -> `Task A` needs to wait for sth and you don't know how long it will take to get it so `Task A` halts its execution voluntarily and saves its state to resume later -> `Task A` doesn't block you and allows you to do other stuff instead -> you can do some other `Task B` -> ... -> you receive an event that you got what `Task A` was waiting for and you set `Task A` as *"ready to resume"* in the future (when you have time to do so) -> `Task A` is eventually resumed and continues from the previously saved state
> * this way concurrency allows performing and advancing multiple tasks simultaneously, in **overlapping time periods** (because multiple tasks can wait simultaneously while you're doing some other things)
> * switching between tasks and advancing them is called **interleaving** (note that even though you do `A1` -> `B1` -> `A2` -> `B2`, the sequential order inside individual tasks `A` and `B` remains correct, i.e. `A1` is before `A2` and `B1` is before `B2`)

> [!IMPORTANT]
> **Parallelism**:
>
> * **executing multiple tasks at the exact same physical time instance** (at the same clock tick)
> * **requires multiple CPU cores** (contrary to concurrency which can be achieved on one CPU core), i.e. is also dependent on hardware design, not only on software design
> * **parallelism is a subset of concurrency**, i.e. any parallel system is inherently concurrent because multiple execution contexts are active simultaneously

> [!IMPORTANT]
> **Synchronous programming**:
> 
> * Tasks run one at a time in a specific order (sequentially).
> * Each operation must finish completely before the program can move on to the next one, which can cause the program to block or freeze while waiting for slow tasks (like file or network requests).

> [!IMPORTANT]
> **Asynchronous programming**:
>
> * Out of order execution of certain tasks (a task is initiated and the program immediately moves on to other tasks, handling the result later once the task finishes).
> * Non-deterministic order of execution of different tasks, it's not random but rather dependent on timing and OS scheduling internals like priorities, etc.
> * It involves quick switching between different logical tasks (logical flows of tasks).
> * *"I controllably and voluntarily yield control back so that others can proceed with their work while I wait for my turn."*

> [!IMPORTANT]
> **Event loop**:
>
> * The central mechanism used to implement asynchronous programming.
> * The crucial insight is that asynchronous programming is single-threaded concurrency. There is only one thread doing the work. Instead of waiting for a slow disk read or network request to finish (which would block a traditional thread), the event loop registers the request with the OS, moves on to other tasks, and comes back only when the OS signals that data has arrived.
> * Apart from that event loop also handles timers and their callbacks for things such as scheduled sleep time (e.g. `asynctio.sleep(5)`) or scheduled function calls (e.g. `loop.call_soon(func)` or `loop.call_later(func, 5)`) or HTTPS connection timeouts.
> * Event loop is non-blocking.
> * See the simplified pseudocode below for the mental model of the event loop.

```
// ==========================================
// Event Loop (Pseudocode)
// ==========================================

initialize EventLoop:
    ready_queue = Queue()            // Tasks ready to run right now
    timers = PriorityQueue()         // Timers sorted by expiration time (min heap, i.e. the closest deadline first)
    poller = OS_Poller()             // Low-level OS notification mechanism (e.g., epoll)
    is_running = False

// ------------------------------------------
// 1. Adding Work to the Loop
// ------------------------------------------

// I/O-driven tasks
function schedule_task(coroutine):
    ready_queue.push(coroutine)

// Time-driven tasks
function call_later(delay_seconds, callback):
    expiration_time = current_time() + delay_seconds
    timers.push((expiration_time, callback))

// ------------------------------------------
// 2. The Core Engine (The While Loop)
// ------------------------------------------
function run():
    is_running = True
    
    while is_running:
        // Stop if there is completely no work left to do
        if ready_queue.is_empty() and timers.is_empty() and poller.is_empty():
            break

        // --- Step A: Determine Polling Timeout ---
        // If there are timers, we shouldn't wait forever in the OS poller for very slow network packages to arrive.
        // We must wake up in time to trigger the next timer callback.
        timeout = calculate_next_timer_timeout(timers)

        // --- Step B: Wait for I/O (Blocking efficiently) ---
        // The OS puts this thread to sleep until a file descriptor is ready 
        // OR the closest timeout expires (whichever comes first).
        // This uses 0% CPU while waiting!
        io_events = poller.poll(timeout)

        // --- Step C: Process I/O Events ---
        for event in io_events:
            task = event.get_associated_task()
            ready_queue.push(task)

        // --- Step D: Process Expired Timers ---
        while not timers.is_empty() and timers.peek().expiration_time <= current_time():
            timer = timers.pop()
            ready_queue.push(timer.callback)

        // --- Step E: Run Ready Tasks ---
        // Drain the ready queue for this cycle
        current_batch_size = ready_queue.size()
        for i from 0 to current_batch_size:
            task = ready_queue.pop()
            
            // Execute the task until it hits the next 'await' or finishes
            status = task.step() 

            if status == "PENDING":
                // Task hit an 'await' on an incomplete operation (e.g., network socket).
                // The task has already registered itself with the 'poller' or with the timer to wake up later.
                pass
            
            else if status == "COMPLETED":
                // Task is done. Clean up resources.
                cleanup_task(task)

// ------------------------------------------
// 3. Stopping the Loop
// ------------------------------------------
function stop():
    is_running = False
```

> [!IMPORTANT]
> **Async task** isn't the same as thread, it's an object managed by the event loop, not by OS.

> [!WARNING]
> The non-deterministic nature of async scheduling can be the cause of problems with debugging async programs (adding `print` statement for debugging can change async order of execution and thus hide the bug).

> [!WARNING]
> A timer deadline doesn't mean the callback executes at exactly that instant. When a deadline is reached, the callback is added to the ready queue and is EVENTUALLY executed by the event loop.

> [!TIP]
> Asynchronous programming is good for I/O-bound tasks but not good for CPU-bound tasks (because CPU-bound tasks can completely monopolize the event loop thread with long running CPU work).

> [!TIP]
> OS scheduler decides: which thread to run next on the CPU?
>
> Event loop decides: which async task gets executed now by the event loop thread?

> [!IMPORTANT]
> **Generator**:
>
> * An object designed to produce values over time.
> * It can yield values sequentially, e.g. `enter generator -> computations... -> yield A -> give control back -> ... -> enter generator -> computations... -> yield B -> give control back -> ...`, etc.
> * Its big advantage is that it saves memory by yielding only single values, one at a time, instead of all at once.

> [!IMPORTANT]
> **Coroutine**:
>
> * Coroutine is a computation flow whose execution can be suspended and later resumed, potentially multiple times, while preserving its execution state.
> * Unlike "normal" functions, which once called must either finish execution and possibly return some value or they block the thread while waiting for sth to finish their execution, coroutines can yield control back to other callers and preserve their state so that they can be later resumed.
> * Suspension can be represented as a transition from one execution state to another, with enough information preserved to continue later. This is why a coroutine is often described as a special kind of a state machine.
> * In Python a coroutine is a function defined with `async def`. It's basically a blueprint for a resumable function call.
> * When you try to call such `async def` function, its code isn't immediately executed. Instead, calling `async def` function creates a coroutine object which is a special object designed to be managed by the event loop (awaitable object).
> * Such coroutine object can be advanced by the event loop to execute its code until `await` is encountered. At this point the code being executed pauses, its state is saved and the control is given back to the event loop because the coroutine object uses `await` to mark the point where the waiting for some external data or for some timer needs to take place before moving on.
> * The code after `await` is executed once the data arrives (e.g. network data) or once the timer expires (e.g. `asynctio.sleep()`). This code after `await` in the original coroutine can thus be viewed as a callback function.
> * This proves that `async def` and `await` is just a syntactic sugar for the callback funtion syntax which makes it easier to write clear and readable asynchronous programs as if they were synchronous programs, without the risk of callback hell (where multiple callback functions are deeply nested within one another greatly reducing the readability of the code).
> * Because coroutines often yield control back, just like generators, while preserving their state, they are sometimes called generator-like state machines.

> [!TIP]
> **yield**: *"here's a value, I give control back to you, you can resume me later and I'll give you another value"*
>
> **await**: *"suspend me, I give control back to you and I'll execute the rest of my instructions once I get what I need"*

> [!TIP]
> Suspended coroutines can be nested and wait for multiple conditions to occur before moving on, thus forming a dependency graph.

> [!IMPORTANT]
> **Task** (in Python):
>
> * Its' a wrapper around the particular coroutine, managed by the event loop.
> * A subclass of Future that is specifically designed to wrap and manage the execution of a coroutine. Tasks are used to run coroutines concurrently, allowing you to cancel them, check their status, and retrieve their results when they complete.

> [!IMPORTANT]
> **Future** (in Python):
>
> * Low-level object representing the eventual result of an operation.
> * It is not tied to a specific coroutine; rather, other code can set its result or exception manually when ready.

> [!TIP]
> Note that context switch between tasks is simpler and faster than context switching for processes or threads.

> [!TIP]
> `asyncio.run()` is completely synchronous from the caller's perspective. To normal Python code, calling `asyncio.run()` is just a regular function call. Python pauses at that line, creates a brand new event loop on the main thread, runs your async tasks to completion, shuts down the event loop, and then continues to the next synchronous line of code. After that you can call `asyncio.run()` again to create another event loop, and so on. You cannot create nested event loops, however, as this probably wouldn't make much sense.

> [!TIP]
> In Python:
> 
> * `await coroutine()`
>   * the control goes directly into the `coroutine()`
>   * the event loop does not schedule a separate task, execution enters the coroutine immediately, pausing the caller until this inner coroutine completes
> * `await create_task(coroutine())`
>   * the control is given back to event loop and `coroutine()` is advanced when the event loop has time to do so
>   * the coroutine is scheduled immediately as an independent task on the event loop, it can run concurrently the next time control is yielded back to the event loop

> [!TIP]
> **Queue** (in Python's asyncio):
> * a FIFO data structure used to pass data between concurrent tasks
> * tasks producing the data are called producers, while tasks consuming the data are called consumers
> * producers await until they can put data into the queue (e.g. while the queue is full), while consumers await until they can get data out of the queue (e.g. while the queue is empty)
> * advantages:
>   * producer-consumer pattern (e.g. scraping web data and then processing it at unpredictable rates)
>   * decoupling code logic (producers generate data while consumers process data)
>   * backpressure (flow control, setting max size for queue prevents the application from running out of memory)

> [!TIP]
> **Semaphore** (in Python's asyncio):
> * internal counter which increments when the task releases it and decrements when the task acquires it
> * limits how many coroutines can access a specific resource or run a specific block of code at the exact same time
> * use cases:
>   * limitting how many tasks can make an API call to a server (prevents you from getting banned due to exceeding the server's concurrency limit)
>   * limitting how many tasks can open a connection to a database, file handles or network sockets simultaneously

> [!TIP]
> `async for`:
> 
> * in Python, it creates an asynchronous for loop
> * this asynchronous for loop doesn't iterate over some ready iterable stored inside memory but rather iterates over items that appear one at a time, step by step, coming for example from an external source (e.g. network bytes), at unknown time instants
> * while the asynchronous for loop waits for the next item of its iterable so as to advance its iterator, it gives control back to the event loop, allowing it to do other tasks and returning to the next item only when it's ready
> * iterating over items one at a time consumes less memory than "normal" for loop which stores all items to iterate over in the memory and processes them without waiting

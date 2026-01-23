## i/o bound
An I/O-bound process or task is one whose overall execution time is determined principally by the speed of input/output (I/O) operations, rather than the speed of the central processing unit (CPU). The process spends most of its time waiting for external operations to complete. 

# Key Characteristics
Bottleneck: The performance bottleneck is the I/O subsystem (e.g., disk, network, memory bus).

CPU Usage: The CPU is often idle or underutilized while the program waits for data transfer to finish.

Performance Improvement: The program would run faster if the I/O subsystem were faster (e.g., a faster hard drive or network connection), but upgrading the CPU would have minimal impact.

Contrast with CPU-bound: A CPU-bound task is limited by the CPU's processing power and would run faster with a faster CPU. 

# difference between multiprocessing/ multithreading
 key difference: multiprocessing offers true parallel execution across multiple cores, while multithreading offers concurrency within a single core or parallelism if multiple cores are available. 
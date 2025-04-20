# Expected Behavior Formalization for Simulation Test Cases

This document outlines the expected behavior of the system under different test cases defined in `simulation/test_cases.py`.

## Notation

-   `N`: Total number of tasks (`NUMBER_OT_TASKS`)
-   `S`: Number of subtasks per task (`TASK_SIZE`)
-   `M`: Number of microservices
-   `lambda_task`: Arrival rate of tasks (tasks per unit time). For Poisson arrivals, this is `1/lamdb`.
-   `lambda_packet`: Arrival rate of packets (packets per unit time).
-   `mu_i`: Service rate of microservice `i` (subtasks per unit time). Service times follow a log-normal distribution derived from an exponential distribution with mean `1/mu_i`.
-   `interval`: Constant time interval between task arrivals (Case 1).
-   `lamdb`: Mean of the Poisson distribution for inter-arrival times (Cases 2-5). Note that the *rate* is `1/lamdb`.
-   `T_arrival,k`: Arrival time of the k-th entity (task or packet).
-   `T_service,j`: Service time for the j-th subtask.
-   `T_wait,j`: Waiting time for the j-th subtask in the microservice queue.
-   `T_proc,j`: Processing time for the j-th subtask (`T_wait,j + T_service,j`).
-   `T_task,k`: Total processing time for task `k` (time from first subtask arrival at LB to last subtask completion at Aggregator).
-   `p_fail`: Probability of a server failing before processing a subtask (`FAIL_PROB`).
-   `lambda_down`: Rate of server recovery after failure (`TIME_DOWN_LAMBDA`). Mean downtime is `1 / lambda_down`.
-   `rho`: System load or traffic intensity, generally defined as (Total Arrival Rate of Subtasks) / (Total Service Rate of Subtasks) = `(lambda_task * S) / (M * mean(mu))`.

## Test Cases Analysis

### 1. Constant Interval, Fixed Packets (`ConstIntervalFixPacketsTask`, No Failures)

-   **Task Arrival:** Deterministic. Tasks arrive exactly `interval` time units apart. `T_arrival,k = k * interval`.
-   **Packet Structure:** One packet per task, containing all `S` subtasks.
-   **Packet Arrival Rate:** `lambda_packet = 1 / interval`.
-   **Expected Behavior:**
    -   This scenario represents the most predictable input.
    -   Arrival times have zero variance.
    -   System performance (queue lengths, task completion times) depends critically on the load `rho = S / (M * interval * mean(mu))`.
    -   If `rho < 1`, the system should be stable. Queueing delays will occur if `S/M` subtasks cannot be processed within `interval` time units on average.
    -   Task processing times should exhibit relatively low variance, primarily driven by the log-normal service time distribution.

### 2. Random Interval, Fixed Packets (`RandIntervalFixPacketsTask`, No Failures)

-   **Task Arrival:** Poisson process. Inter-arrival times `~ Exp(1/lamdb)`. `lambda_task = 1 / lamdb`.
-   **Packet Structure:** One packet per task, containing all `S` subtasks.
-   **Packet Arrival Rate:** `lambda_packet = 1 / lamdb`.
-   **Expected Behavior:**
    -   Arrival times are random, following a Poisson process. This introduces variability (burstiness).
    -   Load `rho = (lambda_task * S) / (M * mean(mu))`.
    -   Compared to Case 1, the randomness in arrivals will likely lead to longer average queue lengths and higher variance in task processing times, even for the same average load `rho`.
    -   The system behaves like M parallel M/G/1 queues (approximately, due to LB and Aggregator).

### 3. Random Interval, Ordered Random Packets (`RandIntervalOrderedRandPacketsTask`, No Failures)

-   **Task Arrival:** Tasks are conceptually generated according to a Poisson process with rate `lambda_task = 1 / lamdb`.
-   **Packet Structure:** Each task is split into multiple packets (`k_i` packets for task `i`). Subtasks within a packet belong to the same parent task. Packets for a given task arrive sequentially.
-   **Packet Arrival:** Poisson process for *packets*. The inter-arrival times are scaled: `~ Exp( (1/lamdb) * (N / N_packets_total) )`. The average packet arrival rate `lambda_packet` is higher than `lambda_task`.
-   **Expected Behavior:**
    -   Subtasks from the same task arrive spread out over time.
    -   This might smooth the load on individual microservices compared to Case 2, potentially reducing peak queue lengths.
    -   However, the total task completion time (`T_task,k`) is now dependent on the arrival and processing of the *last* packet of the task. This can increase the average `T_task,k` compared to Case 2, as the task duration is elongated by the packet arrival process itself.
    -   The aggregator must wait for all `S` subtasks, which arrive over a longer duration.

### 4. Random Interval, Non-Ordered Random Packets (`RandIntervalNotOrderedPacketsTask`, No Failures)

-   **Task/Packet Arrival:** Same as Case 3 regarding rates and splitting.
-   **Packet Order:** Packets from all tasks are pooled and subjected to a *weighted shuffle*. This means packets from the same task are likely, but not guaranteed, to arrive close together, and their original order is not preserved.
-   **Expected Behavior:**
    -   Similar packet arrival statistics and load smoothing potential as Case 3.
    -   The primary difference is the packet ordering. The weighted shuffle introduces additional randomness in the sequence of subtask arrivals at the aggregator for a given task.
    -   This might slightly increase the variance in `T_task,k` compared to Case 3, as the aggregator might wait longer for specific "straggler" subtasks arriving out of sequence. The impact depends on the effectiveness and bias of the shuffle.

### 5. Random Interval, Non-Ordered Random Packets with Failures (`RandIntervalNotOrderedPacketsTask`, With Failures)

-   **Task/Packet Arrival:** Same as Case 4.
-   **Server Behavior:** Microservices can fail with probability `p_fail` before processing a subtask. Downtime follows `~ Exp(lambda_down)`.
-   **Expected Behavior:**
    -   Server failures introduce significant disruptions.
    -   **Reduced Capacity:** The effective service rate of the system decreases. The average available service rate per server is approximately `mu_i * (1 - p_fail * (1 / lambda_down) / (T_up + 1/lambda_down))`, where `T_up` is the average time between failures for a busy server. A simpler view is that capacity is lost during downtime.
    -   **Increased Delays:** Subtasks assigned to a failed server experience significant delays (waiting for recovery).
    -   **Higher Variance:** Both `T_proc,j` and `T_task,k` will have much higher averages and variances compared to Case 4.
    -   **Load Balancer Impact:** The 'least-loaded' (ll) balancer might perform poorly if servers fail frequently, as load might concentrate on remaining servers or queues might build up behind failed ones.
    -   The system becomes unstable at lower traffic intensities (`rho`) compared to the no-failure cases.

lnu-suite — Linux Network Utility Suite
A Linux-first CLI toolset for safe, high-performance network scanning, system monitoring, and process management, designed for infrastructure engineers.

This project is a functional prototype. See the Roadmap section for future development plans.

WARNING
Only run network scans against hosts you own or have explicit permission to test. Unauthorized scanning may be illegal.

Quickstart & Demo
Follow these steps to set up and run the automated demo of the current version.

# 1. Clone the repository
git clone [https://github.com/your-username/lnu-suite.git](https://github.com/your-username/lnu-suite.git)
cd lnu-suite

# 2. Set up the environment and build the tools
chmod +x scripts/run.sh

# 3. Run the automated demo
./scripts/run.sh

The demo will showcase the system monitor, TCP port scanner, and the compiled C++ utility. Output logs can be found in the logs/ directory.

Current Features (Phase 1 Prototype)
System Monitor (lnu/monitor.py): Samples CPU, memory, disk, and network I/O using psutil and logs to a .jsonl file.

TCP Scanner (lnu/scan.py): A concurrent port scanner using a ThreadPoolExecutor for high performance, featuring banner grabbing and JSON report generation.

Process Manager (cpp/lnu_proc.cpp): A C++ utility for Linux systems that lists running processes by parsing the /proc filesystem.

Professional Roadmap & Future Work
This project was designed with a professional feature set in mind. The following is a high-level roadmap for developing this prototype into a production-grade utility suite.

Core Engine Rewrite (C++):

Implement a high-concurrency scanning engine using non-blocking sockets with epoll for superior performance.

Expand the process manager with full POSIX signal handling for graceful shutdowns and process restart policies.

Expose key performance metrics (e.g., connections/sec, latency histograms) via a Prometheus /metrics endpoint.

Advanced Scan Capabilities:

Add privileged SYN (half-open) and UDP scan modes, using raw sockets and setcap for capability management instead of requiring full root.

Develop a pluggable scanner architecture to easily add new application-level probes (e.g., for TLS, DNS, SSH).

Linux Integration & Packaging:

Provide a systemd unit file for running the monitor as a persistent background service (lnu daemon).

Create robust packaging, including a multi-stage Dockerfile for containerized deployment and a Debian package (.deb) for easy installation on Ubuntu/Debian systems.

Rust Integration (Proof-of-Concept):

Explore using Rust for performance-critical and memory-safe components, such as a packet parsing module, exposed to the C++ core via a clean FFI boundary.

This roadmap demonstrates a commitment to building secure, performant, and operationally mature systems software.

License
This project is licensed under the MIT License.


**Action:** After pasting this, save the file, and push the change to your GitHub repository immediately.

```bash
git add README.md
git commit -m "docs: upgrade README with professional roadmap and future work"
git push

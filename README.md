# HDL Flow Studio

**HDL Flow Studio** is a lightweight, Tcl-driven FPGA project simulator and manager built for fast prototyping, logic testing, and automated simulation. Inspired by tools like Vivado, it provides a clean GUI and scripting interface for managing VHDL files, testbenches, and simulation results.

---

## 🧠 Features

- ✅ Tcl-based build flow: `--simulate`, `--simulate-all`, `--full`, `--clean`, `--bitstream-only`
- ✅ GUI simulator with:
  - File explorer (sources, logs, tests, reports)
  - Module dropdown simulation
  - "Simulate All Modules" support
  - In-place editing with Save
  - Double-click to open in default editor
  - Auto-refresh preview on file change
- ✅ Custom logic engine in Python:
  - Supports `and`, `or`, `not`, `xor` logic
  - Reads `.vhdl` + `.json` test pairs
  - Pass/fail output with summary

---

## 🗂️ Project Structure

- `build_project.tcl` – Main flow script (`--simulate`, `--full`, etc.)
- `gui_simulator.py` – GUI frontend (Tkinter-based)
- `sim/`
  - `simulate.py` – Logic simulation engine (Python)
- `sources/` – Your `.vhdl` files
- `tests/` – Input vectors in JSON format
- `logs/` – Simulated synthesis logs
- `reports/` – Output summaries and bitstreams
- `README.md`

---

## 🛠️ How to Use

### 📦 Installation

Clone the repository:

```bash
git clone https://github.com/0khat0/hdl-flow-studio.git
cd hdl-flow-studio

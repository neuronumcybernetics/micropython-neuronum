<h1 align="center">
  <img src="https://neuronum.net/static/neuronum.svg" alt="Neuronum" width="80">
</h1>
<h4 align="center">CHANGELOG of the Neuronum MicroPython Library</h4>

<p align="center">
  <a href="https://neuronum.net">
    <img src="https://img.shields.io/badge/Website-Neuronum-blue" alt="Website">
  </a>
  <a href="https://github.com/neuronumcybernetics/micropython-neuronum">
    <img src="https://img.shields.io/badge/Docs-Read%20now-green" alt="Documentation">
  </a>
  <a href="https://github.com/neuronumcybernetics/neuronum/blob/main/LICENSE.md">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
</p>

---

## 🚀 Version 0.1.0
### Added
- `store()` function for storing data in a circuit context
- `load()` function for retrieving data from circuit context
- `activate_tx()` function for authenticated TX data push

### Changed
- Refactored `stream()` to validate acknowledgment from receiver before completing transmission

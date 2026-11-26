<!-- Hero -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a0000,25:4a0000,50:8B0000,75:4a0000,100:1a0000&height=180&section=header&text=Bharath%20Chandra&fontColor=ffffff&fontSize=42&animation=fadeIn&fontAlignY=35&desc=Performance-first%20systems%20%E2%80%A2%20GPU%20runtimes%20%E2%80%A2%20Research&descAlignY=55&descSize=18" alt="Bharath Chandra banner" width="100%"/>
  <br />
  <br />
  <p><strong>ML systems engineer · Founder at <a href="https://scholarlm.dev/">ScholarLM</a></strong></p>
  <p>I make ML and developer infrastructure fast, and I prove it with numbers: Metal GPU kernels, Rust and Go runtimes,<br/>and code-intelligence tools for AI agents, built as modules that every new project reuses.</p>
  <p><b>Open to opportunities</b> · <a href="mailto:bharath@vbcr.dev">bharath@vbcr.dev</a> </p>
  <br />
  <a href="https://www.linkedin.com/in/bharath-vbcr/"><img src="https://img.shields.io/badge/LinkedIn-8B0000?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>&nbsp;<a href="https://bharath.vbcr.dev/"><img src="https://img.shields.io/badge/Portfolio-bharath.vbcr.dev-8B0000?style=for-the-badge&logo=safari&logoColor=white" alt="Portfolio"/></a>&nbsp;<a href="https://scholar.google.com/citations?user=7sP8mBIAAAAJ&hl=en"><img src="https://img.shields.io/badge/Google_Scholar-6B0000?style=for-the-badge&logo=google-scholar&logoColor=white" alt="Google Scholar"/></a>
  <br /><br />
  <img src="https://visitor-badge.laobi.icu/badge?page_id=bharathvbcr.bharathvbcr&left_text=PROFILE%20VIEWS&left_color=1a0000&right_color=8B0000" alt="Profile Views"/>
  <br /><br />
  <img src="https://img.shields.io/badge/GPU_Kernels-8B0000?style=flat-square" alt="GPU Kernels" />&nbsp;<img src="https://img.shields.io/badge/Rust_%C2%B7_Go_Runtimes-6B0000?style=flat-square" alt="Rust and Go Runtimes" />&nbsp;<img src="https://img.shields.io/badge/Code_Intelligence-4a0000?style=flat-square" alt="Code Intelligence" />&nbsp;<img src="https://img.shields.io/badge/Falsifiable_Research-8B0000?style=flat-square" alt="Falsifiable Research" />
</div>

---

## At a glance

- **Now:** founder and sole engineer of [ScholarLM](https://scholarlm.dev/), an AI research platform (React 19, Rust, Go and Python) that writes fully-cited, grounded manuscripts (**97.7%** [`85/87`] precision on public LitQA2 without a supplied paper corpus). In parallel I build the Apple-silicon GPU, Go↔Rust contract, and code-intelligence stack below.
- **Strongest results:** an Apple-silicon Metal 4 runtime running EmbedGemma 2 **3.06–4.37× faster** than PyTorch MPS (fitting 4K–6K ragged workloads in ≤1,911 MiB where PyTorch OOMs at 33.6 GiB) and pure-Rust **TimesFM 3** forecasting **4.3× faster** than PyTorch MPS eager (`479.5 → 111.3 ms`), LoRA activation checkpointing and weight-gradient skipping cutting Metal peaks **−78%** and **−44%**, MANVI batching + Starlark scripting cutting coding-agent input tokens **245,117 → 110,621 (−54%)** and steps **9.63 → 4.69** across **600 pre-registered runs**, a code-graph indexer **1.6–21× faster** than four rival tools, Waylode (formerly GitPulse) cutting 30k-commit refresh to **1.11 ms** (`25.19 → 1.11 ms`) and watcher wakeups **117.3 → 2.7/s**, and a Go↔Rust call made **8.5× cheaper**.
- **Before:** Associate Researcher at the Adidas Center for Engagement Science (ASU, 2023–2025), and stem-cell research at Texas Tech University Health Sciences Center.
- **Education & papers:** M.S. Biomedical Engineering, Arizona State University (2024) · 2 peer-reviewed papers (2025).
- **Upstream:** Initiated the official Eclipse `iceoryx2` Go bindings ([`eclipse-iceoryx/iceoryx2-go`](https://github.com/eclipse-iceoryx/iceoryx2-go): proposal, repo provisioning, first PR under review); merged patches in [`rust-lang/libc`](https://github.com/rust-lang/libc/pull/5609) (`0.2.191`) and [`objc2`](https://github.com/madsmtm/objc2/pull/870); Apple Silicon MPS `NaN` diagnosis & reproducer in [`decider-ai`](https://github.com/Mapika/decider/issues/21) (`1.8.2`).

---

## Upstream

- **[Eclipse iceoryx2](https://github.com/eclipse-iceoryx/iceoryx2)** — proposed and scaffolded the official Go bindings in [`eclipse-iceoryx/iceoryx2-go`](https://github.com/eclipse-iceoryx/iceoryx2-go) ([#225](https://github.com/eclipse-iceoryx/iceoryx2/issues/225), [#2104](https://github.com/eclipse-iceoryx/iceoryx2/issues/2104)). Provisioned the repository and branch rulesets with the project leads ([.eclipsefdn#28](https://github.com/eclipse-iceoryx/.eclipsefdn/pull/28)) and built the Step 1 `NodeBuilder` → `Node` `cgo` package over the `iceoryx2-ffi` C API with a release-pinned `iceoryx2` submodule (`iox2_*_storage_t` ABI parity), `golangci-lint` v2, and Go 1.26/1.27 Linux/macOS `-race` CI, now open for review as [PR #1](https://github.com/eclipse-iceoryx/iceoryx2-go/pull/1) (first validated on [the fork](https://github.com/bharathvbcr/iceoryx2-go/pull/1)). Committer election follows a review track record; the binding is not published yet.
- **[rust-lang/libc](https://github.com/rust-lang/libc)** — added Apple `F_SETNOSIGPIPE` (`73`) and `F_GETNOSIGPIPE` (`74`) ([#5609](https://github.com/rust-lang/libc/pull/5609)), shipped in `libc 0.2.191`. Upstreamed from completion-pipe `SIGPIPE` suppression in [Gusset](https://github.com/bharathvbcr/gusset).
- **[objc2](https://github.com/madsmtm/objc2)** — marked `MTLTensorDescriptor` consumers `unsafe` in `objc2-metal` ([#870](https://github.com/madsmtm/objc2/pull/870), [#782](https://github.com/madsmtm/objc2/issues/782), found while building Metal 4 tensor ops in [tessl](https://github.com/bharathvbcr/tessl)): Metal segfaults on a nil stride or an oversized tensor instead of returning an error. Also restricted the AppKit examples to macOS ([#871](https://github.com/madsmtm/objc2/pull/871)).
- **[Mapika/decider](https://github.com/Mapika/decider)** (`decider-ai`) — diagnosed `non_blocking=True` host-to-MPS copies of temporary CPU tensors returning `NaN` in `scaled_softmax` and `read_slots` ([#21](https://github.com/Mapika/decider/issues/21)). The reproducer was adopted upstream as a temperature regression test in `decider-ai 1.8.2` (fix by the maintainer). Verified on M5 Pro: `1,697/1,698` choice parity with CPU `float32`.
- **[Electrobun](https://github.com/blackboardsh/electrobun)** — reported Windows packaging resolving `rcedit` from a baked CI path ([#298](https://github.com/blackboardsh/electrobun/issues/298)) and submitted a fix ([#299](https://github.com/blackboardsh/electrobun/pull/299)). That pull request was closed without merging. Also diagnosed the hardcoded Windows icon path ([#235](https://github.com/blackboardsh/electrobun/issues/235)).

---

## Measured

Each figure comes from the project's own benchmark record, with its conditions. Where a figure didn't survive a re-check, it isn't here.

| Project | Result | Conditions |
| --- | --- | --- |
| **[tessl](https://tessl.vbcr.dev/)** | **3.06–4.37× faster bf16 inference** than PyTorch MPS (fits 4K–6K ragged workloads in **≤1,911 MiB** where PyTorch OOMs at 33.6 GiB); pure-Rust **TimesFM 3** forecasting **4.3× faster** than PyTorch MPS eager (`479.5 → 111.3 ms`, parity `≤ 1.4×10⁻⁵`) | EmbedGemma 2 paired against `sentence-transformers 6.1.0` / PyTorch 2.14.1 MPS on M5 Pro (load 5.1–16.7, `2026-10-21`), plus SentencePiece BPE **2.2–3.7×** faster (`3.79M–5.12M tok/s`, `4,671/4,671` exact match) than HF `tokenizers 0.23.2`. TimesFM 3 (`330.7M` F32) paired on `64×512` (`2/3` clean rounds on non-idle M5 Pro, group packing + no-zero exact GEMMs `2.06×`, `2026-11-19`). |
| **[ojas](https://ojas.vbcr.dev/)** | Activation checkpointing cuts peak **18.08 → 3.96 GB (−78%)**; LoRA `dW`-skip cuts peak **11.81 → 6.63 GB (−44%)** and step time **−13.2%** (`6,314 → 5,480 ms`); resident Q8 weights save **1.38–1.58 GB**; CUDA A100 500-step LoRA matches PyTorch fp32 eval loss within **4.5×10⁻⁶** (`2.98–3.22×` cuBLAS over FFMA) | MetalBackend on M5 Pro (`0.8B-Base` checkpointing at T = 2,048, `n = 1`; `2B-Base` `dW`-skip over 5 interleaved reps across 150 sites, `2026-10-22`; resident Q8 at T = 2,048 and T = 9,638 with bit-identical loss, `2026-11-13`). CUDA measured on A100 `sm_80` (self-baseline vs FFMA, slower than PyTorch eager, `2026-11-20`). |
| **[MANVI](https://manvi.vbcr.dev/)** | Input tokens **245,117 → 110,621 (−54%)** and steps **9.63 → 4.69** across **600 pre-registered runs** (`717–719/720` facts right across all 5 arms) | Pre-registered 5-arm study (`120` units, `claude-haiku-5-5`, noise-floor gate held): default read-only batching cut **−69,721** tokens/unit and hermetic Starlark scripting cut a further **−64,774**; single model/repo, savings concentrated in chained lookup trails (`2026-11-24`). |
| **[ScholarLM](https://scholarlm.dev/)** | **97.7% (`85/87`) precision on public LitQA2** without a supplied paper corpus | End-to-end literature pipeline on public LitQA2 queries with zero pre-supplied papers, improving over the closed-book baseline (`2026-10-25`). |
| **[DevMap](https://devcouncil.vbcr.dev/)** | **1.6–21× faster cold index** and **2.2–107× faster unchanged-tree refresh** than four rival code-graph tools; schema `v29` cut index size **593.4 → 272.6 MB (−54%)**; one-file edit instructions cut **29–36%** vs schema 29 | Indexing speed measured on `v0.2.2` (M5 Pro, fixed commits, lost single-file re-index to CodeGraph, `2026-09-14`); schema `v29` storage on cold GitPulse (now Waylode) corpus (`2026-11-02`); edit instructions across 4 repos (`2026-11-19`, self-improvement vs schema 29). |
| **[Waylode](https://bharath.vbcr.dev/waylode)** (formerly GitPulse) | **30k-commit refresh 25.19 → 1.11 ms**; **100k-commit cold history 7.89 s → 534 ms (14.7×)** without commit-graph (`1.35 s → 606 ms`, `2.2×` with); **24-watch wakeups 117.3 → 2.7/s**; **narrow FSEvents ~96% less added `fseventsd` CPU**; **hook gate 32.16 → 11.16 ms (−65%)**; **100k-task search p95 97.59 → 44.60 ms** | Revision-token graph refresh (`2026-11-09`); single-walk 100k history (`n = 7` interleaved, synthetic linear history under heavy load, `2026-11-19`); `kqueue`/wake-pipe (`2026-10-13`) and narrow watch (`2026-11-15`); local-socket hook gate (`2026-10-13`); interleaved `100k`-task search (`2026-10-07`). |
| **[Gusset](https://gusset.vbcr.dev/)** | Go→Rust serial call **90.3 → 10.6 µs (8.5×)** | Spin-then-park, certified before/after on one linux-amd64 VM (`2026-10-08`). A later shared-memory ring (7.46 → 3.73 µs) ran in a different container without a provenance header, so the two are not chained. |

---

## The stack

Each project is a module the next one is built on. Every arrow below is a real dependency in the source: a crate, a `go.mod` require, a vendored engine or a spawned sidecar. Arrows point from a project to what it builds on.

```mermaid
flowchart TB
  subgraph K["Kernels"]
    tessl["tessl<br/>Metal 4 GEMM, Q4/Q8 + Qwen3.5 engine"]
    sparsl["sparsl<br/>sparse + scan kernels"]
  end
  subgraph E["Engines & boundaries"]
    ojas["ojas<br/>deep learning &amp; training engine"]
    gusset["Gusset<br/>Rust-in-Go contract"]
  end
  subgraph A["Code intelligence & agents"]
    devmap["DevCouncil · DevMap<br/>code graph + gate"]
    manvi["MANVI<br/>agent harness"]
    jarvis["Jarvis<br/>model-free replay"]
  end
  subgraph P["Products"]
    waylode["Waylode"]
    scholarlm["ScholarLM"]
    devtype["DevType"]
    vani["Vani"]
  end
  subgraph R["Research"]
    binn["BINN"]
    lappi["Lappi"]
    gemma["gemma-metal"]
    spiketrack["SpikeTrack"]
  end

  ojas -->|kernels| tessl
  ojas -->|cgo| gusset
  lappi -->|Mac backend| tessl
  lappi -->|Mac trainer| ojas
  binn -->|crates.io| sparsl
  binn -.->|optional| tessl
  gemma -->|GEMMs| tessl
  spiketrack -->|Metal 4| tessl
  spiketrack -->|runtime| ojas
  devmap -->|engine + oracle| gusset
  manvi --> devmap
  manvi --> gusset
  jarvis -->|replay| manvi
  waylode -->|vendored| devmap
  waylode -->|sidecar| manvi
  waylode --> gusset
  scholarlm -.->|dev tooling| devmap
  scholarlm -.->|workspaces| waylode
  devtype -.->|dev tooling| devmap
  devtype -.->|coverage| waylode
  vani -->|policy pkg| manvi
  vani -.->|EmbedGemma 2| tessl
  vani -.->|triage + labels| lappi
  vani -.->|dev tooling| devmap
```

`sparsl` was lifted out of BINN's numeric core and published on its own. Waylode and DevCouncil power development workflows across ScholarLM, DevType, Vani, and the rest of the workspace; Waylode also vendors MarkDev's renderer crates, and DevPrism embeds MANVI as its tool gate. Explore the interactive stack on **[bharath.vbcr.dev](https://bharath.vbcr.dev/#ecosystem)**.

---

## Core projects

<table>
<tr><th align="center" width="72"></th><th align="left">Project</th><th align="left">Builds on · Used by</th></tr>

<tr><td colspan="3"><b>Kernels</b></td></tr>
<tr>
<td align="center"><img src="assets/tessl.png" alt="tessl" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/tessl">tessl</a></b> · <a href="https://tessl.vbcr.dev/">tessl.vbcr.dev</a><br/>Makes matrix math, LLM inference, and forecasting fast on Apple GPUs (v0.2.0 on crates.io). A Metal 4 GEMM and tensor runtime in Rust using MPP TensorOps <code>matmul2d</code>, cooperative register accumulators, fused epilogues, and MLX-affine Q8/Q4 dequantization. Runs EmbedGemma 2 3.06–4.37× faster in bf16 than PyTorch MPS (fitting 4K–6K ragged inputs in ≤1,911 MiB where PyTorch OOMs at 33.6 GiB), ports Google's 330.7M TimesFM 3 forecaster to pure Rust/Metal 4 (4.3× faster than PyTorch MPS eager on 64×512, ≤ 1.4×10⁻⁵ parity), and supplies <code>ojas</code>'s Metal backward kernels.</td>
<td>Used by ojas, Lappi, gemma-metal, BINN, SpikeTrack</td>
</tr>
<tr>
<td align="center"><img src="assets/sparsl.png" alt="sparsl" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/sparsl">sparsl</a></b> · <a href="https://crates.io/crates/sparsl"><img src="https://img.shields.io/crates/v/sparsl?style=flat-square&color=8B0000&labelColor=4a0000&label=crates.io" alt="sparsl on crates.io" /></a><br/>Fast, reproducible kernels for spiking-network simulation: resident CSR SpMV, fused LIF membrane updates, a chunked prefix scan, and <code>MTLSharedEvent</code> zero-copy handoff with <code>tessl</code> (v0.3.0). A <code>Device</code> exists only for a backend that can actually execute, so results reproduce bit for bit and never misreport where they ran.</td>
<td>Lifted out of BINN · used by BINN</td>
</tr>

<tr><td colspan="3"><b>Engines &amp; boundaries</b></td></tr>
<tr>
<td align="center"><img src="assets/ojas.png" alt="ojas" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/ojas">ojas</a></b> · <a href="https://ojas.vbcr.dev/">ojas.vbcr.dev</a><br/>Trains and runs neural networks on Metal, CUDA, WebGPU, and CPU inside Go services with no Python runtime. On Metal, LoRA <code>dW</code>-skip cut Qwen3.5-2B peak 11.81 → 6.63 GB (−44%), activation checkpointing cut 0.8B peak 18.08 → 3.96 GB (−78%), and resident Q8 weights saved another 1.38–1.58 GB with bit-identical loss. On NVIDIA A100 (<code>sm_80</code>), cuBLAS accelerated Qwen3.5-2B forward+backward 2.98–3.22× over its FFMA kernel while tracking PyTorch fp32 eval loss within 4.5×10⁻⁶ over 500 steps; WebGPU now implements all 12 Qwen3.5 hybrid-layer ops in WGSL (60 of 118 <code>Backend</code> trait methods).</td>
<td>Builds on tessl, Gusset · used by Lappi, SpikeTrack</td>
</tr>
<tr>
<td align="center"><img src="assets/Gusset.png" alt="Gusset" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/gusset">Gusset</a></b> · <a href="https://gusset.vbcr.dev/">gusset.vbcr.dev</a><br/>Lets a Go service call a Rust engine safely and cheaply (v0.0.3, MIT / Apache-2.0, Rust 1.100 &amp; Go 1.27): panic firewall, bounded uncollected completions (1,024 default), bounded 30 s <code>Close</code> with worker process-group teardown, deadlines enforced inside Rust, poisoned handles, per-field ABI checks, and member-by-member LLVM bitcode stripping (20 → 9.3 MB archive) for Go 1.27.4 cgo compliance.</td>
<td>Used by DevCouncil, MANVI, ojas, Waylode</td>
</tr>

<tr><td colspan="3"><b>Code intelligence &amp; agents</b></td></tr>
<tr>
<td align="center"><img src="assets/DevCouncil.png" alt="DevCouncil" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/DevCouncil">DevCouncil · DevMap</a></b> · <a href="https://devcouncil.vbcr.dev/">devcouncil.vbcr.dev</a><br/>Gives AI coding agents a fast, accurate map and verification gate (v0.2.3, MIT / Apache-2.0, DCO 1.1). DevMap builds stacked zero-copy SQLite code graphs (schema <code>v29</code> / extraction <code>102</code>; cold GitPulse (now Waylode) index shrank 593.4 → 272.6 MB; one-file edit instructions cut 29–36% vs schema 29), serves 11 MCP tools (<code>devmap ask --evidence</code>, <code>devmap cache</code>/<code>federate</code>, blast radius with owners, commit suspects), ships standalone dependency-free <code>dcredact</code> and <code>devcouncil pr-gate</code>, reads <code>.git/index</code> directly in <code>dc-grep</code>, and links Lean 4 anti-reward-hacking checks.</td>
<td>Builds on Gusset · used by MANVI, Waylode, ScholarLM, DevType, Vani (dev tooling)</td>
</tr>
<tr>
<td align="center"><img src="assets/MANVI.png" alt="MANVI" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/Manvi">MANVI</a></b> · <a href="https://manvi.vbcr.dev/">manvi.vbcr.dev</a><br/>Runs AI coding agents under explicit policy in pure Go (1.27.4) and Rust: 54 native tools (including concurrent <code>devcouncil_batch</code> and hermetic Starlark <code>devcouncil_script</code>, cutting input tokens 245,117 → 110,621 [−54%] and steps 9.63 → 4.69 across 600 pre-registered runs), SQLite lease exclusion, SHA-256 read-before-overwrite guards, opt-in macOS <code>sandbox-exec</code> secret containment (~7 ms/cmd), and asymmetric isolated bench verification.</td>
<td>Builds on DevCouncil, Gusset · used by Waylode, Jarvis, DevPrism</td>
</tr>
<tr>
<td align="center"><img src="assets/Jarvis.png" alt="Jarvis" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/Jarvis">Jarvis</a></b> · <a href="https://jarvis.vbcr.dev/">jarvis.vbcr.dev</a><br/>Computer-use agent arm for MANVI and Vani: desktop capabilities discovered once with Gemini, frozen into typed artifacts behind a test-enforced <code>jarvis.*</code> capability table, then replayed through MANVI with no model decisions (35/40 macOS replays and 40/40 saved-state checks, not yet a clean stability pass), out-of-band SHA-256 held-out lock verification, and human approval gating every account change.</td>
<td>Builds on MANVI</td>
</tr>

<tr><td colspan="3"><b>Products</b></td></tr>
<tr>
<td align="center"><img src="assets/Waylode.png" alt="Waylode" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/GitPulse">Waylode</a></b> (formerly GitPulse) · <a href="https://bharath.vbcr.dev/waylode">bharath.vbcr.dev/waylode</a> <a href="https://github.com/bharathvbcr/GitPulse/releases"><img src="https://img.shields.io/github/v/release/bharathvbcr/GitPulse?include_prereleases&sort=semver&style=flat-square&color=8B0000&labelColor=4a0000&label=" alt="Latest Waylode release" /></a><br/>Single-process Rust / Tauri 2 / Svelte 5 control plane (<code>v0.2.0-beta.1</code> macOS pre-release) for Git review, worktree collision detection, task orchestration, and supervised AI agent sessions: 100k-commit cold history in 534 ms (7.89 s → 534 ms, 14.7× without commit-graph), host-load governor with build-slot leases, narrow macOS FSEvents watch (~96% less added <code>fseventsd</code> CPU), in-process secret scanner, unified Explorer with <code>Cmd+L</code> send-to-agent, split-pane canvas terminal, native <code>wry</code> browser tabs, A2A peer bus, 22 MCP tools, and contract-checked IPC handlers.</td>
<td>Builds on DevCouncil, MANVI, Gusset · drives workspaces across ScholarLM &amp; DevType</td>
</tr>
<tr>
<td align="center"><img src="assets/ScholarLM.png" alt="ScholarLM" width="48"/></td>
<td><b><a href="https://scholarlm.dev/">ScholarLM</a></b> · <a href="https://scholarlm.vbcr.dev/">showcase &amp; architecture</a><br/>AI research platform searching 20 scholarly sources across ~250 Go routes and writing fully-cited, grounded manuscripts (plan → write → verify → review, <b>97.7%</b> [85/87] precision on public LitQA2 with no supplied corpus): React 19 PWA, Rust edge (with MCP OAuth 2.1 / PKCE S256), Go orchestration core, Python ML worker, and a 25-tool MCP server whose agent layer is open as <a href="https://github.com/bharathvbcr/WisDev">WisDev</a>.</td>
<td>DevMap &amp; Waylode power its coding-agent workflows</td>
</tr>
<tr>
<td align="center"><img src="assets/DevType.png" alt="DevType" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/DevType">DevType</a></b> · <a href="https://devtype.vbcr.dev/">devtype.vbcr.dev</a> <a href="https://github.com/bharathvbcr/DevType/releases"><img src="https://img.shields.io/github/v/release/bharathvbcr/DevType?include_prereleases&sort=semver&style=flat-square&color=8B0000&labelColor=4a0000&label=" alt="Latest DevType release" /></a><br/>Native macOS text expander and on-device writing assistant in Swift/AppKit (v1.2.0 + companion <code>devtype-cli</code>). Typed triggers expand in ordinary text fields; proofread, rewrite, translate and code actions run on Apple Foundation Models offline; imports TextExpander/Espanso and protects secrets behind Touch ID.</td>
<td>DevCouncil verifies its changes; its coverage export feeds Waylode (development tooling)</td>
</tr>
<tr>
<td align="center"><img src="assets/Vani.png" alt="Vani" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/Vani">Vani</a></b> · <a href="https://bharath.vbcr.dev/vani">architecture &amp; apply suite</a><br/>Listings-first career engine and local-first apply suite in Go 1.27.4 (<code>vanid</code> + canonical nested <code>decide</code> and <code>rkb</code> modules), Swift (macOS Vani Apply), and TypeScript (Chrome/Safari WebExtensions). Ingests roles across 38 built-in ATS and job-board platforms with group-committed ledger updates (500-posting update 2.92 → 0.17 s min), bounded single-pass <code>vani status</code> ledger folding (7.6 → 4.2 s median, 8 s cap), zero-token dead/duplicate filtering, four-slot triage, <code>BLAKE2b</code> MinHash held-out fingerprints for Lappi, and <code>rkb</code>-verified resume generation.</td>
<td>Builds on MANVI, tessl (EmbedGemma 2), Lappi, DevCouncil tooling</td>
</tr>

<tr><td colspan="3"><b>Research</b></td></tr>
<tr>
<td align="center"><img src="assets/BINN.png" alt="BINN" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/Brain-Inspired_Neural_Network">BINN</a></b> · <a href="https://binn.vbcr.dev/">binn.vbcr.dev</a><br/>From-scratch Rust instrument that falsified backprop-free local learning under pre-registered kill-gates, then proved temporal spike order drives a causal-attention read-out on Spiking Heidelberg Digits (0.8320, 12/12 seeds ≥ 0.80) and replicated the recurrent contrast across 32 pre-registered seeds (80/80 cells, 4/4 hypotheses MET, +0.1551 seed-paired gain, 1.404× headroom-normalized); bit-exact NEON attention (1.85×) and Accelerate BLAS (2.23×) accelerate 2-epoch SHD cells over <code>sparsl 0.3</code> resident ticks.</td>
<td>Builds on sparsl, tessl</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/-8B0000?style=flat-square&logo=apple&logoColor=white" alt="SpikeTrack" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/SpikeTrack">SpikeTrack</a></b> · <a href="https://bharath.vbcr.dev/spiketrack">architecture &amp; parity</a> <img src="https://img.shields.io/badge/in_progress-6B7280?style=flat-square&labelColor=4a4a4a" alt="In progress" /><br/>Pure-Rust port of Meta's SAM 3.1 multiplex video tracker on Apple Silicon (zero Python at runtime, Pillow-exact JPEG decoder, 14 linked system frameworks): mixes an fp16 Core ML default trunk (0.569–0.600× fp32 trunk frame time on VISEM) with merge encodes, segmentation head, and Metal 4 Flash cross-attention on <code>ojas</code> / <code>tessl</code> (0.5695 held-out HOTA vs 0.5700 fp32 across 1,500 frames).</td>
<td>Builds on ojas, tessl</td>
</tr>
<tr>
<td align="center"><img src="assets/Lappi.png" alt="Lappi" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/Lappi-decision">Lappi</a></b> · <a href="https://lappi.vbcr.dev/">lappi.vbcr.dev</a> <img src="https://img.shields.io/badge/in_progress-6B7280?style=flat-square&labelColor=4a4a4a" alt="In progress" /><br/>Calibrated typed-decision model (v0.1 preview 0.857 choice top-1, not promoted after OOD abstention 149/180 missed its 90% bar): schema in, typed slots out (choice, score, span, abstain) where <code>not_run</code> never counts as a pass. Now trains and serves job-modeling heads (<code>role_fit</code>, <code>work_mode</code>, <code>seniority</code>, <code>sponsorship</code>) on <code>ojas</code> / <code>tessl</code> behind a MinHash contamination gate, a fail-closed cloud data-governance door, a 3,844-row CUDA-vs-MPS bf16 synthetic parity gate, and −47% scan peak containment (20.6–22.6 → 10.9–12.0 GiB).</td>
<td>Builds on tessl, ojas</td>
</tr>
<tr>
<td align="center"><img src="assets/MLSystemsLab.png" alt="MLSystemsLab / nanolab" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/nanolab">nanolab</a></b> · <a href="https://attention.vbcr.dev/">attention.vbcr.dev</a><br/>Instrumented small-LM training lab (378/378 checks passing): attention, Mamba-2, Gated DeltaNet and minGRU behind CLI flags, chunk-parallel scan kernels, and seed-paired intervals — withdrawing unpaired GDN/Mamba-2 speedups directly in the committed TMLR/preprint manuscript.</td>
<td>Research companion to the kernels</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/-8B0000?style=flat-square&logo=apple&logoColor=white" alt="gemma-metal" width="48"/></td>
<td><b><a href="https://github.com/bharathvbcr/gemma-metal">gemma-metal</a></b> <img src="https://img.shields.io/badge/in_progress-6B7280?style=flat-square&labelColor=4a4a4a" alt="In progress" /><br/>Gemma inference runtime for Apple silicon with split sliding/global KV ring caches. Takes its general and INT4 GEMM kernels from <code>tessl</code>, and remains below its own decode-speed gate (6.83 vs 15 tok/s on 31B Q4; 23.9 vs 48 on E4B).</td>
<td>Builds on tessl</td>
</tr>
</table>

---

## Where the stack goes next

These are directions, each grounded in what the repositories themselves record as open:

- **Train and serve Lappi on my own stack.** Lappi's Mac trainer already runs on `ojas` and its backend serves on `tessl`'s Qwen3.5 kernels, while the main `2B` campaign runs on PyTorch. Next: OOD abstention, serving the code-defect family, and promoting job-modeling runs past pre-registered validation floors.
- **A device-aware engine for Go services.** `ojas` reaches Go through Gusset, and its resource plan reads cores, caches, unified memory, and cgroup limits — but there is no automatic device router yet. Routing work between CPU and Metal from that plan is next.
- **Spiking read-outs on the current kernels.** BINN's `tessl` interop is pinned to `0.1.4`, while `tessl` has moved to `0.2.0` (`C ABI 14`). Bringing the attention read-out that earned the SHD result onto the current kernels comes next.
- **One shared code-graph and policy substrate.** DevMap and Waylode already power engineering workflows across ScholarLM, DevType, and Vani, and MANVI under Waylode, Jarvis, Vani, and DevPrism, so schema (`v29`/`v102`, workbench `17`) and formal-verification upgrades propagate across every repository at once.

---

## Research & publications

| Paper | Journal | Year |
| --- | --- | --- |
| [Investigation on the heating effects of intra-tumoral injectable magnetic hydrogels (IT-MG) for cancer hyperthermia](https://iopscience.iop.org/article/10.1088/2057-1976/adaec6/meta) | _Biomedical Physics & Engineering Express_ | 2025 |
| [The Therapeutic Scope of Orofacial Mesenchymal Stem Cells](https://www.mdpi.com/2306-5354/12/9/970) | _Bioengineering_ | 2025 |

Biomedical computing: **[GenoThermal_Targeting](https://github.com/bharathvbcr/GenoThermal_Targeting)**, a patient-specific magnetic-nanoparticle therapy pipeline from genomic discovery through physics simulation. Research briefs are at **[research.vbcr.dev](https://research.vbcr.dev/)**.

---

## Also built

<details>
<summary>Side projects: finished or maintained, but outside the main stack</summary>
<br/>

- **[Graft](https://github.com/bharathvbcr/Graft)**: sealed Mac-to-Android continuity workspace (clipboard images/text, zipped folders, notifications, remote shell and audio) over mutual TLS 1.3 and Tailscale/USB, checked by a symbolic Dolev-Yao verifier, Kani proofs, and Lean 4 protocol specs.
- **[Chronicle](https://github.com/bharathvbcr/Chronicle)**: local-first second brain across Mac and Android (pinned LAN TLS, E2EE locked-vault parking, local Ollama RAG).
- **[MarkDev](https://github.com/bharathvbcr/MarkDev)**: native macOS Markdown editor (`v0.0.3`) on a Swift + 4-crate Rust core; its renderer crates are vendored into Waylode.
- **[DevPrism](https://github.com/bharathvbcr/DevPrism)**: local-first LaTeX and research workspace, forked from claude-prism, with MANVI as its tool gate.
- **[M5Blade](https://github.com/bharathvbcr/M5Blade)**: Apple-silicon fan controller that writes to the SMC behind a race-free control gate.
- **[Strait](https://strait.vbcr.dev/)**: macOS bulk transfer (`F_NOCACHE` I/O, pure-Swift BLAKE3 hash-on-write, and resumable staging).
- **[Curio](https://github.com/bharathvbcr/Curio)**, **[ChronosFlow](https://github.com/bharathvbcr/ChronosFlow)**, **[Meridian](https://github.com/bharathvbcr/Meridian)**, **[TrailBlazer](https://github.com/bharathvbcr/TrailBlazer)**: on-device AI and native mobile apps.
- **[SalEdge](https://github.com/bharathvbcr/SalEdge)**: multi-firm ERP for battery retailers, with GST e-invoicing and a local AI layer.
- **[AcademiaTrack](https://github.com/bharathvbcr/AcademiaTrack)**, **[Void](https://github.com/bharathvbcr/Void)**, **[Whimsical-Love](https://github.com/bharathvbcr/Whimsical-Love)**: web apps and experiences.

Everything has a page at **[apps.vbcr.dev](https://apps.vbcr.dev/)**.
</details>

---

### Stack

**Systems** &nbsp; ![Rust](https://img.shields.io/badge/Rust-8B0000?style=for-the-badge&logo=rust&logoColor=white) ![Go](https://img.shields.io/badge/Go-6B0000?style=for-the-badge&logo=go&logoColor=white) ![Metal](https://img.shields.io/badge/Metal_4-4a0000?style=for-the-badge&logo=apple&logoColor=white) ![CUDA](https://img.shields.io/badge/CUDA-8B0000?style=for-the-badge&logo=nvidia&logoColor=white) ![Swift](https://img.shields.io/badge/Swift-6B0000?style=for-the-badge&logo=swift&logoColor=white)

**ML** &nbsp; ![PyTorch](https://img.shields.io/badge/PyTorch-8B0000?style=for-the-badge&logo=pytorch&logoColor=EE4C2C) ![MLX](https://img.shields.io/badge/MLX-6B0000?style=for-the-badge&logo=apple&logoColor=white) ![Vertex AI](https://img.shields.io/badge/Vertex_AI-4a0000?style=for-the-badge&logo=google-cloud&logoColor=white)

**Product** &nbsp; ![TypeScript](https://img.shields.io/badge/TypeScript-8B0000?style=for-the-badge&logo=typescript&logoColor=white) ![Tauri](https://img.shields.io/badge/Tauri_2-6B0000?style=for-the-badge&logo=tauri&logoColor=white) ![Svelte](https://img.shields.io/badge/Svelte_5-4a0000?style=for-the-badge&logo=svelte&logoColor=white) ![React](https://img.shields.io/badge/React-8B0000?style=for-the-badge&logo=react&logoColor=61DAFB) ![MCP](https://img.shields.io/badge/MCP-6B0000?style=for-the-badge&logoColor=white)

---

### GitHub activity

<div align="center">
  <img src="https://raw.githubusercontent.com/bharathvbcr/bharathvbcr/output/stats.svg" width="49%" alt="GitHub Stats" />&nbsp;<img src="https://raw.githubusercontent.com/bharathvbcr/bharathvbcr/output/top-langs.svg" width="49%" alt="Most used languages" />
  <img src="https://raw.githubusercontent.com/bharathvbcr/bharathvbcr/output/activity.svg" width="98.5%" alt="Contribution activity and streaks over the last year" />
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/bharathvbcr/bharathvbcr/output/github-snake-dark.svg?v=1" alt="GitHub contribution snake" />
</div>

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a0000,25:4a0000,50:8B0000,75:4a0000,100:1a0000&height=120&section=footer" alt="footer banner" width="100%" />
</div>

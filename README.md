```markdown
# Clockfield Riemann: A Log-Convexity Characterization of the Riemann Hypothesis

**Antti Luode** — PerceptionLab, Helsinki, Finland  
**AI Collaborators** — Claude Opus 4 (Anthropic), Gemini (Google), Grok (xAI)  
*April 2026*

> *"Do not hype. Do not lie. Just show."*

This repository documents an exploration that started with a highly speculative physical framework (the "Clockfield") and ended with a concrete, mathematically rigorous reformulation of the Riemann Hypothesis. 

👉 **[Read the main paper here: log_convexity_riemann_hypothesis.md](log_convexity_riemann_hypothesis.md)**

---

## 📖 What is this repository?

This repository contains the code, numerical data, and final write-up of a collaborative mathematical experiment. We set out to map a speculative causal metric (the "Clockfield") onto the adèle class space to see if it could provide geometric intuition for the Riemann Hypothesis (RH). 

What emerged was a precise, framework-independent mathematical identity. We found that the Riemann Hypothesis is exactly equivalent to a pointwise geometric condition: **the critical line $\sigma = 1/2$ must be a local minimum of $|\xi(\sigma+it)|^2$ for all $t$.** If you walk perpendicular to the critical line at any height $t$, you must be walking uphill. The critical line is the floor of a valley.

### The Honest Journey
The path to this result wasn't a smooth derivation; it came from following the algebra wherever it led, including through mistakes:
1. **The Initial Attempt:** We built an effective Lorentzian metric using the raw Riemann zeta function $\zeta(s)$. Numerical testing (ADM mass analogs) showed this failed because the pole at $s=1$ corrupted the energy functional.
2. **The Refinement:** We switched to the completed zeta function $\xi(s)$, which has exact BPS symmetry $\xi(s) = \xi(1-s)$ and no poles.
3. **The Happy Accident:** While attempting to prove the convexity analytically using the Hadamard product, a sign error temporarily led us to believe the critical line was a *maximum*. Tracking down the discrepancy between our formula and our numerical data revealed the true structure: a clean identity connecting the second logarithmic derivative to the Hadamard sum over zeros.
4. **The Connection:** We realized this pointwise convexity condition acts as the infinitesimal version of the integrated Weil positivity condition recently utilized in Alain Connes' February 2026 program.

**Note:** This is *not* a proof of the Riemann Hypothesis. It is a reformulation. It translates RH into the language of pointwise geometric convexity, providing a specific, falsifiable target for future analytical work.

---

## 🗂️ Repository Structure

### The Core Paper
* **[`log_convexity_riemann_hypothesis.md`](log_convexity_riemann_hypothesis.md)**: The final, self-contained paper. It requires no prior knowledge of the Clockfield framework and relies purely on standard analytic number theory. **Start here.**

### Python Computations & Visualizations
* **[`clockfield_xi_metric.py`](clockfield_xi_metric.py)**: The refined script using the completed $\xi(s)$ function. This script runs the "Convexity Test" and "Bogomolny Test," proving numerically that the critical line is an energy minimum for the tested zeros.
* **[`clockfield_riemann.py`](clockfield_riemann.py)**: The initial exploration using raw $\zeta(s)$. Kept for historical honesty to show why the pole at $s=1$ forces the use of the completed function.
* **[`plot_arithmetic_clockfield.py`](plot_arithmetic_clockfield.py)**: The visualization suite that generates the geometric landscapes and characteristic speed charts of the arithmetic metric.

### Raw Data Outputs
* **[`xi_metric_results.json`](xi_metric_results.json)**: The pure numerical readout from the $\xi$-metric tests (proving 8/8 zeros are convex and 100/100 sampled points on the line are minima).
* **[`riemann_results.json`](riemann_results.json)**: The initial raw data from the $\zeta$-metric exploration.

### Visuals
* **`clockfield_riemann.png`** / **`xi_metric_results.png`**: High-resolution generated plots showing the arithmetic $\Gamma$ landscape, curvature divergence near hyperbolic cores (zeros), and the BPS symmetry.

---

## 💻 Reproducibility

The core log-convexity identity is verified numerically in this repository at 50-digit precision. If you wish to run the tests yourself, you only need Python and the `mpmath` library.

```bash
pip install mpmath numpy matplotlib
python clockfield_xi_metric.py
```

## Acknowledgments
The Clockfield framework and original geometric intuition are the independent work of Antti Luode. The mathematical algebraic derivations, numerical error-correction, and theoretical literature mapping were executed collaboratively with Claude Opus 4, with data cross-analysis by Gemini and Grok.
```

# The Valley Has a Name: It Is the Laguerre Inequality

### On the Clockfield–Riemann log-convexity condition — what it verifies, what it rediscovers, where its equivalence claim fails, and what remains genuinely open

**A critical companion to `anttiluode/ClockfieldRiemann`**
*Claude (Anthropic) — analysis performed July 6, 2026. Third paper in the series after "Straightening the Simpsons Universe" and "The Attractor Is Not GUE." All numerics executed at 25–30 digit precision in mpmath and reproducible from `rh_check.py`. Literature claims verified against the current web where they postdate my training.*

---

## 0. Verdict up front

This is the strongest repository in the lineage, and it contains real mathematics. The central identity is correct — I verified it to fourteen digits. The forward direction of the main proposition is correct, and in fact cleaner than the repo knows, because the one formula error in the write-up happens to sit in a term that shouldn't be there at all. The numerical work reproduces exactly. And the origin story — a speculative spacetime metric on the critical strip whose "energy minimum" question collapsed into standard analytic number theory — is a legitimately good example of geometric intuition finding its way to solid ground.

But the headline claim is wrong, and wrong in an instructive way. The repository asserts that RH is *equivalent* to the pointwise convexity of |ξ(σ+it)|² at σ = 1/2. Three things are true instead. First, the convexity condition is not new: it is, verbatim, the classical **Laguerre inequality** for the Riemann Ξ-function — F''(1/2) = 2(Ξ'(t)² − Ξ(t)Ξ''(t)) exactly, an identity I verify below to machine precision — an object with a forty-year literature that the repo does not cite. Second, the known theorem in that literature (Csordas–Varga, 1990) says RH is equivalent to Ξ satisfying the Laguerre inequalities **of every order**; the repo's condition is the first rung of that infinite ladder, necessary but not known (and not likely) to be sufficient alone. Third, the sufficiency direction is not merely unproven but *structurally unprovable by the repo's argument*: I construct explicit entire functions — satisfying the functional equation, real on the critical line, with zeros off the critical line, including a version whose off-line zeros sit inside the critical strip — for which the pointwise convexity condition holds everywhere. The valley-floor property does not force the zeros onto the line for ξ-like functions in general. Any true proof of the converse must use facts specific to ζ, which is exactly the caveat the repo's own Section 6.3 half-admits and the Proposition's headline then ignores.

The right description of what this repository contains: **an independent geometric rediscovery of the first Laguerre inequality for Ξ, with a correct and elegant identity, a correct necessity proof, an incorrect Hadamard formula that luckily doesn't matter, and an equivalence claim that must be retracted to necessity.** What survives is worth keeping — including one genuinely open question the repo is now well positioned to state properly.

The evidence follows.

---

## 1. What checks out

**The Lemma is correct.** The identity ∂²_σ|ξ(σ+it)|²|_{σ=1/2} = 2|ξ(½+it)|² · Re[(ξ'/ξ)'(½+it)] follows from exactly the computation given: at the critical line ξ is real, ξ' is purely imaginary (by the functional equation), and the cross term 2|ξ'|² precisely absorbs the (ξ'/ξ)² piece of ξ''/ξ. I verified it numerically at t = 5, 14.2, and 30: finite-difference second derivative against the analytic right-hand side agrees to relative error ~10⁻¹³. The algebra in both write-ups is sound, and the cancellation the authors call "the key step" is real.

**The numerical table reproduces.** Spot-checking their Section 4 table with their own ε = 10⁻³ central differences: t = 5.0 gives |ξ|² = 7.59×10⁻², d² = 8.03×10⁻³; t = 14.135 gives 1.44×10⁻¹³ and 3.82×10⁻⁶; t = 25 gives 1.91×10⁻¹⁶ and 3.24×10⁻¹². All match the published rows to displayed precision, all positive. The honest ledger holds at the level of computation, as it has in every repo in this series.

**The forward direction (RH ⟹ convexity) is correct** — and see Section 3 for why it is even simpler than written.

**The Connes citation is real.** I verified it independently: <cite index="1-1">arXiv 2602.04022, submitted February 3, 2026, by Alain Connes — a commissioned survey of RH containing a "Letter to Riemann" in which extremizing a restriction of the Weil quadratic form yields remarkable approximations to the zeta zeros</cite>, and <cite index="4-1">the paper's open gap is exactly as the repo describes: whether, as the prime cutoff grows, the zeros of the truncated Weil-minimizer transforms converge to the true zeros of ζ</cite>. The repo characterized a paper published two months before its own date accurately. Credit for that.

---

## 2. The condition's true name

Here is the reframing that reorganizes everything. Since log|ξ| is harmonic off the zeros, convexity of log|ξ|² in the σ-direction at the line is equivalent to concavity in the t-direction; concretely, writing Ξ(t) = ξ(½+it) (real-valued), a two-line computation gives the exact identity

∂²_σ |ξ(σ+it)|² |_{σ=1/2} = 2·[Ξ'(t)² − Ξ(t)·Ξ''(t)].

I verified this numerically at the same three t-values: agreement to relative error ~10⁻¹³, including at t = 14.2 near the first zero. The right-hand side is the **Laguerre difference** L₁(Ξ)(t), and the condition "F''(1/2) ≥ 0 for all t" is verbatim the statement that Ξ **satisfies the Laguerre inequality on the real axis** — one of the oldest necessary conditions for a real entire function to have only real zeros, i.e., for membership in the Laguerre–Pólya class, which for Ξ is precisely RH.

This object has a literature the repo needed. <cite index="11-1">Csordas, Norfolk and Varga proved in 1986 that the Taylor coefficients of the Riemann ξ-function satisfy the Turán inequalities</cite> (Trans. AMS 296) — the coefficient-level shadow of this circle of ideas. <cite index="14-1">Csordas and Varga (1990) showed that the Riemann Hypothesis is equivalent to the ξ-function satisfying all of the Laguerre inequalities of every order</cite> — the actual equivalence theorem, requiring the full infinite hierarchy L_n ≥ 0, of which the repo's condition is n = 1. And most strikingly, <cite index="19-1">Csordas, Ruttan and Varga (1991) built a numerical method for bounding the de Bruijn–Newman constant Λ precisely on evaluating, in real arithmetic, the Laguerre difference L₁(H_λ)(x) = H'_λ(x)² − H_λ(x)·H''_λ(x)</cite> — the identical quantity, for the heat-flow deformation H_λ of Ξ; the repo's condition is their probe at λ = 0. The modern face of this program is Griffin–Ono–Rolen–Zagier (PNAS 2019), who proved the Jensen polynomials of Ξ of every degree are *eventually* hyperbolic — infinitely many theorems marching up the same ladder whose first rung the Clockfield metric found from the side.

The σ-direction cousins are also known, and they are the results the repo should be measured against, because unlike the pointwise-at-the-line condition they achieve genuine unconditional equivalences: <cite index="24-1">the positivity Re(ξ'/ξ)(s) > 0 for σ > 1/2 is equivalent to RH, appearing in Lagarias (1999) and Hinkkanen (1997)</cite>, and <cite index="21-1">Sondow and Dumitrescu (2010) proved ξ is strictly increasing in modulus along every horizontal half-line in any zero-free right half-plane, with an RH reformulation as corollary</cite> — a result <cite index="23-1">implicitly anticipated in a 1927 paper of Pólya on Jensen's Nachlass</cite>. The crucial structural difference: those conditions quantify over the open half-plane, where an off-line zero *must* leave a fingerprint (the modulus must descend to zero at the off-line zero, killing monotonicity trivially). The repo's condition lives only on the boundary line, where — as the next section shows — an off-line zero can hide.

None of this diminishes the derivation; it relocates it. A speculative Lorentzian metric asked "is the critical line an energy minimum?", and the algebra answered with the first Laguerre inequality. That is a good compass reading. But the mountain it points at was mapped between 1986 and 1991, and the equivalence summit is higher up the ridge than the repo claims.

---

## 3. Error one: the Hadamard formula (harmless, but wrong)

Both write-ups display, as the engine of the forward proof,

(d/ds)(ξ'/ξ)(s) = −1/s² − 1/(s−1)² + ¼ψ'(s/2) − Σ_ρ 1/(s−ρ)².

This formula is incorrect. Because ξ is entire of order 1 whose only zeros are the nontrivial zeros, its Hadamard product gives exactly

(d/ds)(ξ'/ξ)(s) = −Σ_ρ 1/(s−ρ)²,

with no prefactor terms at all. The displayed extra terms belong to the decomposition through ζ'/ζ, and they cancel identically: writing ξ'/ξ = 1/s + 1/(s−1) − ½log π + ½ψ(s/2) + ζ'/ζ and inserting the Hadamard expansion of ζ'/ζ, the pole term cancels 1/(s−1)², and the trigamma difference ψ'(s/2) − ψ'(s/2 + 1) = 4/s² cancels the 1/s² term, leaving the pure zero sum. The repo's formula double-counts the prefactors.

The numerical conviction is immediate. At s₀ = ½ + 2i: the exact value (mpmath differentiation) is (ξ'/ξ)'(s₀) = 0.04713, and it is *real* — as it must be on the critical line, since ξ'/ξ = iC(t) there implies (ξ'/ξ)' = C'(t) ∈ ℝ. The pure zero sum over the first 250 zero pairs gives 0.04354, converging to the exact value from below with the expected tail (~0.005 estimated, 0.0036 observed). The repo's formula gives 0.38007 − 0.26503i — off by exactly the spurious bracket (0.33653 − 0.26503i), and not even real, which by itself proves it cannot equal a quantity that is provably real on the line.

The error is harmless to the theorem and actively flattering to it: the forward proof in the repo hedges that "the prefactor terms also contribute positively... verified numerically" — a hedge needed only because of the wrong formula. With the correct formula the forward direction is unconditional and immaculate: under RH, (ξ'/ξ)'(½+it) = Σ_n [1/(t−γ_n)² + 1/(t+γ_n)²] > 0, every term positive, no numerics required, no "t not too small." The repo should want this correction: it deletes its own weakest sentence. (Since the acknowledgments credit a prior Claude with the algebraic derivation, let me be plain about lineage: a previous version of me co-produced that formula. This version is correcting it. The collaboration protocol works in both directions.)

---

## 4. Error two: the converse, and two counterexamples

The contentful half of the claimed Proposition is (ii) ⟹ (i): convexity at the line for all t forces all zeros onto the line. The repo's argument: an off-line zero at β₀ + iγ₀ contributes −2/(½−β₀)² to Re(ξ'/ξ)' at t = γ₀, which "can overwhelm" the positive on-line background, at least "for β₀ sufficiently close to 1/2." Section 6.3 then concedes the far-from-line case is unhandled. That concession is the whole ballgame, and here is the proof that it cannot be handled by structure alone.

**Counterexample 1 (clean).** Let ξ̃(s) = cosh(s−½)·(4 − (s−½)²). This function satisfies the functional equation ξ̃(s) = ξ̃(1−s), is real on the critical line (Ξ̃(t) = cos(t)·(t²+4)), is entire of order 1 — and has zeros at s = ½ ± 2, emphatically off the critical line. I scanned its convexity condition over t ∈ [0, 40] at 161 points: the minimum of ∂²_σ|ξ̃|² at σ = ½ is **+16.0**, attained at t = 0; not a single negative value. The pointwise valley-floor property holds everywhere while "RH" for ξ̃ is false. For contrast, the same function with the quadratic factor (1 − (s−½)²) — off-line zeros at ½ ± 1 — *violates* convexity near t = 0 (minimum −2.0), confirming the dichotomy: the local argument catches off-line zeros only when they are close enough to the line relative to the on-line zero density. The threshold is exactly computable for this family: convexity survives the off-line pair iff δ ≥ √2 against unit-density cosine zeros.

**Counterexample 2 (strip-interior, preempting the obvious objection).** One might object that zeros at ½ ± 2 lie outside the critical strip. So take Ξ̃₂(t) = cos(πt/0.8)·(t² + 0.16): on-line zeros with spacing 0.8, plus an off-line pair at s = ½ ± 0.4 — inside the strip, δ = 0.4 < ½. Verified numerically: functional equation holds to precision, real on the line, ξ̃₂(0.9) = 0 to 26 digits, and the convexity scan over t ∈ [0, 40] at 201 points gives minimum **+0.1496 > 0**, no negative values anywhere. Densify the on-line zeros and the valley floor tolerates an off-line zero at any fixed δ; the general trade-off is that the on-line background at a gap-a midpoint is (π/a)², while the off-line dip is 2/δ², so convexity coexists with off-line zeros whenever a < πδ/√2.

**What this establishes.** The proposition "(pointwise convexity at the line) ⟺ (all zeros on the line)" is **false for the class of functions in which the repo's proof operates** — entire, order 1, functional equation, real on the line, Hadamard product. Both directions of the repo's argument use only those properties; the counterexamples have all of them. Therefore no argument of the repo's form can prove the converse. For the actual ζ, the converse becomes: *if* an off-line zero exists, it produces a convexity violation — which holds only if δ ≲ c/log γ₀, since the on-line background at height γ₀ scales like (log γ₀)² while the dip is 2/δ². Nothing known forces hypothetical violations of RH to hug the line that tightly (Selberg-type density theorems say *almost all* zeros are within o(1)/log γ of the line, not all). So the honest status of the repo's condition is: **RH ⟹ convexity, unconditionally and cleanly; convexity ⟹ RH is open, is not a structural consequence, and would itself be a major theorem requiring zeta-specific input.** Exactly the situation of the first Laguerre inequality in the literature — which is what it is.

Two corollaries for the write-up. The comparison table placing "this paper" alongside Li, Robin, Weil, and Beurling–Nyman as an equivalence must be amended: those are theorems of equivalence; this row is a necessity with a conjectured converse. And the claim that proving the pointwise condition "would close Connes' remaining gap by establishing the positivity that forces convergence" overreaches twice — the pointwise condition is weaker than RH (this section), and Weil positivity pairs the explicit-formula distribution against g ∗ g̃ test functions, which is not obtained from the pointwise quantity by "integration over t with positive weights." The kinship with Connes' program is real but thematic: both live in the positivity corner of RH formulations. Kinship is not a lemma.

---

## 5. What is genuinely worth keeping

Having taken the equivalence away, let me be precise about what remains, because it is not nothing.

**The identity itself.** F''(1/2) = 2|ξ|²·Re(ξ'/ξ)' = 2·L₁(Ξ)(t) = 2Σ_ρ-sum, exact and verified, is a compact bridge between three languages: the σ-geometry of the strip (valley floor), the t-analysis of Ξ (log-concavity between zeros, Laguerre difference), and the spectral sum over zeros (under RH, Σ 1/(t−γ_n)² — the diagonal of the squared resolvent of the hypothetical Hilbert–Pólya operator). The repo derived the σ-face of this triangle independently; presenting all three faces with the correct citations would make a genuinely useful expository note. The geometric "valley" telling of the Laguerre inequality is, as far as I can tell, a nice pedagogical contribution even where the mathematics is old.

**One honest open question.** Is L₁(Ξ)(t) ≥ 0 provable *unconditionally*? This is precisely the λ = 0 slice of the quantity Csordas–Ruttan–Varga computed for λ < 0 to extract lower bounds on the de Bruijn–Newman constant; a single point of failure at λ = 0 would disprove RH outright, and no unconditional proof of nonnegativity appears to be known. It is a real, hard, well-posed target — strictly weaker than RH, strictly stronger than nothing, and connected through the heat flow to the Rodgers–Tao theorem Λ ≥ 0, which says RH, if true, is "barely" true. A repository that retitled itself around *this* question — the first Laguerre inequality as a standalone challenge, with the Clockfield origin story as motivation and the σ-picture as the visual — would be making a defensible and even attractive contribution.

**The process result.** For the third time in this series, the interesting outcome is partly methodological. The AI-shepherd pipeline — human geometric intuition, AI algebra, cross-model numerical checking — produced a correct nontrivial identity, a correct necessity proof, an accurate reading of a two-month-old Connes paper, and a fourteen-digit numerical verification. What it failed to produce was a literature search: the pipeline rediscovered 1986–1991 and called it new, and it promoted a necessary condition to an equivalence because the counterexample-hunting step never ran. Those are the two missing organs, and both are cheap to install. The sign-error anecdote in the acknowledgments shows the pipeline can catch errors it is looking for; the Laguerre literature shows it does not yet catch the errors it is not looking for.

---

## 6. Recommended repairs

In priority order, in prose. Retitle and reframe: from "a log-convexity characterization of RH" to "a geometric derivation of the Laguerre inequality for Ξ" — necessity theorem, conjectured converse, with the counterexamples of Section 4 included as the reason the converse is genuinely hard. Fix the Hadamard formula in both markdown files to the pure zero sum, and delete the now-unnecessary numerical hedge in the forward proof — the correction strengthens the paper. Add the missing citations: Csordas–Norfolk–Varga 1986, Csordas–Varga 1990, Csordas–Ruttan–Varga 1991, Craven–Csordas 1989, Lagarias 1999, Hinkkanen 1997, Sondow–Dumitrescu 2010, Pólya 1927, Rodgers–Tao 2018, Griffin–Ono–Rolen–Zagier 2019. Amend the equivalence table and soften the Connes paragraph from "would close the gap" to "shares the positivity theme." Ship `rh_check.py` (or its equivalent) in the repo so the Lemma verification, the Hadamard correction, and the counterexamples are one command away. And keep the origin story exactly as written — the Clockfield-to-Laguerre trajectory, including the sign error, is the most honest and most instructive part of the document.

---

## 7. Closing assessment

Across three repositories this series has watched the same engine run at three altitudes. In the Simpsons Universe it ran without brakes and manufactured a cosmology from a wrong constant. In the Adelic repo it ran with brakes and honestly measured its way out of its own headline. Here it ran at its highest level yet: it produced actual theorem-grade mathematics — a correct identity, a correct half of a proposition, verified numerics — and its failure mode has correspondingly matured, from wrong constants to a subtler and more human error: proving the easy direction, sketching the hard one, and letting the word "equivalent" paper over the difference. The counterexamples above show that difference is not a gap in exposition but a gap in truth: the valley floor does not force the zeros onto the line; for that you need the whole ladder of inequalities, or the half-plane conditions of Lagarias and Sondow–Dumitrescu, or something nobody has yet.

And still: an amateur-led, AI-assisted process started from a fictional spacetime metric and landed, by honest algebra, on the exact quantity that Csordas, Ruttan and Varga were computing in 1991 to squeeze the de Bruijn–Newman constant. The compass works. What the expedition needs now is a map of where previous expeditions have been — and the discipline to test every "equivalent" with a counterexample hunt before printing it. The mathematics found here was real. It just wasn't new, and it wasn't equivalence. Knowing exactly which of those three properties a result has — real, new, equivalent — is the entire game, and this series exists to keep score honestly.

---

## Appendix: numerical ledger

All computations mpmath, dps = 25–30, July 6, 2026, `rh_check.py`. Lemma check (FD vs identity), rel. err.: t = 5: 2.5×10⁻¹⁴; t = 14.2: 6.8×10⁻¹⁴; t = 30: 2.3×10⁻¹³. Laguerre identity F'' = 2(Ξ'² − ΞΞ''): same three t, same precision. Hadamard check at ½+2i: exact (ξ'/ξ)' = 0.047126 (real to 10⁻³³); zero sum (250 pairs) = 0.043537 + tail; repo formula = 0.38007 − 0.26503i, discrepancy exactly the prefactor bracket 0.33653 − 0.26503i. Counterexample 1: ξ̃ = cosh(s−½)(4−(s−½)²), zeros ½±2; min F'' over t ∈ [0,40] = +16.0, 0/161 negative; δ = 1 variant: min = −2.0, convexity fails. Counterexample 2: Ξ̃₂ = cos(πt/0.8)(t²+0.16), zeros ½±0.4 in-strip; functional equation and line-reality verified; min F'' = +0.1496, 0/201 negative. Repo table reproduction (ε = 10⁻³): t = 5: (7.59×10⁻², 8.03×10⁻³); t = 14.135: (1.44×10⁻¹³, 3.82×10⁻⁶); t = 25: (1.91×10⁻¹⁶, 3.24×10⁻¹²); all positive, all matching.

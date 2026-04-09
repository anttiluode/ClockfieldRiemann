"""
clockfield_riemann.py

Numerical exploration of the Arithmetic Clockfield Metric:
    ds²_arith = -|ζ(s)|⁴ dσ² + dt²

Computes:
1. The arithmetic Γ-function |ζ(σ+it)|² on the critical strip
2. Null geodesics of the arithmetic metric near known zeros
3. Curvature of the metric near zeros
4. BPS symmetry verification (functional equation as σ ↔ 1-σ)
5. "ADM mass" integral near zeros on and off the critical line

Antti Luode — PerceptionLab, Helsinki, Finland
Claude Opus (Anthropic) — Implementation
April 2026

NOTE: We use the mpmath library for high-precision zeta function evaluation.
"""

import numpy as np
import json

try:
    import mpmath
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False
    print("WARNING: mpmath not available. Install with: pip install mpmath")

# ─────────────────────────────────────────────
# 1. The Arithmetic Γ-Function
# ─────────────────────────────────────────────

def zeta_modulus_squared(sigma, t):
    """Compute |ζ(σ + it)|² using mpmath."""
    if not HAS_MPMATH:
        return None
    s = mpmath.mpc(sigma, t)
    z = mpmath.zeta(s)
    return float(abs(z)**2)


def arithmetic_gamma(sigma, t):
    """
    The arithmetic Γ-function: Γ_arith(s) = |ζ(s)|²
    
    This is the Clockfield lapse function transported to number theory.
    Γ_arith → 0 at zeros of ζ (frozen cores)
    Γ_arith → 1 far from zeros in the convergence region
    """
    return zeta_modulus_squared(sigma, t)


def arithmetic_gamma_grid(sigma_range, t_range, n_sigma=200, n_t=200):
    """Compute Γ_arith on a grid."""
    sigmas = np.linspace(sigma_range[0], sigma_range[1], n_sigma)
    ts = np.linspace(t_range[0], t_range[1], n_t)
    
    G = np.zeros((n_t, n_sigma))
    for i, t in enumerate(ts):
        for j, sigma in enumerate(sigmas):
            try:
                G[i, j] = arithmetic_gamma(sigma, t)
            except:
                G[i, j] = np.nan
    
    return sigmas, ts, G


# ─────────────────────────────────────────────
# 2. Known Riemann Zeros (first 30)
# ─────────────────────────────────────────────

# First 30 non-trivial zeros: ρ_n = 1/2 + i·γ_n
RIEMANN_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
]


# ─────────────────────────────────────────────
# 3. Null Geodesics of the Arithmetic Metric
# ─────────────────────────────────────────────

def null_geodesic_arithmetic(sigma_start, t_center, direction=+1, 
                              n_steps=50000, ds=0.0001):
    """
    Integrate a σ-directed null geodesic of ds²_arith = -|ζ|⁴ dσ² + dt²
    
    Null condition: |ζ|⁴ (dσ/dt)² = 1
    So: dσ/dt = direction / |ζ|²
    
    Wait — let me redo this carefully.
    
    ds² = -|ζ|⁴ dσ² + dt² = 0
    ⟹ dt² = |ζ|⁴ dσ²
    ⟹ dt/dσ = |ζ|²
    ⟹ dσ/dt = 1/|ζ|²   (the σ-speed is INVERSE of Γ_arith)
    
    Hmm, this means near a zero, dσ/dt → ∞. Signals move FASTER 
    toward the zero. That's the opposite of the Clockfield.
    
    Let me reconsider the metric signature. In the Clockfield:
    ds² = -Γ²c₀² dt² + dr²
    
    The "lapse" is Γ, and small Γ means slow propagation in the r-direction.
    The null geodesic is dr/dt = Γc₀.
    
    For the arithmetic analog, we want the same structure:
    ds² = -Γ_arith² dσ² + dt²   (NOT -Γ⁴)
    
    No wait. In the Clockfield, the metric is:
    g_tt = -Γ², g_rr = 1
    
    Null: -Γ² (dt)² + (dr)² = 0 ⟹ dr/dt = Γ
    
    For the arithmetic metric, we want:
    g_σσ = -Γ_arith², g_tt = 1   ... but this makes t timelike and σ spacelike.
    
    Actually, let's think about this more carefully.
    In the critical strip, σ plays the role of the "radial" direction
    (depth into the freeze) and t plays the role of "time" (the imaginary part).
    
    So the correct metric is:
    ds² = -dt² + dσ² / Γ_arith²
    
    where t is timelike and σ is spacelike. Null geodesics:
    -dt² + dσ²/Γ² = 0 ⟹ dσ/dt = Γ_arith = |ζ|²
    
    Near a zero: Γ_arith → 0, so dσ/dt → 0. The geodesic slows down.
    This is the correct analog!
    
    Actually, the cleanest version matching the Clockfield exactly:
    ds² = -Γ_arith² dt² + dσ²
    
    with σ as "space" and t as "time". Then:
    dσ/dt = Γ_arith = |ζ(σ+it)|²
    
    Near a zero: dσ/dt → 0. Frozen. ✓
    """
    sigma = sigma_start
    t = t_center
    
    sigmas = [sigma]
    ts = [t]
    gammas = [arithmetic_gamma(sigma, t)]
    
    for _ in range(n_steps):
        g = arithmetic_gamma(sigma, t)
        if g is None or np.isnan(g):
            break
        
        # dσ/dt = direction * Γ_arith = direction * |ζ(σ+it)|²
        d_sigma = direction * g * ds
        sigma += d_sigma
        t += ds
        
        sigmas.append(sigma)
        ts.append(t)
        gammas.append(g)
        
        # Stop if we've gone too far
        if sigma < -1 or sigma > 3:
            break
    
    return {
        'sigma': np.array(sigmas),
        't': np.array(ts),
        'gamma': np.array(gammas),
    }


# ─────────────────────────────────────────────
# 4. Curvature Near a Zero
# ─────────────────────────────────────────────

def curvature_near_zero(gamma_n, n_points=100, delta=0.1):
    """
    Compute the Gaussian curvature of ds²_arith near the n-th zero
    ρ_n = 1/2 + i·γ_n.
    
    The metric: ds² = -|ζ|² dt² + dσ² (using Γ = |ζ|, not |ζ|²)
    
    Actually, let's use the 2D Riemannian metric for curvature:
    ds² = |ζ(σ+it)|² (dσ² + dt²)    [conformal metric]
    
    For a conformal metric ds² = e^{2φ}(dx² + dy²), the Gaussian curvature is:
    K = -e^{-2φ} Δφ
    
    where φ = (1/2) log|ζ(σ+it)|²  = log|ζ(σ+it)|.
    
    Near a simple zero ρ: ζ(s) ~ c(s-ρ), so |ζ| ~ |c||s-ρ|, 
    and φ ~ log|c| + log|s-ρ| = log|c| + (1/2)log((σ-1/2)²+(t-γ)²)
    
    Δφ = Δ[log|s-ρ|] = 0 for s ≠ ρ (harmonic function)
    
    So K = 0 away from the zero! The conformal metric is flat.
    
    This means the simple conformal metric isn't the right choice.
    The Lorentzian metric ds² = -Γ² dt² + dσ² is what we need.
    
    For this metric (Lorentzian, 1+1D), the scalar curvature is:
    R = -2 (∂²_σ Γ)/Γ    (for Γ = Γ(σ,t))
    
    More precisely, for ds² = -N² dt² + dσ² with N = Γ(σ,t):
    R = -(2/N)(∂²N/∂σ² + ∂²N/∂t²)  ... but this isn't quite right for Lorentzian.
    
    For a 2D metric ds² = -A(x)²dt² + dx², the Ricci scalar is:
    R = -2 A''/A
    
    where primes are d/dx (here d/dσ). Let me compute this numerically.
    """
    results = []
    
    for r in np.linspace(0.01, delta, n_points):
        # Sample points around the zero at radius r
        # The zero is at σ=0.5, t=γ_n
        angles = np.linspace(0, 2*np.pi, 36, endpoint=False)
        
        sigma_0 = 0.5
        t_0 = gamma_n
        
        # Compute Γ = |ζ|² at several points near the zero
        gamma_at_r = []
        for theta in angles:
            s = sigma_0 + r * np.cos(theta)
            t_val = t_0 + r * np.sin(theta)
            g = arithmetic_gamma(s, t_val)
            if g is not None:
                gamma_at_r.append(g)
        
        avg_gamma = np.mean(gamma_at_r) if gamma_at_r else 0
        
        # Numerical second derivative of Γ w.r.t. σ
        eps = 0.001
        g_plus = arithmetic_gamma(sigma_0 + r + eps, t_0)
        g_center = arithmetic_gamma(sigma_0 + r, t_0)
        g_minus = arithmetic_gamma(sigma_0 + r - eps, t_0)
        
        if g_plus and g_center and g_minus and g_center > 1e-15:
            d2g = (g_plus - 2*g_center + g_minus) / eps**2
            R_scalar = -2 * d2g / g_center
        else:
            R_scalar = np.nan
        
        results.append({
            'r': float(r),
            'avg_gamma': float(avg_gamma),
            'R_scalar': float(R_scalar) if not np.isnan(R_scalar) else None,
        })
    
    return results


# ─────────────────────────────────────────────
# 5. BPS Symmetry Verification
# ─────────────────────────────────────────────

def verify_functional_equation_symmetry(t_values=None, n_sigma=200):
    """
    Verify that |ζ(σ+it)|² is symmetric about σ = 1/2
    (up to the gamma factor correction in the completed ξ function).
    
    The raw |ζ| is NOT symmetric — only |ξ| is.
    But the *zeros* are symmetric, and the qualitative freeze structure is.
    """
    if t_values is None:
        t_values = [14.13, 21.02, 30.0, 50.0]
    
    sigmas = np.linspace(0.05, 0.95, n_sigma)
    
    results = {}
    for t_val in t_values:
        zeta_left = []
        zeta_right = []
        
        for sigma in sigmas:
            g = arithmetic_gamma(sigma, t_val)
            g_mirror = arithmetic_gamma(1.0 - sigma, t_val)
            if g is not None and g_mirror is not None:
                zeta_left.append(g)
                zeta_right.append(g_mirror)
        
        # Also compute with ξ (completed)
        xi_left = []
        xi_right = []
        for sigma in sigmas:
            s = mpmath.mpc(sigma, t_val)
            s_mirror = mpmath.mpc(1.0 - sigma, t_val)
            
            # ξ(s) = (1/2)s(s-1)π^(-s/2)Γ(s/2)ζ(s)
            xi_s = 0.5 * s * (s - 1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)
            xi_m = 0.5 * s_mirror * (s_mirror - 1) * mpmath.power(mpmath.pi, -s_mirror/2) * mpmath.gamma(s_mirror/2) * mpmath.zeta(s_mirror)
            
            xi_left.append(float(abs(xi_s)**2))
            xi_right.append(float(abs(xi_m)**2))
        
        # Asymmetry measure for |ζ|²
        zeta_asym = np.mean(np.abs(np.array(zeta_left) - np.array(zeta_right))) / (np.mean(zeta_left) + 1e-15)
        
        # Asymmetry measure for |ξ|²  
        xi_asym = np.mean(np.abs(np.array(xi_left) - np.array(xi_right))) / (np.mean(xi_left) + 1e-15)
        
        results[f't={t_val}'] = {
            'zeta_asymmetry': float(zeta_asym),
            'xi_asymmetry': float(xi_asym),  # should be ~0
        }
    
    return results


# ─────────────────────────────────────────────
# 6. ADM Mass Analog Near Zeros
# ─────────────────────────────────────────────

def adm_mass_near_zero(gamma_n, sigma_zero=0.5, radius=0.5, n_angles=360):
    """
    Compute the "ADM mass" analog near a zero on the critical line.
    
    M = ∮ (1 - Γ_arith) dl
    
    integrated around a circle of given radius centered on the zero.
    
    For a zero at ρ = 1/2 + iγ:
    M(ρ) = ∫₀²π (1 - |ζ(1/2 + radius·cos(θ) + i(γ + radius·sin(θ)))|²) radius dθ
    
    If M > 0 for all zeros on the critical line, and M < 0 for hypothetical
    zeros off the critical line, that would imply RH.
    """
    angles = np.linspace(0, 2*np.pi, n_angles, endpoint=False)
    dtheta = 2*np.pi / n_angles
    
    mass = 0.0
    gamma_values = []
    
    for theta in angles:
        sigma = sigma_zero + radius * np.cos(theta)
        t = gamma_n + radius * np.sin(theta)
        
        g = arithmetic_gamma(sigma, t)
        if g is not None:
            # Clamp: in some regions |ζ|² >> 1, so 1-Γ can be very negative.
            # This is a key difference from the Clockfield where 0 ≤ Γ ≤ 1 always.
            mass += (1.0 - g) * radius * dtheta
            gamma_values.append(g)
    
    return {
        'gamma_n': float(gamma_n),
        'sigma_zero': float(sigma_zero),
        'radius': float(radius),
        'adm_mass': float(mass),
        'avg_gamma': float(np.mean(gamma_values)) if gamma_values else None,
        'min_gamma': float(np.min(gamma_values)) if gamma_values else None,
        'max_gamma': float(np.max(gamma_values)) if gamma_values else None,
    }


def adm_mass_off_critical_line(gamma_n, sigma_zero, radius=0.5, n_angles=360):
    """
    Same computation but for a hypothetical zero at σ ≠ 1/2.
    We compute the ADM mass as if the "frozen core" were at (sigma_zero, gamma_n).
    """
    return adm_mass_near_zero(gamma_n, sigma_zero=sigma_zero, radius=radius, n_angles=n_angles)


# ─────────────────────────────────────────────
# 7. The Characteristic Cone on the Critical Strip
# ─────────────────────────────────────────────

def characteristic_cone_profile(t_fixed=14.134725, sigma_range=(0.05, 2.0), n_points=500):
    """
    Compute the characteristic cone opening |ζ(σ+it)|² as a function of σ
    at a fixed t (imaginary part).
    
    This is the arithmetic analog of the Clockfield's c_eff(r).
    """
    sigmas = np.linspace(sigma_range[0], sigma_range[1], n_points)
    gammas = []
    
    for sigma in sigmas:
        g = arithmetic_gamma(sigma, t_fixed)
        gammas.append(g if g is not None else np.nan)
    
    return {
        'sigma': sigmas.tolist(),
        'gamma_arith': gammas,
        't_fixed': t_fixed,
    }


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    if not HAS_MPMATH:
        print("ERROR: mpmath required. pip install mpmath")
        return
    
    print("=" * 70)
    print("ARITHMETIC CLOCKFIELD METRIC: NUMERICAL EXPLORATION")
    print("Toward the Riemann Hypothesis via Causal Structure")
    print("=" * 70)
    
    results = {}
    
    # 1. Γ_arith at known zeros
    print("\n--- 1. Arithmetic Γ at Known Zeros ---")
    zero_gammas = []
    for i, gamma_n in enumerate(RIEMANN_ZEROS[:10]):
        g = arithmetic_gamma(0.5, gamma_n)
        zeta_val = float(abs(mpmath.zeta(mpmath.mpc(0.5, gamma_n))))
        print(f"  ρ_{i+1} = 1/2 + i·{gamma_n:.6f}:  |ζ| = {zeta_val:.2e},  Γ_arith = {g:.2e}")
        zero_gammas.append({
            'n': i+1, 
            'gamma_n': gamma_n, 
            'zeta_modulus': float(zeta_val),
            'gamma_arith': float(g)
        })
    results['zeros_gamma'] = zero_gammas
    
    # 2. Characteristic speed profile near first zero
    print("\n--- 2. Characteristic Speed Profile (t = γ₁) ---")
    profile = characteristic_cone_profile(t_fixed=RIEMANN_ZEROS[0])
    # Find the minimum
    valid = [(s, g) for s, g in zip(profile['sigma'], profile['gamma_arith']) if g is not None and not np.isnan(g)]
    if valid:
        min_pair = min(valid, key=lambda x: x[1])
        print(f"  Minimum Γ_arith at σ = {min_pair[0]:.4f}: Γ = {min_pair[1]:.2e}")
        print(f"  (Expected minimum at σ = 0.5, since t = γ₁ is a zero)")
    results['profile_first_zero'] = {
        'min_sigma': float(min_pair[0]) if valid else None,
        'min_gamma': float(min_pair[1]) if valid else None,
    }
    
    # 3. BPS symmetry (functional equation)
    print("\n--- 3. BPS Symmetry: |ξ(s)|² = |ξ(1-s)|² ---")
    sym = verify_functional_equation_symmetry(t_values=[14.13, 30.0, 50.0])
    for key, val in sym.items():
        print(f"  {key}: |ζ|² asymmetry = {val['zeta_asymmetry']:.4f}, |ξ|² asymmetry = {val['xi_asymmetry']:.2e}")
    results['bps_symmetry'] = sym
    
    # 4. ADM mass at zeros ON the critical line
    print("\n--- 4. ADM Mass at Zeros on Critical Line (σ = 1/2) ---")
    adm_on = []
    for i, gamma_n in enumerate(RIEMANN_ZEROS[:10]):
        m = adm_mass_near_zero(gamma_n, sigma_zero=0.5, radius=0.3)
        print(f"  ρ_{i+1}: M = {m['adm_mass']:.4f}, avg Γ = {m['avg_gamma']:.4f}")
        adm_on.append(m)
    results['adm_mass_on_line'] = adm_on
    
    # 5. ADM mass at hypothetical zeros OFF the critical line
    print("\n--- 5. ADM Mass at Hypothetical Off-Line Zeros ---")
    adm_off = []
    for sigma_test in [0.3, 0.4, 0.5, 0.6, 0.7]:
        m = adm_mass_off_critical_line(RIEMANN_ZEROS[0], sigma_zero=sigma_test, radius=0.3)
        marker = " ← critical line" if abs(sigma_test - 0.5) < 0.01 else ""
        print(f"  σ = {sigma_test}: M = {m['adm_mass']:.4f}, avg Γ = {m['avg_gamma']:.4f}{marker}")
        adm_off.append(m)
    results['adm_mass_off_line'] = adm_off
    
    # 6. Curvature near first zero
    print("\n--- 6. Scalar Curvature Near First Zero ---")
    curv = curvature_near_zero(RIEMANN_ZEROS[0], n_points=20, delta=0.2)
    for c in curv[:5]:
        R_str = f"{c['R_scalar']:.2f}" if c['R_scalar'] is not None else "N/A"
        print(f"  r = {c['r']:.4f}: avg Γ = {c['avg_gamma']:.4e}, R = {R_str}")
    results['curvature'] = curv
    
    # 7. Null geodesic approaching first zero
    print("\n--- 7. Null Geodesic Toward First Zero ---")
    print("  (Computing... this may take a moment)")
    geo = null_geodesic_arithmetic(sigma_start=1.5, t_center=RIEMANN_ZEROS[0] - 2.0,
                                    direction=-1, n_steps=10000, ds=0.001)
    print(f"  Start: σ = {geo['sigma'][0]:.4f}, t = {geo['t'][0]:.4f}")
    print(f"  End:   σ = {geo['sigma'][-1]:.4f}, t = {geo['t'][-1]:.4f}")
    print(f"  Γ_arith at end: {geo['gamma'][-1]:.4e}")
    print(f"  Steps: {len(geo['sigma'])}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: ARITHMETIC CLOCKFIELD STRUCTURE")
    print("=" * 70)
    
    # Check: are ADM masses consistently positive on the line?
    on_line_masses = [m['adm_mass'] for m in adm_on]
    all_positive = all(m > 0 for m in on_line_masses)
    print(f"\n  ADM mass positive for all zeros on critical line: {all_positive}")
    print(f"  Range: [{min(on_line_masses):.4f}, {max(on_line_masses):.4f}]")
    
    # Check: does ADM mass vary with σ for off-line positions?
    off_masses = [(m['sigma_zero'], m['adm_mass']) for m in adm_off]
    print(f"\n  ADM mass vs σ for hypothetical off-line zeros (t = γ₁):")
    for sigma, mass in off_masses:
        marker = " ← minimum?" if abs(sigma - 0.5) < 0.01 else ""
        print(f"    σ = {sigma:.1f}: M = {mass:.4f}{marker}")
    
    # The key question
    print("\n  KEY QUESTION: Is the ADM mass minimized at σ = 1/2?")
    sigma_vals = [m['sigma_zero'] for m in adm_off]
    mass_vals = [m['adm_mass'] for m in adm_off]
    min_idx = np.argmin(mass_vals)
    print(f"  Minimum mass at σ = {sigma_vals[min_idx]:.1f} with M = {mass_vals[min_idx]:.4f}")
    
    if abs(sigma_vals[min_idx] - 0.5) < 0.01:
        print("  ⟹ YES — the critical line is the energy minimum.")
        print("  ⟹ This is CONSISTENT with the BPS uniqueness argument for RH.")
    else:
        print(f"  ⟹ NO — minimum at σ = {sigma_vals[min_idx]:.2f}, not 1/2.")
        print("  ⟹ The simple ADM mass functional does not select the critical line.")
        print("  ⟹ A more refined energy functional is needed.")
    
    results['summary'] = {
        'adm_positive_on_line': all_positive,
        'adm_minimum_sigma': float(sigma_vals[min_idx]),
        'adm_minimum_mass': float(mass_vals[min_idx]),
        'selects_critical_line': abs(sigma_vals[min_idx] - 0.5) < 0.01,
    }
    
    # Save
    # Convert for JSON
    def convert(obj):
        if isinstance(obj, (np.floating, float)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return obj
    
    output_path = 'riemann_results.json'
    clean = json.loads(json.dumps(results, default=convert))
    with open(output_path, 'w') as f:
        json.dump(clean, f, indent=2)
    print(f"\n  Results saved to {output_path}")
    
    return results


if __name__ == '__main__':
    main()

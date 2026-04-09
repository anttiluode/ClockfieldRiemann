"""
plot_arithmetic_clockfield.py

Comprehensive visualization of the Arithmetic Clockfield Metric
and its connection to the Riemann Hypothesis.

Antti Luode — PerceptionLab, Helsinki, Finland
Claude Opus (Anthropic) — Implementation
April 2026
"""

import numpy as np
import mpmath
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
import matplotlib.patches as mpatches

# ─────────────────────────────────────────────
# Constants & Known Zeros
# ─────────────────────────────────────────────

RIEMANN_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
]

def zeta_mod_sq(sigma, t):
    """Compute |ζ(σ+it)|²"""
    try:
        z = mpmath.zeta(mpmath.mpc(sigma, t))
        return float(abs(z)**2)
    except:
        return np.nan

def xi_mod_sq(sigma, t):
    """Compute |ξ(s)|² = |½s(s-1)π^(-s/2)Γ(s/2)ζ(s)|²"""
    try:
        s = mpmath.mpc(sigma, t)
        xi = 0.5 * s * (s - 1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)
        return float(abs(xi)**2)
    except:
        return np.nan


# ─────────────────────────────────────────────
# Panel 1: The Arithmetic Γ Landscape
# ─────────────────────────────────────────────

def plot_gamma_landscape(ax):
    """Heat map of log|ζ(σ+it)|² on the critical strip."""
    n_s, n_t = 150, 200
    sigmas = np.linspace(0.05, 1.5, n_s)
    ts = np.linspace(10, 55, n_t)
    
    G = np.zeros((n_t, n_s))
    for i, t in enumerate(ts):
        for j, sigma in enumerate(sigmas):
            G[i, j] = zeta_mod_sq(sigma, t)
    
    # Log scale, handle zeros
    G_log = np.log10(np.maximum(G, 1e-20))
    
    im = ax.pcolormesh(sigmas, ts, G_log, cmap='RdYlBu_r', shading='auto',
                       vmin=-15, vmax=2)
    
    # Mark critical line
    ax.axvline(0.5, color='lime', linewidth=2, linestyle='--', label='σ = 1/2')
    
    # Mark zeros
    for gamma_n in RIEMANN_ZEROS:
        if 10 < gamma_n < 55:
            ax.plot(0.5, gamma_n, 'w*', markersize=8, markeredgecolor='black', markeredgewidth=0.5)
    
    ax.set_xlabel('σ = Re(s)', fontsize=11)
    ax.set_ylabel('t = Im(s)', fontsize=11)
    ax.set_title('Arithmetic Γ: log₁₀|ζ(σ+it)|²\n(Zeros = Frozen Cores)', fontsize=12)
    ax.legend(fontsize=8, loc='upper right')
    
    plt.colorbar(im, ax=ax, label='log₁₀ Γ_arith', shrink=0.8)


# ─────────────────────────────────────────────
# Panel 2: Characteristic Speed at t = γ₁
# ─────────────────────────────────────────────

def plot_characteristic_speed(ax):
    """Plot |ζ(σ + iγ₁)|² vs σ — the analog of c_eff(r)."""
    gamma1 = RIEMANN_ZEROS[0]
    sigmas = np.linspace(0.05, 2.0, 400)
    
    gammas = [zeta_mod_sq(s, gamma1) for s in sigmas]
    gammas = np.array(gammas)
    
    ax.semilogy(sigmas, np.maximum(gammas, 1e-20), 'b-', linewidth=2)
    ax.axvline(0.5, color='green', linestyle='--', linewidth=2, label='Critical line σ=1/2')
    
    # Mark the zero
    ax.plot(0.5, max(zeta_mod_sq(0.5, gamma1), 1e-16), 'r*', markersize=15, 
            label=f'Zero at ρ₁ = 1/2 + i·{gamma1:.2f}')
    
    # Mark the functional equation symmetry
    ax.axvspan(0, 0.5, alpha=0.05, color='red', label='σ < 1/2')
    ax.axvspan(0.5, 2.0, alpha=0.05, color='blue', label='σ > 1/2')
    
    ax.set_xlabel('σ = Re(s)', fontsize=11)
    ax.set_ylabel('Γ_arith = |ζ(σ+it)|²', fontsize=11)
    ax.set_title(f'Characteristic Speed at t = γ₁ = {gamma1:.2f}\n(Freeze at σ = 1/2)', fontsize=12)
    ax.legend(fontsize=7, loc='upper right')
    ax.set_xlim(0, 2)
    ax.grid(True, alpha=0.3)


# ─────────────────────────────────────────────
# Panel 3: BPS Symmetry — |ξ(s)|² = |ξ(1-s)|²
# ─────────────────────────────────────────────

def plot_bps_symmetry(ax):
    """Show the perfect σ ↔ 1-σ symmetry of the completed ξ function."""
    gamma1 = RIEMANN_ZEROS[0]
    sigmas = np.linspace(0.05, 0.95, 100)
    
    xi_left = []
    xi_right = []
    zeta_left = []
    zeta_right = []
    
    for sigma in sigmas:
        xi_left.append(xi_mod_sq(sigma, gamma1))
        xi_right.append(xi_mod_sq(1.0 - sigma, gamma1))
        zeta_left.append(zeta_mod_sq(sigma, gamma1))
        zeta_right.append(zeta_mod_sq(1.0 - sigma, gamma1))
    
    ax.semilogy(sigmas, np.maximum(xi_left, 1e-30), 'b-', linewidth=2, label='|ξ(σ+it)|²')
    ax.semilogy(sigmas, np.maximum(xi_right, 1e-30), 'r--', linewidth=2, label='|ξ(1-σ+it)|²')
    ax.semilogy(sigmas, np.maximum(zeta_left, 1e-30), 'b:', linewidth=1, alpha=0.5, label='|ζ(σ+it)|² (raw)')
    ax.semilogy(sigmas, np.maximum(zeta_right, 1e-30), 'r:', linewidth=1, alpha=0.5, label='|ζ(1-σ+it)|² (raw)')
    
    ax.axvline(0.5, color='green', linestyle='--', linewidth=2)
    
    ax.set_xlabel('σ', fontsize=11)
    ax.set_ylabel('Modulus squared', fontsize=11)
    ax.set_title('BPS Condition: ξ(s) = ξ(1−s)\n(Perfect symmetry = Functional Equation)', fontsize=12)
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)


# ─────────────────────────────────────────────
# Panel 4: Curvature Near First Zero
# ─────────────────────────────────────────────

def plot_curvature(ax):
    """Scalar curvature of the arithmetic metric near ρ₁."""
    gamma1 = RIEMANN_ZEROS[0]
    radii = np.linspace(0.005, 0.3, 80)
    
    curvatures = []
    gammas_avg = []
    
    for r in radii:
        # Compute d²Γ/dσ² at (0.5+r, γ₁) using central differences
        eps = 0.001
        sigma = 0.5 + r
        g_p = zeta_mod_sq(sigma + eps, gamma1)
        g_c = zeta_mod_sq(sigma, gamma1)
        g_m = zeta_mod_sq(sigma - eps, gamma1)
        
        if g_c > 1e-20:
            d2g = (g_p - 2*g_c + g_m) / eps**2
            R = -2 * d2g / g_c
            curvatures.append(R)
        else:
            curvatures.append(np.nan)
        gammas_avg.append(g_c)
    
    curvatures = np.array(curvatures)
    
    # Plot
    ax.plot(radii, curvatures, 'r-', linewidth=2)
    ax.axhline(0, color='gray', linestyle='-', alpha=0.3)
    
    # Fit: R ~ -A/r² for small r
    valid_mask = ~np.isnan(curvatures) & (radii < 0.1) & (radii > 0.01)
    if np.any(valid_mask):
        r_fit = radii[valid_mask]
        c_fit = curvatures[valid_mask]
        # Fit log|R| vs log(r) to check power law
        neg_mask = c_fit < 0
        if np.any(neg_mask):
            log_r = np.log(r_fit[neg_mask])
            log_c = np.log(-c_fit[neg_mask])
            if len(log_r) > 2:
                coeffs = np.polyfit(log_r, log_c, 1)
                power = coeffs[0]
                ax.text(0.15, np.nanmin(curvatures)*0.3, 
                        f'R ~ r^{power:.2f}\n(predicted: r^{{-2}})', 
                        fontsize=9, color='red')
    
    ax.set_xlabel('Distance from zero (σ − 1/2)', fontsize=11)
    ax.set_ylabel('Scalar curvature R', fontsize=11)
    ax.set_title('Curvature Near ρ₁: Negative Divergence\n(Hyperbolic Core = Frozen Soliton)', fontsize=12)
    ax.grid(True, alpha=0.3)


# ─────────────────────────────────────────────
# Panel 5: ADM Mass vs σ (The Key Test)
# ─────────────────────────────────────────────

def plot_adm_mass(ax):
    """ADM mass integral as a function of σ for several zeros."""
    sigma_range = np.linspace(0.1, 0.9, 30)
    
    for idx, gamma_n in enumerate(RIEMANN_ZEROS[:4]):
        masses = []
        for sigma_0 in sigma_range:
            # Compute M = ∮(1 - Γ_arith) dl around circle of radius 0.3
            radius = 0.25
            n_angles = 180
            angles = np.linspace(0, 2*np.pi, n_angles, endpoint=False)
            dtheta = 2*np.pi / n_angles
            
            mass = 0.0
            for theta in angles:
                s = sigma_0 + radius * np.cos(theta)
                t = gamma_n + radius * np.sin(theta)
                g = zeta_mod_sq(s, t)
                if not np.isnan(g):
                    mass += (1.0 - min(g, 10.0)) * radius * dtheta
            
            masses.append(mass)
        
        label = f'ρ_{idx+1} (γ={gamma_n:.1f})'
        ax.plot(sigma_range, masses, '-', linewidth=2, label=label)
    
    ax.axvline(0.5, color='green', linestyle='--', linewidth=2, label='σ = 1/2')
    ax.set_xlabel('σ (position of hypothetical zero)', fontsize=11)
    ax.set_ylabel('ADM mass M(σ)', fontsize=11)
    ax.set_title('"ADM Mass" vs σ\n(Testing the BPS Uniqueness Argument)', fontsize=12)
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)


# ─────────────────────────────────────────────
# Panel 6: The Parallel Structure Diagram
# ─────────────────────────────────────────────

def plot_parallel_diagram(ax):
    """Schematic showing the Clockfield ↔ Arithmetic parallel."""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'The Parallel Structure', fontsize=14, fontweight='bold', 
            ha='center', va='top')
    
    # Left column: Clockfield
    ax.text(2.5, 8.5, 'CLOCKFIELD', fontsize=12, fontweight='bold', ha='center', color='#2196F3')
    
    items_left = [
        ('Γ(β) = 1/(1+τβ)²', 7.5),
        ('Frozen core (Γ→0)', 6.5),
        ('Γ-shell = Cauchy horizon', 5.5),
        ('BPS: dΓ/dβ = −2τΓ^{3/2}', 4.5),
        ('Winding number n ∈ ℤ', 3.5),
        ('Energy positivity\n(Bogomolny)', 2.5),
        ('ds² = −Γ²dt² + dr²', 1.5),
    ]
    
    for text, y in items_left:
        ax.text(2.5, y, text, fontsize=8, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#E3F2FD', edgecolor='#2196F3', alpha=0.8))
    
    # Right column: Arithmetic
    ax.text(7.5, 8.5, 'ARITHMETIC', fontsize=12, fontweight='bold', ha='center', color='#F44336')
    
    items_right = [
        ('Γ_arith = |ζ(s)|²', 7.5),
        ('Zeros of ζ (Γ→0)', 6.5),
        ('Critical line = Cauchy horizon', 5.5),
        ('BPS: ξ(s) = ξ(1−s)', 4.5),
        ('Zero index n ∈ ℤ', 3.5),
        ('Weil positivity\n(≡ RH)', 2.5),
        ('ds² = −|ζ|⁴dσ² + dt²', 1.5),
    ]
    
    for text, y in items_right:
        ax.text(7.5, y, text, fontsize=8, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFEBEE', edgecolor='#F44336', alpha=0.8))
    
    # Arrows connecting
    for _, y in items_left:
        ax.annotate('', xy=(5.8, y), xytext=(4.2, y),
                    arrowprops=dict(arrowstyle='<->', color='gray', lw=1))
    
    # Bottom: the gap
    ax.text(5, 0.5, 'THE GAP: Weil positivity = Bogomolny inequality for ζ?\nThis is the Riemann Hypothesis.', 
            fontsize=9, ha='center', va='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF9C4', edgecolor='#FFC107', alpha=0.9))


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print("Computing arithmetic Clockfield visualizations...")
    print("(This will take a few minutes due to zeta function evaluations)")
    
    fig, axes = plt.subplots(2, 3, figsize=(20, 14))
    fig.suptitle('Arithmetic Clockfield Metric: Toward RH via Causal Structure\n'
                 'Antti Luode — PerceptionLab | Claude Opus — Anthropic | April 2026',
                 fontsize=15, fontweight='bold')
    
    print("  Panel 1: Γ_arith landscape...")
    plot_gamma_landscape(axes[0, 0])
    
    print("  Panel 2: Characteristic speed...")
    plot_characteristic_speed(axes[0, 1])
    
    print("  Panel 3: BPS symmetry...")
    plot_bps_symmetry(axes[0, 2])
    
    print("  Panel 4: Curvature near zero...")
    plot_curvature(axes[1, 0])
    
    print("  Panel 5: ADM mass test...")
    plot_adm_mass(axes[1, 1])
    
    print("  Panel 6: Parallel structure...")
    plot_parallel_diagram(axes[1, 2])
    
    plt.tight_layout()
    
    output = 'clockfield_riemann.png'
    plt.savefig(output, dpi=150, bbox_inches='tight')
    print(f"\nSaved: {output}")
    plt.close()


if __name__ == '__main__':
    main()

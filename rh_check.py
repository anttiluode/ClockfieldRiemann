import mpmath as mp
mp.mp.dps = 30

def xi(s):
    s = mp.mpc(s)
    return 0.5*s*(s-1)*mp.power(mp.pi,-s/2)*mp.gamma(s/2)*mp.zeta(s)

def F2_fd(t, eps=mp.mpf('1e-6'), f=xi):
    """Finite-difference d^2/dsigma^2 |f(sigma+it)|^2 at sigma=1/2."""
    g = lambda sig: abs(f(mp.mpc(sig, t)))**2
    return (g(mp.mpf('0.5')+eps) + g(mp.mpf('0.5')-eps) - 2*g(mp.mpf('0.5')))/eps**2

def logderiv2(t, f=xi):
    """(f'/f)'(1/2+it) via mpmath derivatives."""
    s0 = mp.mpc('0.5', t)
    fp  = mp.diff(f, s0)
    fpp = mp.diff(f, s0, 2)
    return fpp/f(s0) - (fp/f(s0))**2

print("1. LEMMA CHECK: F''(1/2) =?= 2|xi|^2 Re(xi'/xi)'")
for t in ['5','14.2','30']:
    t = mp.mpf(t)
    lhs = F2_fd(t)
    rhs = 2*abs(xi(mp.mpc('0.5',t)))**2 * mp.re(logderiv2(t))
    print(f"  t={float(t):6.2f}: FD={mp.nstr(lhs,8)}  identity={mp.nstr(rhs,8)}  reldiff={mp.nstr(abs(lhs-rhs)/abs(rhs),3)}")

print()
print("2. LAGUERRE IDENTITY: F''(1/2) =?= 2*(Xi'(t)^2 - Xi(t)*Xi''(t))")
Xi = lambda t: mp.re(xi(mp.mpc('0.5', t)))   # xi is real on the line
for t in ['5','14.2','30']:
    t = mp.mpf(t)
    lhs = F2_fd(t)
    Xp  = mp.diff(Xi, t)
    Xpp = mp.diff(Xi, t, 2)
    rhs = 2*(Xp**2 - Xi(t)*Xpp)
    print(f"  t={float(t):6.2f}: F''={mp.nstr(lhs,8)}  2*Laguerre={mp.nstr(rhs,8)}  reldiff={mp.nstr(abs(lhs-rhs)/abs(rhs),3)}")

print()
print("3. HADAMARD FORMULA CHECK at s0 = 1/2 + 2i")
t = mp.mpf(2)
s0 = mp.mpc('0.5', t)
exact = logderiv2(t)
print(f"  exact (xi'/xi)'(s0)          = {mp.nstr(exact,8)}")
N = 250
zs = [mp.im(mp.zetazero(n)) for n in range(1, N+1)]
zsum = mp.mpf(0)
for g in zs:
    # zeros at 1/2 + ig and 1/2 - ig; s0 - rho = i(t -+ g)
    zsum += -(1/(mp.mpc(0,1)*(t-g))**2 + 1/(mp.mpc(0,1)*(t+g))**2)
gamN = zs[-1]
tail = 2*(mp.log(gamN/(2*mp.pi))/(2*mp.pi))*(2/gamN)   # ~ 2*integral density/g^2
zsum_corr = zsum + tail   # tail terms are +1/(t-g)^2-type, positive
print(f"  -sum over first {N} zero pairs = {mp.nstr(zsum,8)}   (+tail est. ~ {mp.nstr(tail,3)}) -> {mp.nstr(zsum_corr,8)}")
bracket = -1/s0**2 - 1/(s0-1)**2 + mp.polygamma(1, s0/2)/4
paper = bracket + zsum
print(f"  repo formula (bracket + sum)  = {mp.nstr(paper,8)}")
print(f"  bracket [-1/s^2-1/(s-1)^2+psi'(s/2)/4] = {mp.nstr(bracket,8)}")
print(f"  ==> exact - zerosum = {mp.nstr(exact - zsum,6)}  (should be ~tail if pure-zero-sum is right)")
print(f"  ==> exact - repoformula = {mp.nstr(exact - paper,6)}  (should be ~ -bracket if repo formula wrong)")

print()
print("4. COUNTEREXAMPLE: xi_fake(s) = cosh(s-1/2)*(delta^2-(s-1/2)^2)")
print("   functional eq xi(s)=xi(1-s): YES; real on critical line: YES")
print("   zeros: s = 1/2 +- delta  (OFF the critical line, on the real axis)")
def make_fake(delta):
    d = mp.mpf(delta)
    return lambda s: mp.cosh(mp.mpc(s)-mp.mpf('0.5'))*(d**2-(mp.mpc(s)-mp.mpf('0.5'))**2)
for delta in ['2','1']:
    fake = make_fake(delta)
    vals = []
    tt = mp.mpf('0')
    while tt <= 40:
        vals.append((float(tt), float(F2_fd(tt, f=fake, eps=mp.mpf('1e-5')))))
        tt += mp.mpf('0.25')
    mn = min(vals, key=lambda p: p[1])
    neg = [p for p in vals if p[1] < 0]
    print(f"  delta={delta}: min F''(1/2) over t in [0,40] = {mn[1]:.4f} at t={mn[0]:.2f}; "
          f"negative points: {len(neg)}/{len(vals)}"
          f"  => convexity {'HOLDS everywhere (zeros off line!)' if not neg else 'FAILS'}")

print()
print("5. REPRODUCE THEIR TABLE (spot checks, eps=1e-3 as in repo)")
for t in ['5.0','14.135','25.0']:
    t = mp.mpf(t)
    g = lambda sig: abs(xi(mp.mpc(sig,t)))**2
    e = mp.mpf('1e-3')
    d2 = (g(mp.mpf('0.5')+e)+g(mp.mpf('0.5')-e)-2*g(mp.mpf('0.5')))/e**2
    print(f"  t={float(t):7.3f}: |xi|^2={mp.nstr(g(mp.mpf('0.5')),4)}  d2={mp.nstr(d2,4)}  sign={'+' if d2>0 else '-'}")

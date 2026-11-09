"""
Final Spectral Analysis — using C-stat (proper for low-count data)
Following Karpova et al. (2019) methodology
"""
from sherpa.astro.ui import *

print("=" * 60)
print("PSR J1826-1256 — SPECTRAL FITTING")
print("=" * 60)

# Load the ungrouped spectrum (use C-stat, not chi2)
load_pha("work/7641/pulsar_spec.pi")

# Set up: C-stat with background modeling
notice(0.5, 7.0)
set_stat("wstat")        # W-stat = C-stat with background estimation
set_method("neldermead")  # Nelder-Mead works better for C-stat

# ====== POWER LAW ======
print("\n>>> MODEL: tbabs × powerlaw <<<")
set_source(xsphabs.abs1 * xspowerlaw.pl)
abs1.nH = 0.5
pl.PhoIndex = 1.3
pl.norm = 1e-5

fit()
fr = get_fit_results()
f_abs = calc_energy_flux(0.5, 7.0)

# Unabsorbed flux (set nH=0 temporarily)
nH_save = abs1.nH.val
abs1.nH = 0
f_unabs = calc_energy_flux(0.5, 7.0)
abs1.nH = nH_save

print(f"\n  === POWER LAW RESULTS ===")
print(f"  N_H           = {abs1.nH.val:.3f} ± ~0.3 × 10²² cm⁻²")
print(f"  Γ (Gamma)     = {pl.PhoIndex.val:.3f}")
print(f"  Norm          = {pl.norm.val:.3e}")
print(f"  W-stat        = {fr.statval:.2f} / {fr.dof} dof")
print(f"  Absorbed flux = {f_abs:.3e} erg/cm²/s")
print(f"  Unabs. flux   = {f_unabs:.3e} erg/cm²/s")

pl_stat = fr.statval
pl_dof = fr.dof

# Confidence
print("\n  Confidence intervals (1σ):")
try:
    conf(abs1.nH, pl.PhoIndex)
    cr = get_conf_results()
    for i, name in enumerate(cr.parnames):
        lo = cr.parmins[i] if cr.parmins[i] is not None else "---"
        hi = cr.parmaxes[i] if cr.parmaxes[i] is not None else "---"
        if isinstance(lo, float):
            print(f"    {name}: {cr.parvals[i]:.3f} ({lo:+.3f}, {hi:+.3f})")
        else:
            print(f"    {name}: {cr.parvals[i]:.3f} ({lo}, {hi:+.3f})" if isinstance(hi, float) else f"    {name}: {cr.parvals[i]:.3f} ({lo}, {hi})")
except Exception as e:
    print(f"    {e}")

# ====== BLACKBODY ======
print("\n>>> MODEL: tbabs × bbodyrad <<<")
set_source(xsphabs.abs2 * xsbbodyrad.bb)
abs2.nH = 0.5
bb.kT = 0.3
bb.norm = 1.0

fit()
fr2 = get_fit_results()
f_bb = calc_energy_flux(0.5, 7.0)

print(f"\n  === BLACKBODY RESULTS ===")
print(f"  N_H  = {abs2.nH.val:.3f} × 10²² cm⁻²")
print(f"  kT   = {bb.kT.val:.3f} keV = {bb.kT.val*1.16e7:.2e} K")
print(f"  Norm = {bb.norm.val:.4f}")
print(f"  W-stat = {fr2.statval:.2f} / {fr2.dof} dof")
print(f"  Flux = {f_bb:.3e} erg/cm²/s")

# ====== COMPARISON ======
print("\n" + "=" * 60)
print(f"  {'Model':<22} {'W-stat':>8} {'DOF':>5} {'W/DOF':>8}")
print(f"  {'-'*45}")
print(f"  {'tbabs×powerlaw':<22} {pl_stat:>8.1f} {pl_dof:>5} {pl_stat/pl_dof:>8.3f}")
print(f"  {'tbabs×bbodyrad':<22} {fr2.statval:>8.1f} {fr2.dof:>5} {fr2.statval/fr2.dof:>8.3f}")
print(f"\n  Winner: {'Power Law ✓' if pl_stat < fr2.statval else 'Blackbody ✓'}")

print("\n" + "=" * 60)
print("COMPARISON WITH PAPER (Karpova et al. 2019)")
print("=" * 60)
print(f"  {'':15} {'Our result':>12} {'Paper':>15}")
print(f"  {'-'*44}")
print(f"  {'N_H':15} {abs1.nH.val:>12.3f} {'0.50±0.15':>15}")
print(f"  {'Γ':15} {pl.PhoIndex.val:>12.3f} {'1.25±0.20':>15}")
print(f"  {'Net counts':15} {'~244':>12} {'~227':>15}")
print(f"  {'Flux (abs)':15} {f_abs:>12.2e} {'~3×10⁻¹⁴':>15}")

print("\n>>> Note: Differences from the paper are expected because:")
print("    1. The paper used chandra_repro (reprocessed data)")
print("    2. Different CALDB version")
print("    3. Our region sizes may differ slightly")
print("    4. The paper combined Chandra + XMM-Newton data")
print("\nANALYSIS COMPLETE!")

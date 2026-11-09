# 4. Comparison with Published Results

## My results vs the paper

### Power law (tbabs × powerlaw)

| Parameter | My result | Karpova et al. (2019) |
|-----------|:---------:|:---------------------:|
| N_H (10²² cm⁻²) | 0.83 ± 0.3 | 0.50 ± 0.15 |
| Γ | 0.39 ± 0.27 | 1.25 ± 0.20 |
| Absorbed flux (0.5–7 keV) | 5.95 × 10⁻¹⁴ | ~3 × 10⁻¹⁴ |
| Net counts | ~244 | ~227 |
| Fit statistic | W-stat = 420.7/443 | C-stat |

### Blackbody (tbabs × bbodyrad)

| Parameter | My result |
|-----------|:---------:|
| N_H (10²² cm⁻²) | 0.32 |
| kT | 2.05 keV |
| W-stat/dof | 423.1/443 |

Power law gives a lower statistic so it fits better, same conclusion as the paper.

## Why results differ

My values are off from the paper, especially Γ (0.39 vs 1.25). A few reasons:

1. **Low counts** — with only 244 photons there's a strong degeneracy between N_H and Γ. If N_H goes up, Γ goes down to compensate. My N_H is higher (0.83 vs 0.50) and my Γ is lower (0.39 vs 1.25), which is exactly this degeneracy.

2. **No reprocessing** — I used the archive evt2 directly instead of running chandra_repro. The paper reprocessed with updated calibrations which changes the energy assignments slightly.

3. **Different CALDB** — I used CALDB 4.12.3 (2025), the paper used an older version from ~2018. Updated calibrations change the ARF and RMF.

4. **Regions** — small differences in extraction regions affect which photons are included. With so few counts, even a handful of photons can shift the fit.

5. **Data combination** — the paper also used XMM-Newton data for their full analysis. I only used Chandra ObsID 7641.

6. **Fitting tool** — I used Sherpa with W-stat, they used XSPEC with C-stat. Both are valid for low-count data but can converge to slightly different minima.

---

# 5. Physical Interpretation

## What N_H tells us

N_H = 0.83 × 10²² cm⁻² is the amount of gas and dust between us and the pulsar. It absorbs soft X-rays preferentially. The total Galactic N_H in this direction is about 1.66 × 10²² (from NRAO), so the pulsar sits roughly halfway through the Galaxy's absorbing column — consistent with its estimated distance of ~1.2 kpc.

## What Γ tells us

The photon index Γ describes the spectrum slope (dN/dE ∝ E⁻ᴦ). The paper's Γ ~ 1.25 is a hard spectrum typical of young energetic pulsars — for comparison the Crab pulsar has Γ ~ 1.6. Hard spectra come from synchrotron radiation by ultra-relativistic electrons in the pulsar magnetosphere.

My Γ ~ 0.39 is unusually hard, likely because of the N_H–Γ degeneracy with limited statistics rather than a real physical difference.

## Why power law = non-thermal emission

A blackbody has a characteristic peak energy set by temperature — it's what you'd see from a hot neutron star surface. A power law is a straight line on a log-log plot with no preferred energy, which is the signature of non-thermal processes like synchrotron radiation from relativistic particles spiraling in the pulsar's magnetic field (~10¹² Gauss).

The power law fitting better confirms the X-rays come from the magnetosphere, not the neutron star surface.

## X-ray luminosity

Using the unabsorbed flux (6.8 × 10⁻¹⁴ erg/cm²/s) and distance ~1.2 kpc:

L_X ≈ 4π d² F ≈ 1.2 × 10³¹ erg/s

The spin-down luminosity is Ė ~ 3.6 × 10³⁶ erg/s, giving an X-ray efficiency of η ~ 10⁻⁵. This is typical — only a tiny fraction of the pulsar's rotational energy loss goes into X-rays. Most goes into the pulsar wind and nebula.

## Thermal vs non-thermal

| | Thermal (surface) | Non-thermal (magnetosphere) |
|--|---|---|
| Spectrum | Blackbody curve | Power law |
| Origin | Hot NS surface | Relativistic particles |
| Typical energy | kT ~ 0.1–0.3 keV | Γ ~ 1–2 |

For PSR J1826−1256 the power law dominance means we're seeing magnetospheric emission. Any thermal component from the surface is too faint to detect with ~244 counts.

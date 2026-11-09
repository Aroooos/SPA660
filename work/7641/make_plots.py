"""
Generate X-ray image and radial profile using only CIAO tools.
Run with CIAO's Python: python make_plots.py
"""
import pycrates
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

WORK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WORK))

# Pulsar position in image coords (from wavdetect: sky x=4004.3, y=4127.6)
# Image was binned x=3500:4500, y=3600:4600 so pixel = sky - offset
PSR_X = 4004.3 - 3500
PSR_Y = 4127.6 - 3600

# ========== PLOT 1: X-ray Field Image ==========
print("Creating X-ray field image...")

cr = pycrates.read_file(os.path.join(WORK, "img_0.5-7keV.fits"))
img = pycrates.copy_piximgvals(cr)

fig, ax = plt.subplots(figsize=(8, 8))
# Log scale, similar to DS9 heat colormap
im = ax.imshow(img, origin='lower', cmap='afmhot',
               norm=matplotlib.colors.LogNorm(vmin=0.5, vmax=img.max()),
               interpolation='gaussian')

# Mark pulsar with crosshair
ax.plot(PSR_X, PSR_Y, '+', color='cyan', markersize=20, markeredgewidth=2)
ax.annotate('PSR J1826-1256', (PSR_X + 15, PSR_Y + 15),
            color='cyan', fontsize=11, fontweight='bold')

# Mark source and background regions
# Source: 2" circle ~ 4 pixels (0.492"/pixel)
src_r = 2.0 / 0.492
bkg_inner = 5.0 / 0.492
bkg_outer = 20.0 / 0.492

circle_src = plt.Circle((PSR_X, PSR_Y), src_r, color='lime',
                          fill=False, linewidth=1.5, linestyle='-')
circle_bkg_in = plt.Circle((PSR_X, PSR_Y), bkg_inner, color='yellow',
                             fill=False, linewidth=1, linestyle='--')
circle_bkg_out = plt.Circle((PSR_X, PSR_Y), bkg_outer, color='yellow',
                              fill=False, linewidth=1, linestyle='--')
ax.add_patch(circle_src)
ax.add_patch(circle_bkg_in)
ax.add_patch(circle_bkg_out)

# Zoom into pulsar region (100x100 pixel area around it)
margin = 80
ax.set_xlim(PSR_X - margin, PSR_X + margin)
ax.set_ylim(PSR_Y - margin, PSR_Y + margin)

ax.set_xlabel('X (pixels)', fontsize=12)
ax.set_ylabel('Y (pixels)', fontsize=12)
ax.set_title('Chandra ObsID 7641 — PSR J1826-1256 (0.5-7 keV)', fontsize=13)
plt.colorbar(im, ax=ax, label='Counts', shrink=0.8)
plt.tight_layout()

outpath1 = os.path.join(ROOT, 'xray_field_image.png')
plt.savefig(outpath1, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {outpath1}")


# ========== PLOT 2: Radial Brightness Profile ==========
print("Creating radial profile...")

# Calculate radial distances from pulsar for every pixel
ny, nx = img.shape
yy, xx = np.mgrid[0:ny, 0:nx]
r = np.sqrt((xx - PSR_X)**2 + (yy - PSR_Y)**2)

# Bin into radial annuli (1 pixel wide, up to 50 pixels ~ 25")
max_r = 50
bins = np.arange(0, max_r + 1, 1)
bin_centers = (bins[:-1] + bins[1:]) / 2.0
radial_sum = np.zeros(len(bins) - 1)
radial_area = np.zeros(len(bins) - 1)

for i in range(len(bins) - 1):
    mask = (r >= bins[i]) & (r < bins[i + 1])
    radial_sum[i] = np.sum(img[mask])
    radial_area[i] = np.sum(mask)

# Surface brightness = counts / area (counts per pixel)
sb = radial_sum / np.where(radial_area > 0, radial_area, 1)
# Error bars (Poisson)
sb_err = np.sqrt(radial_sum) / np.where(radial_area > 0, radial_area, 1)

# Normalize to peak
peak = sb.max()
sb_norm = sb / peak
sb_err_norm = sb_err / peak

# Convert pixel to arcsec (0.492"/pixel)
r_arcsec = bin_centers * 0.492

fig, ax = plt.subplots(figsize=(8, 5))
ax.errorbar(r_arcsec, sb_norm, yerr=sb_err_norm,
            fmt='ko-', markersize=4, capsize=2, linewidth=1,
            label='Observed profile')

# Mark source and background regions
ax.axvline(x=2.0, color='green', linestyle='--', linewidth=1.5, label='Source region (2")')
ax.axvline(x=5.0, color='orange', linestyle='--', linewidth=1, label='Bkg inner (5")')
ax.axvline(x=20.0, color='orange', linestyle=':', linewidth=1, label='Bkg outer (20")')

ax.set_xlabel('Radial Distance (arcsec)', fontsize=12)
ax.set_ylabel('Normalized Surface Brightness', fontsize=12)
ax.set_title('Radial Profile of PSR J1826-1256', fontsize=13)
ax.legend(fontsize=9)
ax.set_xlim(0, 25)
ax.set_ylim(-0.05, 1.1)
ax.grid(True, alpha=0.3)
plt.tight_layout()

outpath2 = os.path.join(ROOT, 'radial_profile.png')
plt.savefig(outpath2, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {outpath2}")

# ========== PLOT 3: Wide Field Image ==========
print("Creating wide field image...")

fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(img, origin='lower', cmap='afmhot',
               norm=matplotlib.colors.LogNorm(vmin=0.5, vmax=img.max()),
               interpolation='gaussian')

ax.plot(PSR_X, PSR_Y, '+', color='cyan', markersize=15, markeredgewidth=2)
ax.annotate('PSR J1826-1256', (PSR_X + 20, PSR_Y + 20),
            color='cyan', fontsize=10, fontweight='bold')

ax.set_xlabel('X (pixels)', fontsize=12)
ax.set_ylabel('Y (pixels)', fontsize=12)
ax.set_title('Chandra ACIS-S ObsID 7641 — Full Field (0.5-7 keV)', fontsize=13)
plt.colorbar(im, ax=ax, label='Counts', shrink=0.8)
plt.tight_layout()

outpath3 = os.path.join(ROOT, 'xray_full_field.png')
plt.savefig(outpath3, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {outpath3}")

print("All plots done!")


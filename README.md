# Project 12 – X-ray Spectral Analysis of PSR J1826−1256

Ref: Karpova et al. (2019), MNRAS 487, 1964

## Setup

I'm using CIAO 4.18 and DS9 on macOS. Anaconda conflicts with CIAO so I have to deactivate it first every time.

```bash
conda deactivate
source /Applications/ciao-4.18/bin/ciao.sh
```

**Verify:** `ciaover` should print `CIAO 4.18.0` and `CALDB 4.12.3`.

```bash
cd /Volumes/DATA/baba_dev/AarushProj/space3
```

## A. Chandra Data Reduction

### 1. Getting the data ready

Downloaded ObsID 7641 from the Chandra archive. The evt2 file is already Level-2 processed so I used it directly instead of running chandra_repro.

```bash
mkdir -p work/7641
cp data/chandra/7641/acisf07641N003_evt2.fits.gz work/7641/
cp data/chandra/7641/acisf07641_000N003_bpix1.fits.gz work/7641/
cp data/chandra/7641/acisf07641_000N003_flt1.fits.gz work/7641/
cp data/chandra/7641/acisf07641_000N003_fov1.fits.gz work/7641/
gunzip -kf work/7641/*.gz
```

**Verify:** `ls work/7641/*.fits` should show 4 files (evt2, bpix1, flt1, fov1).

I also needed the aspect solution and mask files for spectrum extraction, which weren't in the original download:

```bash
download_chandra_obsid 7641 asol
```

**Verify:** Wait for it to finish (~2 min). Then check: `ls 7641/primary/*asol*` should show `pcadf07641_000N001_asol1.fits.gz`.

```bash
cp 7641/primary/pcadf07641_000N001_asol1.fits.gz work/7641/
gunzip -kf work/7641/pcadf07641_000N001_asol1.fits.gz
```

**Verify:** `ls -lh work/7641/pcadf07641_000N001_asol1.fits` should show ~35 MB.

```bash
download_chandra_obsid 7641 msk,pbk
```

**Verify:** Wait for download. Then check: `ls 7641/secondary/*msk* 7641/secondary/*pbk*` should show 2 files.

```bash
cp 7641/secondary/acisf07641_000N003_msk1.fits.gz work/7641/
cp 7641/secondary/acisf301853852N003_pbk0.fits.gz work/7641/
gunzip -kf work/7641/acisf07641_000N003_msk1.fits.gz
gunzip -kf work/7641/acisf301853852N003_pbk0.fits.gz
```

**Verify:** `ls work/7641/*.fits | wc -l` should show 7 files total (evt2, asol, bpix, flt, fov, msk, pbk).

Check the event file has data:

```bash
dmlist "work/7641/acisf07641N003_evt2.fits" counts
```

**Verify:** Should say 527,014 — that's how many X-ray photons were detected.

### 2. Making the X-ray image

Filtered to 0.5–7 keV to remove noise and binned into an image:

```bash
dmcopy "work/7641/acisf07641N003_evt2.fits[energy=500:7000]" work/7641/evt2_0.5-7keV.fits clobber=yes
```

**Verify:** `dmlist "work/7641/evt2_0.5-7keV.fits" counts` should say ~183,984 (about 35% of original).

```bash
dmcopy "work/7641/evt2_0.5-7keV.fits[bin x=3500:4500:1,y=3600:4600:1]" work/7641/img_0.5-7keV.fits clobber=yes
```

**Verify:** `dmlist "work/7641/img_0.5-7keV.fits" cols` should show a 1000×1000 image (`Int2(1000x1000)`).

Opened in DS9 to see it:

```bash
/Applications/SAOImageDS9.app/Contents/MacOS/ds9 work/7641/img_0.5-7keV.fits -scale log -cmap heat -zoom to fit &
```

**Verify:** DS9 opens with a heat-colored image. You should see several bright point sources. If it looks all black, make sure Scale is set to Log.

### 3. Finding PSR J1826−1256

The pulsar is at RA = 18:26:08.5, Dec = −12:56:34.

Ran wavdetect to find all sources automatically:

```bash
mkpsfmap work/7641/img_0.5-7keV.fits work/7641/psfmap.fits energy=1.5 ecf=0.393 clobber=yes
```

**Verify:** `ls -lh work/7641/psfmap.fits` should exist (~4 MB).

```bash
wavdetect infile=work/7641/img_0.5-7keV.fits outfile=work/7641/src_list.fits scellfile=work/7641/scell.fits imagefile=work/7641/imgfile.fits defnbkgfile=work/7641/nbkg.fits psffile=work/7641/psfmap.fits scales="1 2 4 8 16" clobber=yes
```

**Verify:** `dmlist "work/7641/src_list.fits" counts` should show ~68 sources detected.

List the sources:

```bash
dmlist "work/7641/src_list.fits[cols ra,dec,net_counts]" data
```

**Verify:** Look for source #5 — it should have RA~276.5356, Dec~−12.9429, net_counts~244. That's the pulsar. It matches the known coordinates (276.5354, −12.9428) within 0.0002°.

To confirm in DS9, type `18:26:08.5 -12:56:34` in the coordinate box — the crosshair should land right on a bright source.

### 4. Source and background regions

Following the paper I used a 2″ circle for the source and a 5″–20″ annulus for background:

```bash
echo 'circle(18:26:08.5,-12:56:34,2")' > work/7641/src.reg
echo 'annulus(18:26:08.5,-12:56:34,5",20")' > work/7641/bkg.reg
```

**Verify:** `cat work/7641/src.reg` should print `circle(18:26:08.5,-12:56:34,2")`.
`cat work/7641/bkg.reg` should print `annulus(18:26:08.5,-12:56:34,5",20")`.

Checked them in DS9:

```bash
/Applications/SAOImageDS9.app/Contents/MacOS/ds9 work/7641/img_0.5-7keV.fits -scale log -cmap heat -region work/7641/src.reg -region work/7641/bkg.reg -pan to 18:26:08.5 -12:56:34 wcs -zoom 8 &
```

**Verify:** You should see a small green circle (source) sitting on the bright pulsar, surrounded by a larger green ring (background). The pulsar should be clearly inside the circle. No other bright sources should be inside the background ring.

### 5. Extracting the spectrum

```bash
specextract \
  infile="work/7641/acisf07641N003_evt2.fits[sky=region(work/7641/src.reg)]" \
  outroot=work/7641/pulsar_spec \
  bkgfile="work/7641/acisf07641N003_evt2.fits[sky=region(work/7641/bkg.reg)]" \
  asp=work/7641/pcadf07641_000N001_asol1.fits \
  mskfile=work/7641/acisf07641_000N003_msk1.fits \
  grouptype=NUM_CTS binspec=1 weight=no clobber=yes
```

Takes about 3 minutes. Lots of output is normal.

**Verify:** `ls work/7641/pulsar_spec*` should show 7 files:
- `pulsar_spec.pi` — source spectrum
- `pulsar_spec_bkg.pi` — background spectrum
- `pulsar_spec.arf` — effective area (~39 KB)
- `pulsar_spec.rmf` — energy response (~2 MB)
- `pulsar_spec_grp.pi` — grouped spectrum
- `pulsar_spec_bkg.arf` and `pulsar_spec_bkg.rmf`

To view the spectrum in DS9: open DS9 → File → Open Other → Open PHA → select `pulsar_spec_grp.pi`. A plot window should appear showing counts vs energy.

## B. Spectral Analysis

Used Sherpa (built into CIAO) to fit the spectrum. The fitting script is in `work/7641/fit_final.py`.

```bash
python work/7641/fit_final.py
```

**Verify:** Script should print fit results without errors. Check that W-stat/dof is close to 1.0 (good fit = reduced statistic near 1).

### Power law fit (tbabs × powerlaw)

| Parameter | My result | Paper |
|-----------|-----------|-------|
| N_H | 0.83 × 10²² cm⁻² | 0.50 ± 0.15 |
| Γ | 0.39 | 1.25 ± 0.20 |
| Absorbed flux | 5.95 × 10⁻¹⁴ erg/cm²/s | ~3 × 10⁻¹⁴ |
| W-stat/dof | 420.7/443 = 0.95 | — |

### Blackbody fit (tbabs × bbodyrad)

| Parameter | My result |
|-----------|-----------|
| N_H | 0.32 × 10²² cm⁻² |
| kT | 2.05 keV |
| W-stat/dof | 423.1/443 = 0.96 |

**Verify:** Power law W-stat (420.7) should be lower than blackbody W-stat (423.1), confirming power law is the better model.

### Why my results differ from the paper

- I didn't reprocess with chandra_repro (used archive evt2 directly)
- Different CALDB version (mine is 4.12.3, theirs was older)
- Region sizes might be slightly different
- They combined Chandra + XMM data, I only used Chandra
- With only ~244 counts there's a strong N_H–Γ degeneracy

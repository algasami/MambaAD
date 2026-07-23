from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_LOG_MEL


# Scorer ablation: 'cos-residual' (the native MambaAD readout) — the explicit baseline for the
# scorer/ front. Per-pixel 1-cos(ft,fs) summed over taps, pooled sp_max/sp_mean. Identical to
# the historical default (ABL_SCORER=None); included so every readout is one config to run.
# Input = log-Mel, e50 schedule. See mimii/_base.py + util/scorer.py.
class cfg(cfg_mimii_base):

	INPUT_ROOT = DATA_ROOT_LOG_MEL
	ABL_SCORER = dict(type='CosResidualScorer', amap_mode='add', gaussian_sigma=4, uni_am=False)

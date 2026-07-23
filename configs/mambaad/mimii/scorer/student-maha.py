from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_LOG_MEL


# Scorer ablation: 'student-maha'. Re-scores the DECODER's reconstructed features with a
# per-class Mahalanobis distance on GAP-concat features (the winning readout in the
# student-feature probe), instead of the cosine-residual sp_max/sp_mean.
# Fits a per-class bank on the normal train split each eval; run single-GPU.
# Input = log-Mel, e50 schedule. See mimii/_base.py + util/scorer.py.
class cfg(cfg_mimii_base):

	INPUT_ROOT = DATA_ROOT_LOG_MEL
	ABL_SCORER = dict(type='MahaScorer', source='student')

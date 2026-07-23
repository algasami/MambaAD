from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_LOG_MEL


# Scorer ablation: 'student-knn'. Re-scores the DECODER's reconstructed features with mean
# cosine distance to the k=5 nearest normal train clips on GAP-concat features (DN2/SPADE-image),
# instead of the cosine-residual sp_max/sp_mean.
# Fits a per-class bank on the normal train split each eval; run single-GPU.
# Input = log-Mel, e50 schedule. See mimii/_base.py + util/scorer.py.
class cfg(cfg_mimii_base):

	INPUT_ROOT = DATA_ROOT_LOG_MEL
	ABL_SCORER = dict(type='KNNScorer', source='student', k=5)

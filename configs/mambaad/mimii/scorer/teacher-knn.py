from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_LOG_MEL


# Scorer ablation: 'teacher-knn'. Scores the FROZEN ResNet34 teacher features with mean cosine
# distance to the k=5 nearest normal train clips on GAP-concat features (SPADE-image). Like
# teacher-maha, a decoder-free ceiling reference; the bank is fitted once (frozen teacher).
# Input = log-Mel, e50 schedule. See mimii/_base.py + util/scorer.py.
class cfg(cfg_mimii_base):

	INPUT_ROOT = DATA_ROOT_LOG_MEL
	ABL_SCORER = dict(type='KNNScorer', source='teacher', k=5)

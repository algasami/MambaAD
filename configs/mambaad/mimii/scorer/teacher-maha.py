from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_LOG_MEL


# Scorer ablation: 'teacher-maha'. Scores the FROZEN ResNet34 teacher features with a per-class
# Mahalanobis distance on GAP-concat features (PaDiM-image). This is the decoder-free ceiling
# reference — it ignores the student entirely, so the bank is fitted once (frozen teacher).
# Use to check how much (if any) the trained decoder adds over the raw encoder.
# Input = log-Mel, e50 schedule. See mimii/_base.py + util/scorer.py.
class cfg(cfg_mimii_base):

	INPUT_ROOT = DATA_ROOT_LOG_MEL
	ABL_SCORER = dict(type='MahaScorer', source='teacher')

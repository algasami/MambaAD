from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_LOG_MEL


# Scan-type x scorer ablation: scan_type='hilbert', re-scored with the student-maha readout.
# Input = log-Mel, e50 schedule. Same architecture as scan-type/hilbert.py (matching scan_type
# so the trained checkpoint loads and forwards under the right scan order), but the test-time
# score is the per-class Mahalanobis distance on the DECODER's GAP features (the winning readout
# in the scorer/ front) instead of the native cosine-residual sp_max/sp_mean.
# Used by docs/reeval_sp_mean.py to re-score a scan-type/hilbert.py training run.
# Fits a per-class bank on the normal train split each eval; run single-GPU.
# See mimii/_base.py + util/scorer.py + docs/run_scan_ablation.sh.
class cfg(cfg_mimii_base):

	INPUT_ROOT = DATA_ROOT_LOG_MEL
	SCAN_TYPE = 'hilbert'
	SCAN_NDIR = 8
	ABL_SCORER = dict(type='MahaScorer', source='student')

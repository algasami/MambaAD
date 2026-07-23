from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_LOG_MEL


# Scan-type ablation: 'zigzag'. Input = log-Mel, e50 schedule.
# Anti-diagonal traversal, JPEG-style.
# Baseline is scan_type='hilbert', num_direction=8. See mimii/_base.py.
class cfg(cfg_mimii_base):

	INPUT_ROOT = DATA_ROOT_LOG_MEL
	SCAN_TYPE = 'zigzag'
	SCAN_NDIR = 8

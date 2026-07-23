from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_LOG_MEL


# Scan-type ablation: 'zorder'. Input = log-Mel, e50 schedule.
# Z-order / Morton curve (locality-preserving like Hilbert, but with periodic long jumps).
# Baseline is scan_type='hilbert', num_direction=8. See mimii/_base.py.
class cfg(cfg_mimii_base):

	INPUT_ROOT = DATA_ROOT_LOG_MEL
	SCAN_TYPE = 'zorder'
	SCAN_NDIR = 8

from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_LOG_MEL


# Scan-type ablation: 'hilbert'. Input = log-Mel, e50 schedule.
# Hilbert space-filling curve (locality-preserving). The baseline (== e50/log-Mel); listed here so the scan sweep is self-contained.
# Baseline is scan_type='hilbert', num_direction=8. See mimii/_base.py.
class cfg(cfg_mimii_base):

	INPUT_ROOT = DATA_ROOT_LOG_MEL
	SCAN_TYPE = 'hilbert'
	SCAN_NDIR = 8

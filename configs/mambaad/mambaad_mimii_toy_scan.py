from MambaAD.configs.mambaad.mambaad_mimii_toy import cfg as cfg_mimii_toy


# Scan ablation: 'scan' (serpentine/boustrophedon order — alternate rows reversed).
# Baseline is mambaad_mimii_toy.py (scan_type='hilbert', num_direction=8).
class cfg(cfg_mimii_toy):

	def __init__(self):
		cfg_mimii_toy.__init__(self)
		# self.model_s is the same dict object held by self.model.kwargs['model_s'],
		# so in-place mutation reaches the model factory.
		self.model_s['scan_type'] = 'scan'
		self.model_s['num_direction'] = 8

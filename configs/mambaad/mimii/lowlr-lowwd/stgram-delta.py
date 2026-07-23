from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_STGRAM_DELTA


# lowlr-lowwd x stgram-delta (Sgram, frozen Tgram, delta).
# Low lr / low wd probe (lr 1e-3 / wd 1e-4, 200 ep). Verdict: stable but underfit -- lowering wd 100x is the wrong lever for divergence.
# See mimii/_base.py for the shared config body.
class cfg(cfg_mimii_base):

	ABL_EPOCH = 200
	ABL_LR_BASE = 1e-3
	ABL_WD = 1e-4
	INPUT_ROOT = DATA_ROOT_STGRAM_DELTA

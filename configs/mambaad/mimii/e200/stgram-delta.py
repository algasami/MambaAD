from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_STGRAM_DELTA


# e200 x stgram-delta (Sgram, frozen Tgram, delta).
# 200-epoch schedule (lr 5e-3 / wd 0.01). Never diverges at 200 ep; best trained config so far with best-epoch selection.
# See mimii/_base.py for the shared config body.
class cfg(cfg_mimii_base):

	ABL_EPOCH = 200
	INPUT_ROOT = DATA_ROOT_STGRAM_DELTA

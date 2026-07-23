from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_STGRAM, METRICS_SP_MAX


# e1000 x stgram (Sgram, frozen Tgram, Sgram).
# Long 1000-epoch schedule (lr 5e-3 / wd 0.01, step decay @ ep800). Historical: student weights grow until overflow -> NaN before decay kicks in; recorded sp_max only (21-col). Kept for reproduction.
# See mimii/_base.py for the shared config body.
class cfg(cfg_mimii_base):

	ABL_EPOCH = 1000
	ABL_METRICS = METRICS_SP_MAX
	INPUT_ROOT = DATA_ROOT_STGRAM

from MambaAD.configs.mambaad.mimii._base import cfg_mimii_base, DATA_ROOT_STGRAM


# e50 x stgram (Sgram, frozen Tgram, Sgram).
# Super-short 50-epoch schedule (lr 5e-3 / wd 0.01). Current default; AUROC peaks ~ep10-20 then declines (no best-ckpt selection).
# See mimii/_base.py for the shared config body.
class cfg(cfg_mimii_base):

	ABL_EPOCH = 50
	INPUT_ROOT = DATA_ROOT_STGRAM

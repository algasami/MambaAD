from argparse import Namespace
from timm.data.constants import IMAGENET_DEFAULT_MEAN
from timm.data.constants import IMAGENET_DEFAULT_STD
import torchvision.transforms.functional as F

from configs.__base__ import *


# =============================================================================
# Shared MambaAD-on-MIMII config base.
#
# Directory layout (this package):
#   mimii/<ablation-type>/<input-type>.py
#     ablation-type : e50 | e200 | e1000 | lowlr-lowwd | scan-type
#     input-type    : log-Mel | stgram | stgram-delta   (scan-type is by scan)
#
# Every leaf is a thin subclass of `cfg_mimii_base` that only flips the
# ablation knobs (ABL_*) and/or the input representation (INPUT_ROOT). All the
# heavy lifting (transforms, model, optimiser, trainer, loss, logging) lives
# here so the matrix stays in sync. See CLAUDE.md / NOTE.md for the rationale
# behind each ablation.
# =============================================================================

# --- metric presets ----------------------------------------------------------
# 42-column metric.txt: both sp_max (per-pixel max) and sp_mean (mean) pooling
# families. This is the current standard for all MIMII runs.
METRICS_SP_MEAN = [
	'mAUROC_sp_max', 'mAP_sp_max', 'mF1_max_sp_max',
	'mAUROC_sp_mean', 'AP_sp_mean', 'F1_max_sp_mean',
]
# 21-column metric.txt: sp_max only. What the original long-schedule (e1000)
# runs recorded before mean metrics were added; kept for faithful reproduction.
METRICS_SP_MAX = [
	'mAUROC_sp_max', 'mAP_sp_max', 'mF1_max_sp_max',
]

# --- input representations (spectrogram dataset roots) ------------------------
DATA_ROOT_LOG_MEL      = 'data/dcase-2020-spectrogram'       # (log-Mel, delta, delta-delta)
DATA_ROOT_STGRAM       = 'data/dcase-2020-stgram'            # (Sgram, frozen Tgram, Sgram)
DATA_ROOT_STGRAM_DELTA = 'data/dcase-2020-stgram-delta'      # (Sgram, frozen Tgram, delta)


class cfg_mimii_base(cfg_common, cfg_dataset_default, cfg_model_mambaad):

	# ---- ablation knobs: schedule / optimiser (override per ablation folder) ----
	ABL_EPOCH = 50            # epoch_full
	ABL_LR_BASE = 0.005       # base lr, scaled by batch/16
	ABL_WD = 0.01             # weight decay (0.01 tamps down divergence w/ AdamW)
	ABL_METRICS = METRICS_SP_MEAN

	# ---- input representation (override per input-type leaf) ----
	INPUT_ROOT = DATA_ROOT_LOG_MEL

	# ---- scan ablation (override in scan-type leaves) ----
	SCAN_TYPE = 'hilbert'
	SCAN_NDIR = 8

	def __init__(self):
		# super(cfg, self).__init__()
		cfg_common.__init__(self)
		cfg_dataset_default.__init__(self)
		cfg_model_mambaad.__init__(self)

		self.fvcore_b = 1
		self.fvcore_c = 3
		self.seed = 42
		self.size = 256
		self.epoch_full = self.ABL_EPOCH
		self.warmup_epochs = 0
		self.test_start_epoch = self.epoch_full
		self.test_per_epoch = self.epoch_full // 20
		self.batch_train = 16
		self.batch_test_per = 16
		self.lr = self.ABL_LR_BASE * self.batch_train / 16
		self.weight_decay = self.ABL_WD
		self.metrics = self.ABL_METRICS

		# ==> data
		self.data.type = 'DefaultAD'
		self.data.root = self.INPUT_ROOT
		self.data.meta = 'meta.json'
		self.data.cls_names = []

		self.data.train_transforms = [
			dict(type='Resize', size=(self.size, self.size), interpolation=F.InterpolationMode.BILINEAR),
			dict(type='CenterCrop', size=(self.size, self.size)),
			dict(type='ToTensor'),
			dict(type='Normalize', mean=IMAGENET_DEFAULT_MEAN, std=IMAGENET_DEFAULT_STD, inplace=True),
		]
		self.data.test_transforms = self.data.train_transforms
		self.data.target_transforms = [
			dict(type='Resize', size=(self.size, self.size), interpolation=F.InterpolationMode.BILINEAR),
			dict(type='CenterCrop', size=(self.size, self.size)),
			dict(type='ToTensor'),
		]

		# ==> modal
		self.model_t = Namespace()
		self.model_t.name = 'timm_resnet34'
		self.model_t.kwargs = dict(pretrained=False, checkpoint_path='model/pretrain/resnet34-43635321.pth',
								   strict=False, features_only=True, out_indices=[1, 2, 3])
		self.model_s = dict(
			depths_decoder=[3, 4, 6, 3],
			scan_type=self.SCAN_TYPE,
			num_direction=self.SCAN_NDIR,
		)
		self.model = Namespace()
		self.model.name = 'mambaad'
		self.model.kwargs = dict(pretrained=False, checkpoint_path='', strict=True, model_t=self.model_t,
								 model_s=self.model_s)

		# ==> evaluator
		self.evaluator.kwargs = dict(metrics=self.metrics, pooling_ks=None, max_step_aupro=100)
		# self.evaluator.kwargs = dict(metrics=self.metrics, pooling_ks=[16, 16], max_step_aupro=100)

		# ==> optimizer
		self.optim.lr = self.lr
		self.optim.kwargs = dict(name='adamw', betas=(0.9, 0.999), eps=1e-8, weight_decay=self.weight_decay, amsgrad=False)

		# ==> trainer
		self.trainer.name = 'MAMBAADTrainer'
		self.trainer.logdir_sub = ''
		self.trainer.resume_dir = ''
		self.trainer.epoch_full = self.epoch_full
		self.trainer.scheduler_kwargs = dict(
			name='step', lr_noise=None, noise_pct=0.67, noise_std=1.0, noise_seed=42, lr_min=self.lr / 1e2,
			warmup_lr=self.lr / 1e3, warmup_iters=-1, cooldown_iters=0, warmup_epochs=self.warmup_epochs, cooldown_epochs=0, use_iters=True,
			patience_iters=0, patience_epochs=0, decay_iters=0, decay_epochs=int(self.epoch_full * 0.8), cycle_decay=0.1, decay_rate=0.1)
		self.trainer.mixup_kwargs = dict(mixup_alpha=0.8, cutmix_alpha=1.0, cutmix_minmax=None, prob=0.0, switch_prob=0.5, mode='batch', correct_lam=True, label_smoothing=0.1)
		self.trainer.test_start_epoch = self.test_start_epoch
		self.trainer.test_per_epoch = self.test_per_epoch

		self.trainer.data.batch_size = self.batch_train
		self.trainer.data.batch_size_per_gpu_test = self.batch_test_per

		self.trainer.find_unused_parameters = True

		# ==> loss
		self.loss.loss_terms = [
			dict(type='CosLoss', name='cos', avg=False, lam=1.0),
		]

		# ==> logging
		self.logging.log_terms_train = [
			dict(name='batch_t', fmt=':>5.3f', add_name='avg'),
			dict(name='data_t', fmt=':>5.3f'),
			dict(name='optim_t', fmt=':>5.3f'),
			dict(name='lr', fmt=':>7.6f'),
			dict(name='cos', suffixes=[''], fmt=':>5.3f', add_name='avg'),
		]
		self.logging.log_terms_test = [
			dict(name='batch_t', fmt=':>5.3f', add_name='avg'),
			dict(name='cos', suffixes=[''], fmt=':>5.3f', add_name='avg'),
		]

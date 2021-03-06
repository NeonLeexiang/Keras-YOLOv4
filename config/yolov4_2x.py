#! /usr/bin/env python
# coding=utf-8
# ================================================================
#
#   Author      : miemie2013
#   Created date: 2020-10-30 21:08:11
#   Description : keras_ppyolo
#
# ================================================================



class YOLOv4_2x_Config(object):
    def __init__(self):
        # 自定义数据集
        self.train_path = 'annotation_json/voc2012_train.json'
        self.val_path = 'annotation_json/voc2012_val.json'
        self.classes_path = 'data/voc_classes.txt'
        self.train_pre_path = 'JPEGImages/'   # 训练集图片相对路径
        self.val_pre_path = 'JPEGImages/'     # 验证集图片相对路径
        self.num_classes = 8                                      # 数据集类别数

        # COCO数据集
        # self.train_path = '../COCO/annotations/instances_train2017.json'
        # self.val_path = '../COCO/annotations/instances_val2017.json'
        # self.classes_path = 'data/coco_classes.txt'
        # self.train_pre_path = '../COCO/train2017/'  # 训练集图片相对路径
        # self.val_pre_path = '../COCO/val2017/'      # 验证集图片相对路径
        # self.num_classes = 80                       # 数据集类别数


        # ========= 一些设置 =========
        self.train_cfg = dict(
            lr=0.0001,      # 0.0001
            batch_size=8,
            num_threads=5,   # 读数据的线程数
            max_batch=3,     # 最大读多少个批
            model_path='yolov4_2x.h5',
            # model_path='./weights/step00020000.h5',
            save_iter=10,   # 每隔几步保存一次模型 1000
            eval_iter=50,   # 每隔几步计算一次eval集的mAP 5000
            max_iters=5000,   # 训练多少步 500000
        )


        # 验证。用于train.py、eval.py、test_dev.py
        self.eval_cfg = dict(
            model_path='yolov4_2x.h5',
            # model_path='./weights/step00005000.h5',
            target_size=320,     # 608
            draw_image=False,    # 是否画出验证集图片
            draw_thresh=0.15,    # 如果draw_image==True，那么只画出分数超过draw_thresh的物体的预测框。
            eval_batch_size=4,   # 验证时的批大小。
        )

        # 测试。用于demo.py
        self.test_cfg = dict(
            model_path='yolov4_2x.h5',
            # model_path='./weights/step00020000.h5',
            target_size=320,    # 608
            # target_size=320,
            draw_image=True,
            draw_thresh=0.15,   # 如果draw_image==True，那么只画出分数超过draw_thresh的物体的预测框。
        )


        # ============= 模型相关 =============
        # self.use_ema = True
        self.use_ema = False
        self.ema_decay = 0.9998
        self.backbone_type = 'CSPDarknet53'
        self.backbone = dict(
            norm_type='bn',
            feature_maps=[3, 4, 5],
            freeze_at=5,
        )
        self.head_type = 'YOLOv4Head'
        self.head = dict(
            num_classes=self.num_classes,
            norm_type='bn',
            anchor_masks=[[6, 7, 8], [3, 4, 5], [0, 1, 2]],
            anchors=[[12, 16], [19, 36], [40, 28],
                     [36, 75], [76, 55], [72, 146],
                     [142, 110], [192, 243], [459, 401]],
            coord_conv=True,
            iou_aware=False,
            iou_aware_factor=0.4,
            scale_x_y=1.05,
            spp=True,
            drop_block=True,
            keep_prob=0.9,
            downsample=[32, 16, 8],
            in_channels=[1024, 1024, 512],
        )
        self.iou_loss_type = 'IouLoss'
        self.iou_loss = dict(
            loss_weight=2.5,
            max_height=320,     # 608
            max_width=320,      # 608
            ciou_term=True,
        )
        self.iou_aware_loss_type = 'IouAwareLoss'
        self.iou_aware_loss = dict(
            loss_weight=1.0,
            max_height=320,     # 608
            max_width=320,      # 608
        )
        self.yolo_loss_type = 'YOLOv3Loss'
        self.yolo_loss = dict(
            ignore_thresh=0.7,
            scale_x_y=1.05,
            label_smooth=False,
            use_fine_grained_loss=True,
        )
        self.nms_cfg = dict(
            nms_type='matrix_nms',
            score_threshold=0.01,
            post_threshold=0.01,
            nms_top_k=500,
            keep_top_k=100,
            use_gaussian=False,
            gaussian_sigma=2.,
        )
        # self.nms_cfg = dict(
        #     nms_type='fast_nms',
        #     score_threshold=0.01,
        #     nms_threshold=0.45,
        #     nms_top_k=500,
        #     keep_top_k=100,
        # )


        # ============= 预处理相关 =============
        self.context = {'fields': ['image', 'gt_bbox', 'gt_class', 'gt_score']}
        # DecodeImage
        self.decodeImage = dict(
            to_rgb=True,
            with_mixup=True,
        )
        # MixupImage
        self.mixupImage = dict(
            alpha=1.5,
            beta=1.5,
        )
        # ColorDistort
        self.colorDistort = dict()
        # RandomExpand
        self.randomExpand = dict(
            fill_value=[123.675, 116.28, 103.53],
        )
        # RandomCrop
        self.randomCrop = dict()
        # RandomFlipImage
        self.randomFlipImage = dict(
            is_normalized=False,
        )
        # NormalizeBox
        self.normalizeBox = dict()
        # PadBox
        self.padBox = dict(
            num_max_boxes=50,
        )
        # BboxXYXY2XYWH
        self.bboxXYXY2XYWH = dict()
        # RandomShape
        self.randomShape = dict(
            sizes=[320, 352, 384, 416, 448, 480, 512, 544, 576, 608],
            random_inter=True,
        )
        # NormalizeImage
        self.normalizeImage = dict(
            mean=[0., 0., 0.],
            std=[1., 1., 1.],
            is_scale=True,
            is_channel_first=False,
        )
        # Permute
        self.permute = dict(
            to_bgr=False,
            channel_first=True,
        )
        # Gt2YoloTarget
        self.gt2YoloTarget = dict(
            anchor_masks=[[6, 7, 8], [3, 4, 5], [0, 1, 2]],
            anchors=[[12, 16], [19, 36], [40, 28],
                     [36, 75], [76, 55], [72, 146],
                     [142, 110], [192, 243], [459, 401]],
            downsample_ratios=[32, 16, 8],
            num_classes=self.num_classes,
        )
        # ResizeImage
        self.resizeImage = dict(
            target_size=608,
            interp=2,
        )



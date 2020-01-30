#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/init.h>
#include <linux/sched.h>
#include <linux/kernel.h>
#include <linux/slab.h>        
#include <linux/fs.h>
#include <linux/hdreg.h>
#include <linux/genhd.h>
#include <linux/blkdev.h>
#include <linux/bio.h>
#include <linux/version.h>
#include <linux/vmalloc.h>

static int vblkdev_major;
module_param(vblkdev_major, int, 0);

#define HARDSECT_SIZE 512  /* 扇区大小 */
#define NSECTORS 1024  /* 扇区数量 */
#define NDEVICES 4

enum {
	VMEMD_QUEUE  = 0, /* request_queue */
	VMEMD_NOQUEUE = 1, /* make_request */
};
static int request_mode = VMEMD_QUEUE;
module_param(request_mode, int, 0);


#define VBLKDEV_MINORS    16
#define KERNEL_SECTOR_SIZE  512

struct vblkdev {
	int size;                       /* 设备空间大小 */
	u8 *data;                       /* 数据数组 */
	spinlock_t lock;                /* 自旋锁 */
	struct request_queue *queue;    /* 请求队列 */
	struct gendisk *gd;             /* gendisk结构体 */
};

static struct vblkdev *devices;

/* 进行数据传送 */
static void vblkdev_transfer(struct vblkdev *dev, unsigned long sector,
		unsigned long nsect, char *buffer, int write)
{
	unsigned long offset = sector*KERNEL_SECTOR_SIZE;
	unsigned long nbytes = nsect*KERNEL_SECTOR_SIZE;

	if ((offset + nbytes) > dev->size) {
		printk (KERN_NOTICE "Beyond-end write (%ld %ld)\n", offset, nbytes);
		return;
	}
	if (write)
		memcpy(dev->data + offset, buffer, nbytes);
	else
		memcpy(buffer, dev->data + offset, nbytes);
}

/* 传送一个bio结构体 */
static int vblkdev_xfer_bio(struct vblkdev *dev, struct bio *bio)
{
    /* 新版本内核改动较大 */
    struct bio_vec bvec;
    struct bvec_iter iter;
    sector_t sector = bio->bi_iter.bi_sector;

	bio_for_each_segment(bvec, bio, iter) {
		char *buffer = __bio_kmap_atomic(bio, iter); /* 获取映射的内存 */
		/* 传送数据 */
        vblkdev_transfer(dev, sector, bio_cur_bytes(bio) >> 9,
			buffer, bio_data_dir(bio) == WRITE);
		sector += bio_cur_bytes(bio) >> 9;
		__bio_kunmap_atomic(buffer);
	}
	return 0;
}

/* 用于请求队列 */
static void vblkdev_request(struct request_queue *q)
{
	struct request *req;
	struct bio *bio;
    /* 忽略非读写命令 */
	while ((req = blk_peek_request(q)) != NULL) {
		struct vblkdev *dev = req->rq_disk->private_data;
		
        if (req->cmd_type != REQ_TYPE_FS) {
			printk (KERN_NOTICE "Skip non-fs request\n");

            /* blk_peek_request 不能使请求出队，需要调用blk_start_request手动出队 */
			blk_start_request(req);
			__blk_end_request_all(req, -EIO);
			continue;
		}

		blk_start_request(req);
		__rq_for_each_bio(bio, req)
			vblkdev_xfer_bio(dev, bio);
		__blk_end_request_all(req, 0);
	}
}


/* make_request版本 */
static void vblkdev_make_request(struct request_queue *q, struct bio *bio)
{
	struct vblkdev *dev = q->queuedata;
	int status;

	status = vblkdev_xfer_bio(dev, bio);
    bio->bi_error = status;
    bio_endio(bio);
}

/* 获取设备信息 */
static int vblkdev_getgeo(struct block_device *bdev, struct hd_geometry *geo)
{
	long size;
	struct vblkdev *dev = bdev->bd_disk->private_data;

	size = dev->size*(HARDSECT_SIZE/KERNEL_SECTOR_SIZE);
	geo->cylinders = (size & ~0x3f) >> 6;
	geo->heads = 4;
	geo->sectors = 16;
	geo->start = 4;

	return 0;
}

/* 定义块设备操作函数 */
static struct block_device_operations vblkdev_ops = {
	.getgeo          = vblkdev_getgeo,
};

/* 初始化虚拟设备 */
static void setup_device(struct vblkdev *dev, int which)
{
    /* 分配dev结构所需主存 */
	memset (dev, 0, sizeof (struct vblkdev));
	dev->size = NSECTORS*HARDSECT_SIZE;
	dev->data = vmalloc(dev->size); /* 为虚拟块设备申请主存 */
	if (dev->data == NULL) {
		printk (KERN_NOTICE "vmalloc failure.\n");
		return;
	}

    /* 初始化请求队列 */
	spin_lock_init(&dev->lock);
	switch (request_mode) {
	case VMEMD_NOQUEUE:
		dev->queue = blk_alloc_queue(GFP_KERNEL);
		if (dev->queue == NULL)
			goto out_vfree;
		blk_queue_make_request(dev->queue, vblkdev_make_request);
		break;
	default:
		printk(KERN_NOTICE "Bad request mode %d, using simple\n", request_mode);
	case VMEMD_QUEUE:
		dev->queue = blk_init_queue(vblkdev_request, &dev->lock);
		if (dev->queue == NULL)
			goto out_vfree;
		break;
	}
	blk_queue_logical_block_size(dev->queue, HARDSECT_SIZE);
	dev->queue->queuedata = dev;

    /* 初始化gendisk */
	dev->gd = alloc_disk(VBLKDEV_MINORS);
	if (!dev->gd) {
		printk (KERN_NOTICE "alloc_disk failure\n");
		goto out_vfree;
	}
	dev->gd->major = vblkdev_major;
	dev->gd->first_minor = which*VBLKDEV_MINORS;
	dev->gd->fops = &vblkdev_ops;
	dev->gd->queue = dev->queue;
	dev->gd->private_data = dev;
	snprintf (dev->gd->disk_name, 32, "vblkdev_%c", which + 'a');
	set_capacity(dev->gd, NSECTORS*(HARDSECT_SIZE/KERNEL_SECTOR_SIZE));
	add_disk(dev->gd);
	return;

out_vfree:
	if (dev->data)
		vfree(dev->data);
}

/* 模块初始化函数 */
static int __init vblkdev_init(void)
{
	int i;

	vblkdev_major = register_blkdev(vblkdev_major, "vmem_disk"); /* 申请并注册主设备号 */
	if (vblkdev_major <= 0) {
		printk(KERN_WARNING "vmem_disk: unable to get major number\n"); 
		return -EBUSY;
	}

	devices = kmalloc(NDEVICES*sizeof (struct vblkdev), GFP_KERNEL); /* 为管理数据结构申请空间 */
	if (!devices)
		goto out_unregister;
	for (i = 0; i < NDEVICES; i++)
		setup_device(devices + i, i);

	return 0;

out_unregister:
	unregister_blkdev(vblkdev_major, "sbd");
	return -ENOMEM;
}

/* 模块清理函数 */
static void vblkdev_exit(void)
{
	int i;

	for (i = 0; i < NDEVICES; i++) {
		struct vblkdev *dev = devices + i;

		if (dev->gd) {
			del_gendisk(dev->gd);
			put_disk(dev->gd);
		}
		if (dev->queue) {
			if (request_mode == VMEMD_NOQUEUE)
				kobject_put (&dev->queue->kobj);
			else
				blk_cleanup_queue(dev->queue);
		}
		if (dev->data)
			vfree(dev->data);
	}
	unregister_blkdev(vblkdev_major, "vmem_disk");
	kfree(devices);
}

module_init(vblkdev_init);
module_exit(vblkdev_exit);
MODULE_LICENSE("GPLv2");
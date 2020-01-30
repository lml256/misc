#include<linux/init.h>
#include<linux/module.h>
#include<linux/proc_fs.h>
#include<linux/kernel.h>
#include<linux/sched/signal.h>  // 4.11后版本的内核中for_each_process的定义

MODULE_LICENSE("GPL");

static int num = -1;

module_param(num, int, S_IRUGO);

static __init int km_init(void) {
	struct task_struct *p = NULL;

	for_each_process(p) {
		if(num == 0) {
			break;
		}
		printk("pid = %d, ppid = %d, name = %s\n", p->pid, p->parent->pid, p->comm);
		num--;
	}
	
	return 0;
}


static __exit void km_exit(void) {
	printk("kmodule has be removed");
}

module_init(km_init);
module_exit(km_exit);

#include <linux/init.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/kernel.h>
#include <linux/sched/signal.h>  // 4.11后版本的内核中for_each_process的定义
#include <linux/fs.h>
#include <linux/seq_file.h> 
#include <linux/uaccess.h>
#include <linux/sched.h>

#define BUFFER_SIZE 1024
MODULE_LICENSE("GPL");

char global_buffer[BUFFER_SIZE];

int stoi(char *s) {
	int sum = 0;
	for(; (*s) != 0 && (*s) != '\n'; s++) {
		sum = sum * 10 + ((*s) - '0');
	}
	return sum;
}

static int my_proc_show(struct seq_file *m, void *v)
{
	printk("pids = %s\n", global_buffer); 
	int pid = stoi(global_buffer);
	printk("pid: %d\n", pid);
	//	struct task_struct *process = find_process_by_pid(pid); /*新版本内核不适用，包括find_task_by_vpid也不在适用*/
	struct task_struct *process = pid_task(find_vpid(pid), PIDTYPE_PID);
	if(!process) {
		seq_printf(m, "pid is invilable\n");
		return 0;	
	}
		
	seq_printf(m,"process info:\n"); 
	seq_printf(m," pid:   %d\n", pid); 
	seq_printf(m," ppid:  %d\n", process->parent->pid); 
	seq_printf(m," name:  %s\n", process->comm); 
	seq_printf(m," ...\n"); 
	return 0;
}

static int my_proc_open(struct inode *inode, struct file *file) {
	return single_open(file, my_proc_show, NULL);
}

static ssize_t proc_write_test(struct file *file, const char __user *buffer, size_t count, loff_t *f_pos) {
	copy_from_user(global_buffer, buffer, count);
	return count;
}


/*创建/proc文件的文件操作结构体*/
static struct file_operations my_fops = {
	.owner	= THIS_MODULE,
	.open	= my_proc_open,
	.release = single_release,
	.read	= seq_read,
	.llseek	= seq_lseek,
	.write 	= proc_write_test,
};

static __init int test_init(void) {
	proc_create("query_pid", 0666, NULL, &my_fops);  /* 在/proc中创建query_pid文件, 当前内核不支持create_proc_entry */
	return 0;
}

static __exit void test_exit(void) {
	remove_proc_entry("query_pid", NULL);
}

module_init(test_init);
module_exit(test_exit);


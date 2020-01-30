obj-m :=main.o                  #使用kmodule.o文件来产生kmodule.ko
CONFIG_MODULE_SIG=n
all:
	make -C /lib/modules/$(shell uname -r)/build SUBDIRS=$(PWD) modules    #编译模块
clean:
	make -C /lib/modules/$(shell uname -r)/build SUBDIRS=$(PWD) clean      #清理


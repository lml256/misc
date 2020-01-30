obj-m :=kmodule.o                  #使用kmodule.o文件来产生kmodule.ko
all:
	make -C /lib/modules/$(shell uname -r)/build SUBDIRS=$(PWD) modules    #编译模块
clean:
	make -C /lib/modules/$(shell uname -r)/build SUBDIRS=$(PWD) clean      #清理


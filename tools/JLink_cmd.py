./JLinkExe -if SWD -device MK64FN1M0xxx12 -speed 1000
connect
erase
loadbin /home/sandlacus/jenkins_jobs/sl_log/sl_homebox_log/17/kds.srec 0x0
go

>r
>go

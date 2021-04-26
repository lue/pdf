import glob
import os


for c1 in range(0,50,1):
    c2=c1+1
    if c2>250:
        c2=250
    for jj in ['130']:  # '073', '098', '112', '130'
        ss = 'sbatch --export=ALL,pdf_c1='+str(c1)+',pdf_c2='+str(c2)+',snap_id='+jj+' starter.sh'
        print(ss)

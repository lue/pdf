import pynbody
import numpy as np



N_files = 1920
box = 1000
snap_id = '098'

path_cov = '/scratch/kaurov/misha_c/mdpl2/snapshot_'+snap_id+'/snap_'+snap_id+'.'

xbins = np.linspace(0,box,box/(2*10)+1)
total_n_particles = 0

for i in range(0, N_files):
    print(i,)
    s = pynbody.load(path_cov+str(i))
    print(len(s))
    #print(s['pos'][:,0].min(), s['pos'][:,0].max())
    total_n_particles += len(s['pos'])
    for c in range(0, 50):
        x_min = xbins[c]
        x_max = xbins[c+1]
        temp = s['pos'][(s['pos'][:,0] >= x_min) & (s['pos'][:,0] < x_max), :]
        if len(temp)>0:
            np.savez('/scratch/kaurov/misha_c/mdpl2/snapshot_'+snap_id+'/slice_' + str(i) + '_' + str(c)+'.npz', pos = temp)
            print(temp.shape)

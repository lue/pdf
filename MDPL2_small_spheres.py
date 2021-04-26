import argparse
import glob

parser = argparse.ArgumentParser(description='Process some integers.')                                  
parser.add_argument('c1', metavar='N', type=int, nargs=1, help='an integer for the accumulator')        
parser.add_argument('c2', metavar='N', type=int, nargs=1, help='an integer for the accumulator')       
parser.add_argument('snap_id', metavar='N', type=str, nargs=1, help='an integer for the accumulator')                                           

args = parser.parse_args()



import pynbody
import numpy as np



N_files = 1920
box = 1000
snap_id = args.snap_id[0]

path_cov = '/scratch/kaurov/misha_c/mdpl2/snapshot_'+snap_id+'/snap_'+snap_id+'.'

Rs = np.array([2.5, 10.])

Rmax = Rs.max()
# Rmax = 2
xbins = np.linspace(0,box,box/(2*Rmax)+1)
print(xbins)

print('Slices: ', args.c1[0], args.c2[0], 'total ', len(xbins)-1)
assert args.c2[0] < len(xbins), "Error, c2 larger number of slices"


path_sn = path_cov
# xx = np.zeros([N_grid, N_grid, N_grid])
# xbins = np.linspace(0,box,box/(2*Rmax)+1)
for c in range(args.c1[0], args.c2[0]):
    print(c)
    pos = []
    x_min = xbins[c]
    x_max = xbins[c+1]
    total_n_particles = 0
#     for i in range(0, N_files):
#         print(i,)
#         s = pynbody.load(path_sn+str(i))
#         print(len(s))
#         #print(s['pos'][:,0].min(), s['pos'][:,0].max())
#         total_n_particles += len(s['pos'])
        
#         x_shift = np.random.rand(3) * 2.5
        
#         s['pos'][:, 0] += x_shift[0]
#         s['pos'][:, 1] += x_shift[1]
#         s['pos'][:, 2] += x_shift[2]
        
#         s['pos'][:, 0] = s['pos'][:, 0] % box
#         s['pos'][:, 1] = s['pos'][:, 1] % box
#         s['pos'][:, 2] = s['pos'][:, 2] % box
        
#         temp = (s['pos'][:,0] >= x_min) & (s['pos'][:,0] <= x_max)
#         if len(temp)>0:
#             if len(pos)==0:
#                 pos = s['pos'][temp]
#             else:
#                 pos = np.concatenate([pos, s['pos'][temp]])
    files = glob.glob('/scratch/kaurov/misha_c/mdpl2/snapshot_'+snap_id+'/slice_' + '*' + '_' + str(c)+'.npz')
    c2 = (c+1) % 50
    files += glob.glob('/scratch/kaurov/misha_c/mdpl2/snapshot_'+snap_id+'/slice_' + '*' + '_' + str(c2)+'.npz')
    pos = np.load(files[0])['pos']
    for i in (files[1:]):
        temp = np.load(i)['pos']
        pos = np.concatenate([pos, temp])
    print(pos.shape)
#     print('Total N of particles: ', total_n_particles)
    for R in Rs:
        print(R)
        R_res_temp = []
        R_res_temp_box = []
        ii_n = int(np.round((x_max-x_min)/(2*R)))
        jj_n = int(np.round((box)/(2*R)))
        for ii in np.arange(ii_n*c, ii_n*(c+1), 0.5):
            t = np.abs(pos[:,0] - ii*2*R - R)
            temp_i = pos[(t < R) | (t > box - R)]
            temp_i[:, 0] = (temp_i[:, 0] - ii*2*R - R) % box
            temp_i[temp_i[:, 0] > box/2, 0] -= box
            for jj in np.arange(0, jj_n, 0.5):
                t = np.abs(temp_i[:,1] - jj*2*R - R)
                temp_j = temp_i[(t < R) | (t > box - R)]
                temp_j[:, 1] = (temp_j[:, 1] - jj*2*R - R) % box
                temp_j[temp_j[:, 1] > box/2, 1] -= box
                for kk in np.arange(0, jj_n, 0.5):
                    t = np.abs(temp_j[:,2] - kk*2*R - R)
                    temp_k = temp_j[(t < R) | (t > box - R)]
                    temp_k[:, 2] = (temp_k[:, 2] - kk*2*R - R) % box
                    temp_k[temp_k[:, 2] > box/2, 2] -= box
                    filt = (temp_k[:,0])**2 + \
                    (temp_k[:,1])**2 + \
                    (temp_k[:,2])**2 < R**2
                    R_res_temp.append(filt.sum())
                    R_res_temp_box.append(len(temp_k))
            np.savez(snap_id + '_' + str(R) + '_' + str(c)+'_'+'sph'+'.npz', R_res_temp=R_res_temp, R_res_temp_box=R_res_temp_box, R=R)
        print(np.array(R_res_temp).sum(), pos.shape[0])
    

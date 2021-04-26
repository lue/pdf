
import numpy as np
import glob
import matplotlib.pyplot as plt

plt.figure(dpi=200, facecolor='w')

for snap in ['130']: # 073', '098', '112', '
    for R in [2.5]:#, 5.0, 10.0]: # 0.625, 1.25, 
        d = []
        for f in glob.glob('MDPL2/snapshot_'+snap+'/'+snap+'_'+str(R)+'_*_sph.npz'):
            d.append(np.load(f)['R_res_temp'])

        d = np.concatenate(d)
        print(d.shape, d.shape[0] / (1000/(2*R))**3)
        
#         d
#         d = d[::2,::2,::2]
        dmean = 4./3*np.pi*(R)**3*3.84**3
#         dmean = (2*R)**3*3.84**3
        # dmean = 4./3*np.pi*(0.3125)**3*3.84**3
        print(dmean, d.mean())
        print(dmean / d.mean() - 1.)

        bins = np.linspace(-3,4,128)
        H,X = np.histogram(np.log10(d/dmean), bins=bins)

        Xc = (X[1:]+X[:-1])/2
        plt.plot(Xc, H, label=snap+'_'+str(R))
        plt.yscale('log')

#         np.savetxt('output/MDPL2_'+snap+'_all_spheres_'+str(R)+'.txt', d.astype(int)) 
#         np.save('output/MDPL2_'+snap+'_all_spheres_'+str(R)+'.npy', np.bincount(d))        
        np.savetxt('output/MDPL2_'+snap+'_all_spheres_'+str(R)+'_test1.txt', np.bincount(d), fmt='%i')   
        np.savetxt('output/MDPL2_'+snap+'_all_spheres_'+str(R)+'_test1.txt', d, fmt='%i')        
        np.savetxt('output/MDPL2_'+snap+'_spheres_bins_'+str(R)+'_test1.txt', bins)
        np.savetxt('output/MDPL2_'+snap+'_spheres_values_'+str(R)+'_test1.txt', H)
        np.savetxt('output/MDPL2_'+snap+'_spheres_err_rel_'+str(R)+'_test1.txt', np.sqrt(H)/H)

plt.xlabel('1+\delta')
plt.legend()
plt.title('MDPL2 histograms')

d = d.reshape([400,400,400])

for i in range(2):
    for j in range(2):
        for k in range(2):
            print(d[i::2,j::2,k::2].flatten().shape)
            np.savetxt('output/MDPL2_'+snap+'_all_spheres_'+str(R)+'_'+str(i)+str(j)+str(k)+'_test1.txt', d[i::2,j::2,k::2].flatten(), fmt='%i')        
            

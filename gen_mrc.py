from aspire.source import MicrographSimulation
from aspire.volume import Volume
from aspire.volume import AsymmetricVolume
from aspire.noise import WhiteNoiseAdder
from aspire.operators import RadialCTFFilter
import numpy as np
import gc

#載入3j79的volume
vol = Volume.load('/home/m112040034/workspace/3j79-1.mrc', dtype=np.float64)

#設定虛擬出的每張顯微影像含有的粒子數
n_particles_per_micrograph = 40
#生成n_microggraphs張影像
n_micrographs = 300

#最大最小焦距
defocus_min = 8000              # Minimum defocus value (in angstroms).
defocus_max = 38000              # Maximum defocus value (in angstroms).
defocus_ct = n_micrographs
random_defocus_values = np.random.uniform(defocus_min, defocus_max, defocus_ct)
# Create filters pixel_size(nominal pixel、額定電壓、焦距、球像差)
ctfs = [RadialCTFFilter(pixel_size=1.34, voltage=300, defocus=d, Cs=2.0, alpha=0.07) for d in random_defocus_values]

noise_var_list = []
signal_var_list = []
for i in range(10):
    # 生成經過CTF Filter的影像
    src = MicrographSimulation(
        vol,
        particles_per_micrograph=n_particles_per_micrograph,
        micrograph_size=3072,
        micrograph_count=1,  # 一次生成一張影像
        ctf_filters=[ctfs[i]],
    )
    
    # 計算影像信號的變異數
    images = src.images[:].asnumpy()
    signal_var = np.var(images)
    signal_var_list.append(signal_var)
    '''
    # 設定生成的目標SNR值=0.1，SNR值的計算為signal_var/noise_var
    target_snr = 0.05
    # 反推noise_std以設定在WhiteNoiseAdder中的參數
    noise_var = signal_var / target_snr
    #print(f"第{i+1}張影像的噪聲變異數: {noise_std}")
    noise_var_list.append(noise_var)
    '''
target_snr = 0.05
# 計算平均noise_var
#avg_noise_var = sum(noise_var_list) / len(noise_var_list)
avg_signal_var = sum(signal_var_list) / len(signal_var_list)
avg_noise_var = avg_signal_var/target_snr
print("Average of noise_var:", avg_noise_var,"avg_sig_var", avg_signal_var)

# Create our noise using WhiteNoiseAdder
noise = WhiteNoiseAdder(avg_noise_var, seed=2024)

# Add noise to our MicrographSimulation using the noise_adder argument
src = MicrographSimulation(
    vol,
    noise_adder=noise,
    particles_per_micrograph=n_particles_per_micrograph,
    micrograph_size=3072,
    micrograph_count=n_micrographs,
    ctf_filters=ctfs,
    seed=2024,
)
noise_images = src.images[:].asnumpy()
src.save('/home/m112040034/workspace/simulation/mrc/train')


whole_var = np.var(noise_images)
sig_var = whole_var - avg_noise_var
SNR = sig_var/avg_noise_var
print("SNR:", SNR,", noise_var:",avg_noise_var,", whole_var:",whole_var)
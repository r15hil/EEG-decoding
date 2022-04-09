
fs = 256;
t = 0:1/fs:1-1/fs;
f = fopen('/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/logs/texts/connected_no_filter.txt');
data = textscan(f,'%s');
fclose(f);
x = str2double(data{1}(2:end-1))';

[pxx,f] = pwelch(x,500,300,500,fs);
plot(f,10*log10(pxx))
xlabel('Frequency (Hz)')
ylabel('PSD (dB/Hz)')
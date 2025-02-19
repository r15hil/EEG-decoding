
fs = 512;
t = 0:1/fs:1-1/fs;
f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\saved_array.txt");
data = textscan(f,'%s');
fclose(f);
x_open = removeDC(str2double(data{1}(2:end-1)))';

f = fopen("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\fs512hz_gain255_30s\closed\closed_eyes2.txt");
data = textscan(f,'%s');
fclose(f);
x_close = removeDC(str2double(data{1}(2:end-1)))';

fs=512;

x_open = bandpass(x_open,[1 37],fs);
average_samples = 4;
data = x_open';
s1 = size(data, 1);
m  = s1 - mod(s1, average_samples);
y  = reshape(data(1:m), average_samples, []); 
averaged_samples_open = sum(y, 1) / average_samples;

fs_new = 128;

x_close = bandpass(x_close,[1 37],fs);
average_samples = 4;
data = x_close';
s1 = size(data, 1);
m  = s1 - mod(s1, average_samples);
y  = reshape(data(1:m), average_samples, []); 
averaged_samples_close = sum(y, 1) / average_samples;


figure;
[pxx_open,f_open] = pwelch(averaged_samples_open,500,300,500,fs_new);
[pxx_close,f_close] = pwelch(averaged_samples_close,500,300,500,fs_new);
plot(f_open,10*log10(pxx_open))
hold on;
plot(f_close,10*log10(pxx_close))
xlabel('Frequency (Hz)')
ylabel('PSD (dB/Hz)')
legend('Open','Closed')
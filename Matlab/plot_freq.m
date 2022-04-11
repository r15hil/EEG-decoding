close all
clear all

f = fopen('C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\logs\texts\10hz_fs256_unfilt.txt');
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';

figure;
plot(1:length(data), data);
title('Time Series')

y = lowpass(data,20,256);
figure;
plot(1:length(y), y);
title('Data filtered')


Fs = 256;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(data);     % Length of signal
t = (0:L-1)*T;        % Time vector

figure;
s_fft = fft(data);
P2 = abs(s_fft/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of Data')
xlabel('f (Hz)')
ylabel('|P1(f)|')
ylim([0 12])

% Fs = 256;            % Sampling frequency                    
% T = 1/Fs;             % Sampling period       
% L = length(data);             % Length of signal
% t = (0:L-1)*T;        % Time vector

% figure;
% s_fft = fft(y);
% P2 = abs(s_fft/L);
% P1 = P2(1:L/2+1);
% P1(2:end-1) = 2*P1(2:end-1);
% 
% f = Fs*(0:(L/2))/L;
% plot(f,P1) 
% title('Single-Sided Amplitude Spectrum of Data')
% xlabel('f (Hz)')
% ylabel('|P1(f)|')
% ylim([0 12])

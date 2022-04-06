close all
clear all

f = fopen('/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/logs/texts/connected_no_filter.txt');
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';

figure;
plot(1:length(data), data);
title('Time Series')

% y = lowpass(data,20,256);
% figure;
% plot(1:length(y), y);
% title('Data filtered')


Fs = 256;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(data(1,1:256));             % Length of signal
t = (0:L-1)*T;        % Time vector

figure;
s_fft = fft(data(1,512:768));
P2 = abs(s_fft/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of Data')
xlabel('f (Hz)')
ylabel('|P1(f)|')
ylim([0 12])


figure;

Fs = 256;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(data(1,256:512));             % Length of signal
t = (0:L-1)*T;        % Time vector

figure;
s_fft = fft(data(1,256:512));
P2 = abs(s_fft/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of Data')
xlabel('f (Hz)')
ylabel('|P1(f)|')
ylim([0 12])

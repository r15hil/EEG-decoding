clear all

% 8.57 Hz, 10 Hz, 12 Hz and 15 Hz
T = readtable("C:\Users\RISHI\Desktop\FYP\EEG-decoding\Matlab\CCA\OpenSourceData\subject2.csv");
eight = T.F1;
ten = T.F2;
twelve = T.F3;
fifteen = T.F4;

X = bandpass(fifteen,[1 37],256)';

fs = 256; % Sampling frequency (samples per second) 
dt = 1/fs; % seconds per sample 
StopTime = 2; % seconds 
t = (0:dt:StopTime)'; % seconds 

% #########################################################################
F = 8.57; % Sine wave frequency (hertz) 
data = sin(2*pi*F*t);
data1 = cos(2*pi*F*t);
Y = data(1:end-1,:)';
Y1 = data1(1:end-1,:)';

data_h = sin(2*pi*F*2*t);
data1_h = cos(2*pi*F*2*t);
Y_h = data_h(1:end-1,:)';
Y1_h = data1_h(1:end-1,:)';

[r7, Wx7, Wy7] = cca_calc(X(:,1:length(Y)),Y);
[r7_1, Wx7_1, Wy7_1]= cca_calc(X(:,1:length(Y1)),Y1);

[r7_h, Wx7_h, Wy7_h] = cca_calc(X(:,1:length(Y)),Y_h);
[r7_1_h, Wx7_1_h, Wy7_1_h]= cca_calc(X(:,1:length(Y1_h)),Y1_h);
% #########################################################################
F = 10; % Sine wave frequency (hertz) 
data = sin(2*pi*F*t);
data1 = cos(2*pi*F*t);
Y = data(1:end-1,:)';
Y1 = data1(1:end-1,:)';

data_h = sin(2*pi*F*2*t);
data1_h = cos(2*pi*F*2*t);
Y_h = data_h(1:end-1,:)';
Y1_h = data1_h(1:end-1,:)';

[r10, Wx10, Wy10] = cca_calc(X(:,1:length(Y)),Y);
[r10_1, Wx10_1, Wy10_1]= cca_calc(X(:,1:length(Y1)),Y1);
[r10_h, Wx10_h, Wy10_h] = cca_calc(X(:,1:length(Y)),Y_h);
[r10_1_h, Wx10_1_h, Wy10_1_h]= cca_calc(X(:,1:length(Y1_h)),Y1_h);
% #########################################################################
F = 12; % Sine wave frequency (hertz) 
data = sin(2*pi*F*t);
data1 = cos(2*pi*F*t);
Y = data(1:end-1,:)';
Y1 = data1(1:end-1,:)';

data_h = sin(2*pi*F*2*t);
data1_h = cos(2*pi*F*2*t);
Y_h = data_h(1:end-1,:)';
Y1_h = data1_h(1:end-1,:)';

[r12, Wx12, Wy12] = cca_calc(X(:,1:length(Y)),Y);
[r12_1, Wx12_1, Wy12_1]= cca_calc(X(:,1:length(Y1)),Y1);
[r12_h, Wx12_h, Wy12_h] = cca_calc(X(:,1:length(Y)),Y_h);
[r12_1_h, Wx12_1_h, Wy12_1_h]= cca_calc(X(:,1:length(Y1_h)),Y1_h);
% #########################################################################

r7_avg = 0.5 * (r7 + r7_1);
r10_avg = 0.5 * (r10 + r10_1);
r12_avg = 0.5 * (r12 + r12_1);

r7_avg_h_s = 0.5 * (r7 + r7_h);
r10_avg_h_s = 0.5 * (r10 + r10_h);
r12_avg_h_s = 0.5 * (r12 + r12_h);
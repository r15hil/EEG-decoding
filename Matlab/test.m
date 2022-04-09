close all
clear all

f = fopen('/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/logs/texts/connected_no_filter.txt');
data = textscan(f,'%s');
fclose(f);
data = str2double(data{1}(2:end-1))';

figure;

for k = 1:length(data)
    plot(k, data(k), '-x')
    hold on
    if k <= 129
        xlim([1, 128])
        plot(1:k,data(1:k))
    else
        xlim([k-128, k])
        plot(k-128:k,data(k-128:k))
    end
    
    pause(0.0001)
end

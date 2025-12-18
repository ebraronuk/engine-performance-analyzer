% Titreşim sinyalinin FFT'sini alip genlik spektrumunu dondurur.
function mag = vibration_fft(signal)
    % FFT hesapla
    spectrum = fft(signal);
    % Mutlak deger ile genlik spektrumu
    mag = abs(spectrum);
end

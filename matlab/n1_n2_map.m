% N1'den N2'yi yaklasik hesaplayan basit fonksiyon.
% N2 = 0.85 * N1 + 0.002 * N1.^2 formulu kullanilir.
function n2 = n1_n2_map(n1)
    n2 = 0.85 .* n1 + 0.002 .* (n1 .^ 2);
end

% Itki seviyesinden yakit akisini basit oransal iliskiyle hesaplar.
% Yakit akis = k * thrust formulu kullanilir.
function ff = fuel_flow_sim(thrust, k)
    if nargin < 2 || isempty(k)
        k = 0.8; % varsayilan oransal katsayi
    end
    ff = k .* thrust;
end

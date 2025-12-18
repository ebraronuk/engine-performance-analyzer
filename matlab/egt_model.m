% EGT tahmini icin basit lineer model.
% N1 ve yakit akisina dayali hizli hesaplama yapar.
function egt = egt_model(n1, fuel_flow, coeffs)
    % coeffs: [a b c] katsayilari, varsayilan [1.2 2.5 50]
    if nargin < 3 || isempty(coeffs)
        coeffs = [1.2, 2.5, 50];
    end
    a = coeffs(1);
    b = coeffs(2);
    c = coeffs(3);

    % EGT = a*N1 + b*fuel_flow + c
    egt = a .* n1 + b .* fuel_flow + c;
end

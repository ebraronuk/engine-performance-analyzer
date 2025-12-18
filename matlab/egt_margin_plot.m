% EGT marj degerlerini basit cizgi grafigi olarak gosterir.
function egt_margin_plot(margins)
    if nargin < 1
        margins = [];
    end
    plot(margins, '-o');
    grid on;
    xlabel('Ornek');
    ylabel('EGT Marji (C)');
    title('EGT Marj Trend');
end

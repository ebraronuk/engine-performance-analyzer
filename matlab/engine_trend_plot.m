% Zaman ve EGT degerlerini basit cizgi grafiginde gosterir.
function engine_trend_plot(time, egt)
    if nargin < 2
        time = 1:numel(egt);
    end
    plot(time, egt, '-b');
    grid on;
    xlabel('Zaman');
    ylabel('EGT');
    title('EGT Trend');
end

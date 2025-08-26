% Parámetros
Ts = 1;        % Duración del símbolo
L = 16;        % Número de muestras por símbolo
a = 1;       % Factor de roll-off
b = 4;
% Vector de tiempo para el eje x
t = -3:Ts/L:3;

% Versión muestreada del pulso de coseno alzado
pt = rcosdesign(a, 6, L, 'normal');

% Graficar
if b == 1
    plot(t, pt, 'LineWidth', 4);
elseif b == 2
    plot(t, pt, 'r', 'LineWidth', 4);
elseif b == 3
    plot(t, pt, 'g', 'LineWidth', 4);
else
    plot(t, pt, 'm', 'LineWidth', 4);
end

grid on;
hold on;

%marca inicio y fin del coseno truncado
xline(-3,'--r','LineWidth', 1.5)
xline(3,'--r','LineWidth', 1.5)

% Etiquetas
xlabel('Tiempo [T_s]');
ylabel('Amplitud');

if b == 1
    legend('Roll-off = 0');
elseif b == 2
    legend('Roll-off = 0.25');
elseif b == 3
    legend('Roll-off = 0.75');
else
    legend('Roll-off = 1');
end

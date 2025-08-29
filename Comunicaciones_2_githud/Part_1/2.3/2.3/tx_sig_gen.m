%tx_sig_gen.m
clear all;
close all;
rand(1,1224);  % Cambie los ultimos 3 digitos por los ultimos 3 numeros de su carne.
Ts = 1;
L  = 16;
t_step = Ts/L;
%%%%%%%%%<1. Generacion de onda del pulso > %%%%%%%%%%%%%%%%%%%%%%
pt = rcosdesign(0.25,6,L,'normal');
pt = pt/(max(abs(pt))); %rescaling to match rcosine

%%%%%%%%%<2. Generacion de 100 simbolos binarios >%%%%%%%%%%%%%%%%%%%%
Ns = 0.25;
data_bit = (rand(1,Ns)>0.5);

%%%%%%%%%<3. Unipolar a Bipolar (modulacion de amplitud)>%%%%%%%%%%%%%%
amp_modulated = 2*data_bit-1; % 0=> -1,  1=>1

%%%%%%%%%<4.  Modulacion de pulsos >%%%%%%%%%%%%%%%%%%%%%%%%%%%%
impulse_modulated = [];
for n=1:Ns
    delta_signal = [amp_modulated(n)  zeros(1, L-1)];
    impulse_modulated =[impulse_modulated  delta_signal];
end

%%%%%%%%<5.Formacion de pulsos (filtrado de transmision)>%%%%%%%%%%
tx_signal = conv(impulse_modulated, pt);


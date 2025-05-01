clear;
close all;
clc;

% Specificeer het pad naar het CSV-bestand
csv_file = 'Coated_pitch1_0_4hz_v2\Coated_pitch1_0_4hz_v2_Trajectory.csv';

% Lees de gegevens in
data = readtable(csv_file);

% Verkrijg de tijd (in seconden) en de X, Y coördinaten
time = data.Time;  % Tijd in seconden
x = data.X;  % X-coördinaten
y = data.Y;  % Y-coördinaten
z = data.Z   % Z coordinaten

% Plot de X- en Y-coördinaten tegen de tijd
figure;
subplot(2,1,1);
plot(time, x, 'g', 'LineWidth', 1.5);
xlabel('Time (seconds)');
ylabel('X Position');
title('X Position over Time');

subplot(2,1,2);
plot(time, y, 'b', 'LineWidth', 1.5);
xlabel('Time (seconds)');
ylabel('Y Position');
title('Y Position over Time');

figure;
plot(x, y, 'g', 'LineWidth', 1.5);
xlabel('x (pixels)');
ylabel('y (pixels)');
title('position umr');

% ====== 3D TRAJECTORY PLOT ======
figure;
plot3(x, y, z, 'k', 'LineWidth', 2);
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');
title('3D Trajectory of Tracked Object');
grid on;
axis equal;
view(45, 25);  % Kies een fijne 3D kijkhoek

% ====== ANIMATIE VAN DE 3D TRAJECTORY ======
figure;
hold on;
grid on;
axis equal;
xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');
title('3D Trajectory Animation');
view(45, 25);

% Set axis limits if you want fixed view
xlim([min(x), max(x)]);
ylim([min(y), max(y)]);
zlim([min(z), max(z)]);

% Plot lijn en bewegend punt
trajectoryLine = plot3(NaN, NaN, NaN, 'k-', 'LineWidth', 2);
movingPoint = plot3(NaN, NaN, NaN, 'ro', 'MarkerFaceColor', 'r');

% Maak animatie
for i = 1:length(x)
    set(trajectoryLine, 'XData', x(1:i), 'YData', y(1:i), 'ZData', z(1:i));
    set(movingPoint, 'XData', x(i), 'YData', y(i), 'ZData', z(i));
    drawnow;
    pause(0.01);  % snelheid van animatie aanpassen
end

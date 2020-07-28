% This code is a series of snipets from "demo.m" and %"cnlos_reconstruction.m", and mariko's code stiched together 
% for processing the "interactive" sequence
% The code saves trimmed and rectified separate ".mat" files, ready to be used
%
%
% Author: Javier Grau


%% Code from 'demo.m'
wall_size = 2; % scanned area is 2 m x 2 m
fprintf('\nProcessing interactive results\n');

% this processes the frame, but it could also be directly loaded from the
% preprocessed version in 'interactive/fk_32.mat'
load('interactive/meas_32.mat');
load('interactive/tof_32.mat');

%frame_idx = 73;
for frame_idx=1:130
    frame = squeeze(meas(frame_idx, :, :, :));
    crop = 1024; % crop measurements to 1024 bins

    %% Code from 'cnlos_reconstruction.m'
    % Constants
    bin_resolution = 32e-12; % Native bin resolution for SPAD is 4 ps
    c              = 3e8;    % Speed of light (meters per second)
    width          = wall_size / 2;

    % adjust so that t=0 is when light reaches the scan surface
    if ~isempty(tofgrid)
        for ii = 1:size(frame, 1)
            for jj = 1:size(frame,2 )
                frame(ii, jj, :) = circshift(frame(ii, jj, :), -floor(tofgrid(ii, jj) / (bin_resolution*1e12)));
            end
         end  
    end
    frame = frame(:, :, 1:crop);

    N = size(frame,1);        % Spatial resolution of data
    M = size(frame,3);        % Temporal resolution of data
    range = M.*c.*bin_resolution; % Maximum range for histogram

    % Permute data dimensions
    data = permute(frame,[3 2 1]);

    filename = sprintf('interactive_rect/%03d.mat', frame_idx);
    save(filename, 'data');
end
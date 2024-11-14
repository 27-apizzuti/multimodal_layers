function [winner_map] = winner_map_fnc(maskedVMPMaps, voxels_indices)
% This function takes as input a 4D array and compute 
% voxel-wise winner value (labelling).
%
% Input:        -maskedVMPMaps, 3D + 1D array (x,y,z + contrast)
%               -voxels_indices, 3D binary array 
% 
% Output:       -winner_map, 3D array (x,y,z) with voxel-wise label

%% === Execution ===
% Get voxel preference
dims=size(maskedVMPMaps);
ncontr=dims(end);

temp_deMeanedMat = zeros(numel(maskedVMPMaps(:,:,:,1)),ncontr);   % vectorize vmp maps & put them in 2d matrix form, where columns = contrast
for IterContr=1:ncontr
    temp = squeeze(maskedVMPMaps(:,:,:,IterContr));
    temp_deMeanedMat(:,IterContr) =  temp(:);
end

voxels_indices=voxels_indices(:);

indxMax = zeros(size(voxels_indices));
[~,ind] = max(temp_deMeanedMat,[],2);                       % find contrast with highest value
indxMax(voxels_indices>0) = ind(voxels_indices>0);          % save index

winner_map = reshape(indxMax,dims(1),dims(2),dims(3));      % reshape it



end


function [tuningCurves, NrOfVox] = tuning_curve_fnc(dataset,labels)
% This function computes tuning curves: for each class of voxels computes
% mean and standard deviation of the metric stored in the dataset 
% (e.g. t-values)
% Input:    -dataset, 3D + 1D array (x,y,z + contrast)[VMPdim]
%           -labels, 3D array [VMPdim]
%
% Output:   -tuningCurves, 4x4x2 array (mean, std for each contrast)
%           -NrOfVox,4x1 number of voxels for each class

%% === Execution === 
ncond=size(dataset,4);                  % number of constrast
tuningCurves=zeros(ncond,ncond,2);   
NrOfVox=zeros(1,ncond);
for nn=1:ncond
    % for each contrast, use the preferred axis of motion indices to
    % compute the mean and se
    
    for cc=1:ncond
        indxMatrix = labels==nn;
        temp = squeeze(dataset(:,:,:,cc)).*double(indxMatrix);
        temp = temp(temp(:)~=0);
        tuningCurves(nn,cc,1) = mean(temp);
        tuningCurves(nn,cc,2) = std(temp)./sqrt(sum(labels(:)==nn));
    end
    NrOfVox(1, nn) = sum(labels(:)==nn);
    
end




end


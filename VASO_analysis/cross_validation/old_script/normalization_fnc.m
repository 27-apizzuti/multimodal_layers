function [norm_VMPMaps, voxels_indices, saveSuffix] = normalization_fnc(VMPMaps,deMeanOpt)
% This function normalizes VMPMaps throught demeaning operation 
% (4 options available)
% Input:    -VMPMaps, 3D + 1D array (x,y,z + contrast)
%           -demeanOpt, string array
%
% Output:   -norm_VMPMaps, 4D array (x,y,z,contrast)
%           -voxels_indices, 3D binary array [same dim of VMPMaps 3D] 

%% === Execution ===
% Normalization

dims=size(VMPMaps);
ncontr=dims(end);

dataMatr = zeros(numel(VMPMaps(:,:,:,1)),ncontr);   % vectorize vmp maps & put them in 2d matrix form, where columns = contrast
for IterContr=1:ncontr
    temp = squeeze(VMPMaps(:,:,:,IterContr));
    dataMatr(:,IterContr) =  temp(:);
end

% Get indices where at least one condition was > 0
overlapArr = sum(dataMatr>0,2);     
tempInd = overlapArr>0;             % logic index

% Mask matrix to compute the mean
tempArr = dataMatr.*double(repmat(tempInd, [1 ncontr]));
tempArr = tempArr(tempInd,:);

temp_deMeanedMat = zeros(size(dataMatr)); % initialize  matrix

switch deMeanOpt
    
    case 1 % demeaning across contrasts (row-wise)
        av = mean(tempArr,2);
        saveSuffix = 'dMeanAcross_';
        
    case 2 % demeaning within each contrast (column-wise)
        av=mean(tempArr,1);
        saveSuffix = 'dMeanWithin_';
        
    case 3 % demean based on pulled values across & within contrasts
        av = mean(tempArr(:));
        saveSuffix = 'dMeanPulled_';
        
    case 4 % no demeaning
        av = zeros(1,NrOfCont);
        saveSuffix = 'dMeaIterControne_';
end

temp_deMeanedMat(tempInd,:) = tempArr-av;
norm_VMPMaps = reshape(temp_deMeanedMat,dims(1),dims(2),dims(3), dims(4)); % reshape it

voxels_indices = reshape(overlapArr,dims(1),dims(2),dims(3)); % reshape it

end


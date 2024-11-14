%% Leave-one-run out, cross-validation for AOM tuning curves
% TRAINING SET
% Compute tuning curve from GLM results computed using all runs-1 (leave one out)
% It works for one processing (standard or nordic)
%%
clear all;
clc;
% ===== Input Setting ======
%
subj='sub-04';
proc='magn_only_noNOISE';       % for the input folder

PathIn = ['D:\Pilot_Exp_VASO\pilotAOM\' subj '\derivatives\'...
    'func\AOM\vaso_analysis\' proc '\cross_validation'];
PathIn_VOI = ['D:\Pilot_Exp_VASO\pilotAOM\' subj '\derivatives'...
    '\func\AOM\vaso_analysis\magn_only\GLM'];
% Output folder
PathOut = ['D:\Pilot_Exp_VASO\pilotAOM\' subj '\derivatives\'...
    'func\AOM\vaso_analysis\' proc '\cross_validation\output\WinnerMaps'];

if ~exist(PathOut, 'dir')
    mkdir(PathOut)
end

voiFile = xff(fullfile(PathIn_VOI, [subj '_clust500_fdr0001_AND_sphere.voi']));

% ===== Parameters ======
condNames={'horizontal','diag45','vertical','diag135'};
NrOfCont=4; % Number of contrast that we will use
NrOfVox=zeros(NrOfCont,2); % to store data for histogram

colors=jet(numel(condNames)*4);
colors=colors(3:numel(condNames):end,:);

deMeanOpt=1; % 1: demeaning across contrasts [default];
% 2: demeaning within contrast;
% 3: pulled demeaning (across & within contrast)
% 4: no demeaning

if strcmp(proc, 'standard')
    nameBOLD = 'BOLD_meanRuns_noNORDIC';
    nameVASO = 'VASO_meanRuns_noNORDIC';
    
else 
    nameBOLD = 'BOLD_meanRuns_NORDIC';
    nameVASO = 'VASO_meanRuns_NORDIC';
end


%% ===== Execution ======
TuningCurves=struct;        % output structure
TrainingSet=struct;         % output structure

cv_fld_files=dir([PathIn '\runs*.*']);

for iterRunOut=1:size(cv_fld_files,1)
    
    % Go through different cv folders
    fld = [cv_fld_files(iterRunOut).folder, '\'...
        cv_fld_files(iterRunOut).name, '\GLM'];
    
    bold_vmp = xff(fullfile(fld,[nameBOLD '.vmp']));
    vaso_vmp = xff(fullfile(fld,[nameVASO '.vmp']));
        
    % Loop through contrasts [ BOLD, VASO]
    for iterContrast=1:2
        crossValidation=struct;
        
        disp(['Leave one run out: '  num2str(iterRunOut)...
            ' [Contrast ' num2str(iterContrast) ']']);
        
        if iterContrast==1 % bold
            vmpFile = bold_vmp;
            field='BOLD';
        else
            vmpFile = vaso_vmp;
            field='VASO';
        end
        % Preparing input for winner_maps_fnc.m
        % step 1: voi to vmr conversion
        indx = sub2ind([256,256,256], ...
            voiFile.VOI(1).Voxels(:,1)+1, ...
            voiFile.VOI(1).Voxels(:,2)+1, ...
            voiFile.VOI(1).Voxels(:,3)+1); % +1 is necessary to avoid voxel shifts in BV
        
        ROI_VMRData = zeros(256,256,256);
        ROI_VMRData(indx) = 240;
        
        ROI_VMR =xff('new:vmr');
        ROI_VMR.VMRData = uint8(ROI_VMRData);
        
        % step 2: mask vmp with vmr (converted voi)
        vmpFile = vmpFile.MaskWithVMR(ROI_VMR,100); % 100 is the threshold value
        
        % step 3: make non-significant voxels =0
        tempMatrix = zeros(size(vmpFile.Map(1).VMPData));
        maskedVMPMaps = zeros([size(tempMatrix), 4]);
        for cc=1:NrOfCont
            
            if iterContrast==2 % vaso
                tempVMP = vmpFile.Map(cc).VMPData * (-1); % flip signs for VASO
            else
                tempVMP = vmpFile.Map(cc).VMPData;
            end
            
            thrsh= vmpFile.Map(cc).FDRThresholds(2,2); % (2,2) corresponds to q = 0.05
            temp = tempVMP >thrsh;
            maskedVMPMaps(:,:,:,cc) = tempVMP .*temp;
            tempMatrix = tempMatrix + double(temp);
        end
        
        %% Compute winner maps
        [demeaned_maskedVMPMaps, voxels_indices, saveSuffix] = normalization_fnc(maskedVMPMaps,deMeanOpt);
        [idxMax] = winner_map_fnc(demeaned_maskedVMPMaps, voxels_indices);
        
        %% Compute tuning curves
        [tuningCurves, NrOfVox] = tuning_curve_fnc(demeaned_maskedVMPMaps,idxMax);
        
            
        %% Storing results
        % 1. Matlab structure
        crossValidation.name=cv_fld_files(iterRunOut).name;
        crossValidation.data=demeaned_maskedVMPMaps;
        crossValidation.label=idxMax;
        crossValidation.condOrder=condNames;
        crossValidation.demeanOpt=saveSuffix;
        crossValidation.count=NrOfVox;
        
        % 2. Save Winner maps as .VOI
        % 2.1. Intermediate step -> put 3D winner map into VMP [256x256x256]
        
        targetVMP = vmpFile.CopyObject;
        targetVMP.Map(2:5) = []; % we only want to have one map
        targetVMP.NrOfMaps = 1;
        targetVMP.Map(1).VMPData = single((idxMax).*10); % matrix of preferences [vmp size dims]
        targetVMP_HR = targetVMP.MakeHiResVMP(1); % matrix of preferences [256x256x256]
        targetVMR = targetVMP_HR.SaveAsVMR; 
        dataMat = targetVMR.VMRData;
        % when creating the vmr, the vmp values [1-4] will be scaled. Find which
        % ones these are, to create voi file in BV [manually for right now]
        val = unique(dataMat(dataMat(:)>0)); % NrOfCont values, smallest equals to 0 in the high res vmp
        val = val(2:end);
        template = [75 125 175 225]; % colors pref.maps
        indx = 1:numel(condNames);
        indx = indx(ismember(template,val));
        
        % 2.2 Convert VMP into VOI
        if ~isempty(indx)
            % convert the preference matrix into a voi
            tempVOI = voiFile.CopyObject;
            tempVOI.VOI(2:end) = [];
            tempVOI.NrOfVOIs = numel(indx);
            for nn=1:numel(indx)
                tempVOI.VOI(nn) = tempVOI.VOI(1);
                [x,y,z]=ind2sub(size(dataMat),find(dataMat(:) == val(nn)));
                tempVOI.VOI(nn).Name = condNames{indx(nn)};
                tempVOI.VOI(nn).Color = round(colors(indx(nn),:).*255);
                tempVOI.VOI(nn).NrOfVoxels = numel(x);
                tempVOI.VOI(nn).Voxels = [x y z]-1; % the -1 is SUPER importart. there is a shift between NE and BV
                numel(x);
            end
            
            
            % 2.3 Saving VOI
            if iterContrast==1
                tempVOI.SaveAs(fullfile(PathOut,['TrainingSet_' nameBOLD '_' cv_fld_files(iterRunOut).name ...
                    '_prefMap_' saveSuffix voiFile.VOI(1).Name '.voi']));
            else
                tempVOI.SaveAs(fullfile(PathOut,['TrainingSet_' nameVASO '_' cv_fld_files(iterRunOut).name ...
                    '_prefMap_' saveSuffix voiFile.VOI(1).Name '.voi']));
            end
            
            TuningCurves(iterRunOut).(field)=tuningCurves;
            TrainingSet(iterRunOut).(field)=crossValidation;
            
            
            disp(['======================================'])
        end
        
    end
end

save(fullfile(PathOut, ['TrainingSet_' proc, '_TC_' saveSuffix voiFile.VOI(1).Name]),'TuningCurves');
save(fullfile(PathOut, ['TrainingSet_' proc '_RES_' saveSuffix voiFile.VOI(1).Name]), 'TrainingSet');







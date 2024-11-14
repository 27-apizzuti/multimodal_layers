%% Comparison with averaged runs winner
clear all;
clc;
%% ===== Input Setting ======

subj='sub-04';
deMeanOpt=1;
proc='magn_only_noNOISE';

if strcmp(proc,'standard')
    tag='stand';
    vmpNAME='_meanRuns_noNORDIC.vmp';
else
    tag='nordic';
    vmpNAME=['_meanRuns_NORDIC_' proc '.vmp'];
end

% Input/Output folder
pathGLM=['D:\Pilot_Exp_VASO\pilotAOM\' subj '\derivatives\'...
    'func\AOM\vaso_analysis\' proc '\GLM'];
PathCV = ['D:\Pilot_Exp_VASO\pilotAOM\' subj '\derivatives\'...
    'func\AOM\vaso_analysis\' proc '\cross_validation\output\WinnerMaps'];
PathAVG=['D:\Pilot_Exp_VASO\pilotAOM\' subj '\derivatives\'...
    'func\AOM\vaso_analysis\winnerMaps'];

file_cv=['Voxels_CV_results_' proc 'deMeanOpt_' num2str(deMeanOpt) '.mat'];

file_avg=['Tuning_curve_localizer_sphere_deMean_'  num2str(deMeanOpt) '.mat'];

ncond=4;        % number of conditions/contrasts
  

%% Execution

load(fullfile(PathCV,file_cv ));
load(fullfile(PathAVG,file_avg ));

% Output structure
Voxels_AVG_CV=struct;

for iterContr=1:2
    if iterContr==1
        field='BOLD';
    else
        field='VASO';

    end
    
    % AVERAGED RUNS
    vmp=xff(fullfile(pathGLM, [field vmpNAME]));
    
    
    temp_labelsAVG=zeros(vmp.VMRDimX, vmp.VMRDimY, vmp.VMRDimZ);
    temp_labelsAVG(vmp.XStart:vmp.XEnd-1, ...
        vmp.YStart:vmp.YEnd-1,...
        vmp.ZStart:vmp.ZEnd-1)=Voxels_AVG.(tag).(field).Voxels_AVG;
    
    
    temp_dataAVG=zeros(256,256,256,4);
    temp_dataAVG(vmp.XStart:vmp.XEnd-1, ...
        vmp.YStart:vmp.YEnd-1,...
        vmp.ZStart:vmp.ZEnd-1,:)=TuningCurves.(tag).(field).demeanMaskVMP;
    
    nvoxAVG=sum(sum(sum(Voxels_AVG.(tag).(field).Voxels_AVG>0)));
    
    temp_labelsCV=zeros(256,256,256);
    temp_labelsCV(Voxels_CV.(field).Voxels(:,1))=Voxels_CV.(field).Voxels(:,2);
    
    nvoxCV=size(Voxels_CV.(field).Voxels,1);
    
    [cmatrix, nVOX_act_pred_match, matchVOX_idx, matchVOX_act_pred, TPR, PPV] = confusion_matrix_fnc(temp_labelsAVG,temp_labelsCV);
    
    % Extract matching voxels from the original group
    % to associate the frequency across cv
    [C,IA,IB]=intersect(matchVOX_idx(:,1),Voxels_CV.(field).Voxels(:,1)); 
    freqCV=Voxels_CV.(field).Voxels(IB,3);
    diag_vox=matchVOX_idx(matchVOX_idx(:,2)==1,1);
    
    label_CV_AVG=zeros(256,256,256);
    label_CV_AVG(diag_vox)=matchVOX_act_pred(matchVOX_idx(:,2)==1);
    
    [tuningCurves, NrOfVox] = tuning_curve_fnc(temp_dataAVG,label_CV_AVG);
    
    % Saving in the structure
    Voxels_AVG_CV.(field).cmatrix=cmatrix;
    Voxels_AVG_CV.(field).TPR=TPR;
    Voxels_AVG_CV.(field).PPV=PPV;
    Voxels_AVG_CV.(field).matchVOX_idx=matchVOX_idx;
    Voxels_AVG_CV.(field).matchVOX_act_pred=matchVOX_act_pred;
    Voxels_AVG_CV.(field).nVOX_act_pred_match=nVOX_act_pred_match;
    Voxels_AVG_CV.(field).nvoxAVG=nvoxAVG;
    Voxels_AVG_CV.(field).nvoxCV=nvoxCV;
    Voxels_AVG_CV.(field).freqCV=freqCV;
    Voxels_AVG_CV.(field).tuningCurves=tuningCurves;
    Voxels_AVG_CV.(field).NrOfVox=NrOfVox;
    
    
    %% Put voxels back to BV
    
    % Winner voxels
    winn_vox=matchVOX_idx;
    winn_lab=matchVOX_act_pred(:,1);
    winn_lab(matchVOX_idx(:,2)==0)=5;   % residual voxels labeled with 5
    winn_freq=freqCV;
    
    targetVMP = vmp.CopyObject;
    targetVMP.NrOfMaps = 5;
    
    cLUT={'blue', 'green', 'yellow', 'red', 'purple'};
    
    for iterCond=1:ncond+1
        
        basenameLut=['ap_cbrew_seq_singlehue_' cLUT{iterCond} '_pos_inv.olt'];
        
        
        idxCLASS=winn_lab==iterCond;
        
        idxVOX=winn_vox(idxCLASS,1);
        freqVOX=winn_freq(idxCLASS);
        
        tempHR=zeros(256,256,256);
        
        tempHR(idxVOX)=freqVOX;     % frequency across cv
        
        dim=size(vmp.Map(1).VMPData);
        dataVMP=zeros(dim);
        
        dataVMP=tempHR(vmp.XStart:vmp.XEnd-1, ...
            vmp.YStart:vmp.YEnd-1,...
            vmp.ZStart:vmp.ZEnd-1);
        
        targetVMP.Map(iterCond).VMPData = single(dataVMP); % matrix of preferences
        targetVMP.Map(iterCond).LowerThreshold = 0;
        targetVMP.Map(iterCond).UpperThreshold = 4;
        targetVMP.Map(iterCond).LUTName = basenameLut;
        
        
    end
    
     targetVMP.SaveAs(fullfile(PathAVG, [field, '_voxels_' proc '.vmp']));
    
end

save([PathAVG, '/Voxels_AVG_CV_' proc], 'Voxels_AVG_CV');



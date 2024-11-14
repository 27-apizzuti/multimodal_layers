% Cross-validated set of voxels
% 1. Within fold selection: voxel's label concordance between training and test;
% 2. Across fold selection: unique voxel's label across CV folds

clear all;
clc;

%% ===== Input Setting ======

subj='sub-04';
proc='magn_only_noNOISE';       % for the input folder
deMeanOpt=1;

% Input/Output folder
PathIn = ['D:\Pilot_Exp_VASO\pilotAOM\' subj '\derivatives\'...
    'func\AOM\vaso_analysis\' proc '\cross_validation\output\WinnerMaps'];

PathVMP=['D:\Pilot_Exp_VASO\pilotAOM\' subj '\derivatives\func\AOM\vaso_analysis\' proc '\'...
    'cross_validation\'];

% ===== Parameters ======
condNames={'horizontal','diag45','vertical','diag135'};
approach={'magn_only'};
NrOfCont=4; % Number of contrast that we will use
training=['TrainingSet_' proc '_RES_dMeanAcross_' subj '_clust500_fdr0001_AND_sphere.mat'];
voiName=[subj '_clust500_fdr0001_AND_sphere'];

if strcmp(proc,'standard')
    
    vmpNAME='_meanRuns_noNORDIC.vmp';
else
    vmpNAME='_meanRuns_NORDIC.vmp';
end

% Output structure
TestSet=struct;
TuningCurves=struct;
Voxels_TRAIN_TEST=struct;       % store all the results within fold
Voxels_CV=struct;               % store all the results across folds

%% ===== Execution ======

load(fullfile(PathIn, training));
nfold=size(TrainingSet,2);
runs=[1:nfold];

for iterFold=1:nfold
    
    for iterContr=1:2
        
        if iterContr==1
            field='BOLD';
        else
            field='VASO';
        end
        
        disp([field ' cross-validation, fold: ' num2str(iterFold)]);
        
        % 1. Find left-out run
        temp=split(TrainingSet(iterFold).(field).name, '_');
        
        train_runs=str2double(temp(2:end))';
        train_runs=train_runs+1;
        
        left_run = find(~ismember(runs,train_runs));
        
        %% TRAIN
        
        % 2. Extract dataset to classify from the left-run test set
        labels_train=TrainingSet(iterFold).(field).label;
        
        % 3. Arrange the data in the same box (256, 256, 256)
        path_train=[PathVMP, TrainingSet(iterFold).(field).name, '\GLM'];
        train_vmp= xff(fullfile(path_train, [field vmpNAME]));
        
        temp_labels_train=zeros(train_vmp.VMRDimX, train_vmp.VMRDimY, train_vmp.VMRDimZ);
        temp_labels_train(train_vmp.XStart:train_vmp.XEnd-1, ...
            train_vmp.YStart:train_vmp.YEnd-1, ...
            train_vmp.ZStart:train_vmp.ZEnd-1) = labels_train;
        
        temp_mask_vox_train=zeros(size(temp_labels_train));
        temp_mask_vox_train(temp_labels_train>0)=1;
        
        %% TEST SET
        path_test=[PathVMP, 'run_' num2str(left_run), '\GLM'];
        test_vmp=xff(fullfile(path_test, [field vmpNAME]));
        temp_data_test=zeros(test_vmp.VMRDimX, test_vmp.VMRDimY, test_vmp.VMRDimZ,NrOfCont);
        
        for cc=1:NrOfCont
            
            if iterContr==1 % BOLD
                buff=test_vmp.Map(cc).VMPData;
            else
                buff=test_vmp.Map(cc).VMPData.*(-1);
            end
            
            temp_data_test(test_vmp.XStart:test_vmp.XEnd-1, ...
                test_vmp.YStart:test_vmp.YEnd-1, ...
                test_vmp.ZStart:test_vmp.ZEnd-1,cc) = buff;
            
            temp_data_test(:,:,:,cc)=temp_data_test(:,:,:,cc).*temp_mask_vox_train;
        end
        
        % 1. Compute Winner Map
        [demeaned_VMPMaps, voxels_indices_dem, saveSuffix_dem] = normalization_fnc(temp_data_test,deMeanOpt);
        
        [idxMax_dem] = winner_map_fnc(demeaned_VMPMaps, voxels_indices_dem);
        
        % 2. Compute tuning curves inside test set itself
        [tuningCurves_dem, NrOfVox_dem] = tuning_curve_fnc(demeaned_VMPMaps,idxMax_dem);
        
        % Saving test-set struct results as for training set
        TestSet(left_run).(field).name=['run_' num2str(left_run)];
        TestSet(left_run).(field).data=demeaned_VMPMaps;
        TestSet(left_run).(field).label=idxMax_dem;
        TestSet(left_run).(field).condOrder=condNames;
        TestSet(left_run).(field).demeanOpt=saveSuffix_dem;
        TestSet(left_run).(field).count=NrOfVox_dem;
        
        TuningCurves(left_run).(field)=tuningCurves_dem;
        
        %% 3. Confusion matrix: TRAINING vs TEST set
        [cmatrix, nVOX_act_pred_match, matchVOX_idx, matchVOX_act_pred, TPR, PPV] = confusion_matrix_fnc(temp_labels_train,idxMax_dem);
        [tuningCurves_test, NrOfVox_test] = tuning_curve_fnc(demeaned_VMPMaps,temp_labels_train);

        Voxels_TRAIN_TEST(iterFold).(field).cmatrix=cmatrix;
        Voxels_TRAIN_TEST(iterFold).(field).TPR=TPR;
        Voxels_TRAIN_TEST(iterFold).(field).PPV=PPV;
        Voxels_TRAIN_TEST(iterFold).(field).matchVOX_idx=matchVOX_idx;
        Voxels_TRAIN_TEST(iterFold).(field).matchVOX_act_pred=matchVOX_act_pred;
        Voxels_TRAIN_TEST(iterFold).(field).nVOX_act_pred_match=nVOX_act_pred_match;
        Voxels_TRAIN_TEST(iterFold).(field).tuning=tuningCurves_test;
        Voxels_TRAIN_TEST(iterFold).(field).NrOfVox_tuning=NrOfVox_test;
    end
end
save(fullfile(PathIn, ['TestSet_' proc, '_TC_' saveSuffix_dem voiName]),'TuningCurves');
save(fullfile(PathIn, ['TestSet_' proc '_RES_' saveSuffix_dem voiName]), 'TestSet', '-v7.3');   

clear cmatrix nVOX_act_pred_match matchVOX_idx_lab TPR PPV tuningC NrOfVox iterContr iterFold
clear temp* left_run labels_test labels_train train_runs
%% Voxels selection across cv-folds
% Voxel selection 1: voxels should show same label between training and test set
% (voxels belonging to the diag of cmatrix)
matchVOX_cv=struct;

for iterContr=1:2
    
    temp_vox=[];
    
    if iterContr==1
        field='BOLD';
    else
        field='VASO';
    end
    
    for iterFold=1:nfold
        
        vox=Voxels_TRAIN_TEST(iterFold).(field).matchVOX_idx;
        lab=Voxels_TRAIN_TEST(iterFold).(field).matchVOX_act_pred;
        temp_vox=[temp_vox; [vox(find(vox(:,2)),1), lab(find(vox(:,2)),1)]];
        
    end
    
    matchVOX_cv.(field)=temp_vox;
    
end
%% Voxel selection 2: voxels shouldn't have different labels across folds.
% From matchVOX_cv find unique cv voxels and count how many times they show a label
Voxels_CV=struct;

for iterContr=1:2
    
    if iterContr==1
        field='BOLD';
    else
        field='VASO';
    end
    
    n_match=matchVOX_cv.(field)(:,1);
    lab_vox=matchVOX_cv.(field)(:,2);
    
    unique_vox=unique(n_match);             % unique voxels
    cvVOX=zeros(size(unique_vox,1),5);      % result matrix
    
    for ii=1:size(unique_vox,1)
        
        idx=find(n_match==unique_vox(ii));
        cvVOX(ii,1)=unique_vox(ii);         % voxel index
        labels=lab_vox(idx);
        for iterFold=1:size(labels,1)
            cvVOX(ii,labels(iterFold)+1)=cvVOX(ii,labels(iterFold)+1)+1;
        end
        
    end
    
    % Consistency
    a=[sum(cvVOX(:,2)==4), sum(cvVOX(:,3)==4), sum(cvVOX(:,4)==4), sum(cvVOX(:,5)==4)];
    b=[sum(cvVOX(:,2)==3), sum(cvVOX(:,3)==3), sum(cvVOX(:,4)==3), sum(cvVOX(:,5)==3)];
    c=[sum(cvVOX(:,2)==2), sum(cvVOX(:,3)==2), sum(cvVOX(:,4)==2), sum(cvVOX(:,5)==2)];
    d=[sum(cvVOX(:,2)==1), sum(cvVOX(:,3)==1), sum(cvVOX(:,4)==1), sum(cvVOX(:,5)==1)];
    
    Voxels_CV.(field).cvVOX=cvVOX;
    Voxels_CV.(field).stat_cvVOX=[a;b;c;d];
    
end

% Adding some info to the selected voxels
% Here the step2 selection happen
for iterContr=1:2
    
    if iterContr==1
        field='BOLD';
    else
        field='VASO';
    end
    
    datavox=Voxels_CV.(field).cvVOX;        % labels stored as binary info
    x=(datavox(:,2:end)>0);                 % binarize the labels
    nlab=sum(x,2);                          % num of labels for each vox
    
    lab=datavox(:,2:end);                   % label is the col index
    rows=nlab==1;
    temp=lab(rows,:);
    [rId, cId, val] = find( temp' ) ;
    
    Voxels=[datavox(rows,1), rId, val];     % label, occurrence
    Voxels_CV.(field).Voxels=Voxels;
    Voxels_CV.(field).nVoxels=size(Voxels,1);
    Voxels_CV.(field).n_cvVox=sum(x);
end

save([PathIn, '/Voxels_CV_results_' proc 'deMeanOpt_' num2str(deMeanOpt)],...
    'Voxels_TRAIN_TEST', 'Voxels_CV');

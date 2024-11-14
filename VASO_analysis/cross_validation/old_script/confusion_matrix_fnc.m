function [cmatrix, nVOX_act_pred_match, matchVOX_idx, matchVOX_act_pred, TPR, PPV] = confusion_matrix_fnc(labels_pred,labels_test)
% This function compare two matrix of labels(winner): 
% predicated(train set) vs actual(test set).
% Steps: 1. Find common voxels (independent voxels selection betw 2 groups)
%        2. Find voxels with the same label
%        3. Compute confusion matrix
%
% === Execution ===        

ncond=4;

% 0. Starting point: nvox for class
nVOX_act_pred_match=zeros(4, ncond);
for itclass=1:ncond
    nVOX_act_pred_match(1,itclass)=sum(sum(sum(labels_test==itclass)));
    nVOX_act_pred_match(2,itclass)=sum(sum(sum(labels_pred==itclass)));
    
end

% 1. Find common voxels, 
% Voxels found in both cases but they can have different labels

idx_pred=(labels_pred(:)>0);
idx_test=(labels_test(:)>0);

idx_match=find(idx_pred.*idx_test); 
ntot_match=size(idx_match,1);

v_pred=labels_pred(idx_match);
v_test=labels_test(idx_match);

% 2. Compute confusion matrix
cmatrix=zeros(ncond);           % predicted (col) & test (row)

% 3. Find voxels show same label (consistent)
lab_match=zeros(ntot_match,1);  % 1rst col=1 if labels match

for it=1:ntot_match
    
    cmatrix(v_test(it), v_pred(it))=cmatrix(v_test(it), v_pred(it))+1;
    
    if v_test(it)==v_pred(it)   % perfect match
        lab_match(it,1)=1;
        
    end
    
end

matchVOX_idx=[idx_match, lab_match];
matchVOX_act_pred=[v_test,  v_pred];

% Relative performance indices (for each class)

n_test=sum(cmatrix,2)';  % number of "actual" positive (test)
n_pred=sum(cmatrix);     % number of "predicted" positive (training)

% Change due to the presence of zeros
n_test(n_test==0)=1;
n_pred(n_pred==0)=1;

n_match=diag(cmatrix)';  % number of true positive for each class

TPR=n_match./n_test;     % sensitivity
PPV=n_match./n_pred;     % precision

nVOX_act_pred_match(3,:)=n_test;
nVOX_act_pred_match(4,:)=n_pred;


end


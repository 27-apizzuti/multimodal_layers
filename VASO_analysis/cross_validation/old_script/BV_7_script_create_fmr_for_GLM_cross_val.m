% Create .fmr document for cross validation analysis
% Required for GLM in BV
% Works for both single run and leave one run out.
%%
clear all
clc

% P02, P03, P04 (standard and magn_only_noNOISE)
subj={'04'};
cond={'magn_only_noNOISE'};

for iterSbj=1:length(subj)
    for iterCond=1:length(cond)
        % set path with nii files
        PathIn = ['D:\Pilot_Exp_VASO\pilotAOM\sub-' num2str(subj{iterSbj}) ...
            '\derivatives\func\AOM\vaso_analysis\' cond{iterCond} '\cross_validation\'];
        d=dir([PathIn 'run*.*']);
        nfold=size(d,1);
        for iterFile=1:nfold
            PathRun=[PathIn, d(iterFile).name, '\boco'];
            
            if exist(PathIn, 'dir')
                
                PathOut =[PathIn, d(iterFile).name, '\GLM'];
                
                if ~exist(PathOut, 'dir')
                    mkdir(PathOut)
                end
                
                % set fmr names
                components = {'BOLD_interp', 'VASO_interp_LN'};
                
                % define number of runs
                nr_fmrs = length(components);
                
                % deduce motion corrected *.nii names
                for i=1:nr_fmrs
                    nii_names{i}=fullfile(PathRun,[components{i} '.nii']);
                end
                
                % convert nii to fmr
                for i=1:nr_fmrs;
                    % create temporary nii
                    tempnii=xff(nii_names{i});
                    % Convert .nii  to .fmr
                    tempfmr=tempnii.Dyn3DToFMR;
                    data = tempfmr.Slice.STCData;
                    data = flip(data,2);
                    % This is necessary to flip the y axis
                    % save
                    
                    if (i == 2)
                        data = flip(data,2)*30000;
                        %     data = data*30000;
                    else
                        data = flip(data,2);
                    end
                    
                    tempfmr.Slice.STCData = data;
                    tempfmr.SaveAs(fullfile(PathOut,[components{i} '_NeuroElf.fmr']))
                end
            end
        end
    end
end

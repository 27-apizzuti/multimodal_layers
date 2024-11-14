%% Script to plot cross-validation results
clear all;
clc;
close all;

subj='sub-03';
proc='standard';
filename= ['TrainingSet_standard_TC_dMeanAcross_' subj '_clust500_fdr0001_AND_sphere'];

flag=split(filename, '_');

PATH_IN = ['D:\Pilot_Exp_VASO\pilotAOM\' subj '\derivatives\func\AOM\vaso_analysis\' proc ...
    '\cross_validation\output\WinnerMaps\'];

load(fullfile(PATH_IN, filename));


%% Plot 1: Tuning curves for each cross-validation fold 

figH=figure('units','normalized','outerposition',[0 0 1 1]);
set(gcf,'color','w')
cond = {'horizontal', '45 | 225º','vertical', '135 | 315º'};
ncond=4;
nfold=size(TuningCurves,2);
count=0;
    
for jj=1:size(TuningCurves,2)
    
    % set max-min y values for plots by adding the SE to the mean values
%     matB = sum(TuningCurves(jj).bold_tuningC,3); % Bold
%     matV = sum(TuningCurves(jj).vaso_tuningC,3); % Vaso
%     maxVal = ceil(max(matB(:)));
%     minVal = floor(min(matV(:)));
    maxVal = 3;    
    minVal = -2;
    lineSpec = '-';
    
    
    for ii=1:2
        % select contrast type
        if ii==1 % BOLD
            
            tuningC = TuningCurves(jj).BOLD;
            lineCol = [0.1 0.1 0.75];
            
        else % VASO
            
            tuningC = TuningCurves(jj).VASO;
            lineCol = [0.75 0.1 0.1];
            
        end
        
        for nn=1:ncond
            sp = subplot(nfold,4,count+nn);
            if ii==1 
                aH = area([nn-0.5 nn+0.5], repelem(maxVal,2)); % mark preferred axis in gray
                aH.FaceColor = [0.9 0.9 0.9];
                aH.EdgeColor = aH.FaceColor;
                hold all,
                aH2 = area([nn-0.5 nn+0.5], repelem(minVal,2));
                aH2.FaceColor = [0.9 0.9 0.9];
                aH2.EdgeColor = aH2.FaceColor;
            end
            hold all,
            errorbar(tuningC(nn,:,1),tuningC(nn,:,2),...
                     'Color', lineCol, 'LineWidth', 1.5, 'LineStyle',lineSpec)
            
            % complete plot 
            xlim([0,ncond+1])
            ylim([minVal aH.YData(1)]);            
            
            if nn==1, ylabel('t-values','FontSize',9),end
            
            sp.XTick = 1:ncond;
            if count+nn < 5
                title([cond{nn} ' preference'])
            elseif count+nn > 12
                sp.XTickLabel = {'   0˚\newline 180˚ ' '  45˚\newline 225˚' '  90˚\newline 270˚' '135˚\newline315˚'};
                sp.FontSize = 9;
                sp.Title.FontWeight = 'normal';
            end
        end

    end

    count=count+4;
end
% add legend
% lH = legend([sp.Children(4),sp.Children(3), sp.Children(2),sp.Children(1)],{'BOLD Standard','VASO Standard','BOLD Nordic','VASO Nordic'});
% lH.Position = [0.9149 0.5130 0.0715 0.0491];
% lH.EdgeColor = [1 1 1];
% lH.FontSize = 12;
suptitle( [ 'Axis of Motion Tuning Curves (' flag{1} ')'])
saveas(gca, fullfile(PATH_IN, [flag{1} '_Cross_Validation_Tuning Curves' ]), 'jpeg');
saveas(gca, fullfile(PATH_IN, [flag{1} '_Cross_Validation_Tuning Curves' ]), 'fig');



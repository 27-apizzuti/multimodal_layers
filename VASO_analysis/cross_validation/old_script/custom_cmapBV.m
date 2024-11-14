pathLUT='D:\Pilot_Exp_VASO\AOM-project\brainvoyager_colormaps\';
col={'blue', 'green', 'red', 'yellow', 'purple'};

for it=1:size(col,2)
    filename=['cbrew_seq_singlehue_' col{1,it} '_pos_inv.olt'];
    
    data= importdata(fullfile(pathLUT, filename));
    
    maxCol= data.data(8,:);
    minCol= data.data(8,:);
    
    newCol=[linspace(maxCol(1),minCol(1),10)', linspace(maxCol(2),minCol(2),10)',...
        linspace(maxCol(3),minCol(3),10)'];
    
    data.data(1:10,:)=newCol;
    
    fileID = fopen(fullfile(pathLUT, ['ap_' filename]),'w');
    for it1=1:20
        nbytes = fprintf(fileID,': %0.f %0.f %0.f\n', data.data(it1,:));
        
    end
    
    fclose(fileID)
end

% [data.textdata{:}]'

clear all
clc

subjects = {'demo_whole_brain'};
hemisphere = 'LH';


for subnum = 1:length(subjects) 
    
    subject_id = subjects{subnum};
    
    dirpois = ['D:\AHEAD_v2\derivatives\', subject_id, '\LH-CBA\pois\'];
    dirdata = ['D:\AHEAD_v2\derivatives\', subject_id, '\LH-CBA\'];

    poi = xff([dirpois,'visfAtlasPOIs_', hemisphere, '_toAVG.poi']);
    ssm = xff([dirdata, 'seg-01_', hemisphere, '_rim_bvbabel_RECO_D200k_HIRES_SPH_GROUPALIGNED_INV.ssm']);        
    
    poi2 = poi.CopyObject;
    
    for i=1:poi.NrOfPOIs
        data = zeros(poi.NrOfMeshVertices,1);
        data(poi.POI(i).Vertices)  = 1;
        newdata = data(ssm.SourceOfTarget);
        indexPOI = find(newdata);
        
        poi2.POI(i).NrOfVertices = length(indexPOI);
        poi2.POI(i).Vertices = indexPOI;
    
    end
    
    poi2.SaveAs([dirpois, 'sub-01_visfAtlasPOIs_', hemisphere, '.poi']);

end 

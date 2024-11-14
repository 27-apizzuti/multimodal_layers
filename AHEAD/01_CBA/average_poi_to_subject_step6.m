clear all
clc

subjects = {'122017'};
hemisphere = 'RH';


for subnum = 1:length(subjects) 
    
    subject_id = subjects{subnum};
    
    dirpois = ['D:\AHEAD_v2\derivatives\', subject_id, '\', hemisphere, '\pois\'];
    dirdata = ['D:\AHEAD_v2\derivatives\', subject_id, '\', hemisphere, '\'];

    poi = xff([dirpois,'visfAtlasPOIs_', hemisphere, '_toAVG.poi']);
    
    ssm = xff([dirdata, subject_id, '_', hemisphere, '_D200k_smooth-120_HIRES_SPH_GROUPALIGNED_INV.ssm']);        
    
    poi2 = poi.CopyObject;
    
    for i=1:poi.NrOfPOIs
        data = zeros(poi.NrOfMeshVertices,1);
        data(poi.POI(i).Vertices)  = 1;
        newdata = data(ssm.SourceOfTarget);
        indexPOI = find(newdata);
        
        poi2.POI(i).NrOfVertices = length(indexPOI);
        poi2.POI(i).Vertices = indexPOI;
    
    end
    
    poi2.SaveAs([dirpois, subject_id, '_visfAtlasPOIs_', hemisphere, '.poi']);

end 

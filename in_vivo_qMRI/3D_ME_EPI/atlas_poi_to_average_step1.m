clear
clc

subject = 'demo_whole_brain';
hemisphere = 'LH';

dirpois = ['D:\AHEAD_v2\derivatives\', subject, '\LH-CBA\'];
dirdata = ['D:\AHEAD_v2\derivatives\', subject, '\LH-CBA\'];

poi = xff([dirpois, 'visfAtlas_' hemisphere '_hires.poi']);
ssm = xff([dirdata, 'BVaverage_' hemisphere '_HIRES_CURVATURE_GROUPALIGNED.ssm']);

poi2 = poi.CopyObject;

for i=1:poi.NrOfPOIs
    data = zeros(poi.NrOfMeshVertices,1);
    data(poi.POI(i).Vertices) = 1;
    newdata = data(ssm.SourceOfTarget);
    indexPOI = find(newdata);
    
    poi2.POI(i).NrOfVertices = length(indexPOI);
    poi2.POI(i).Vertices = indexPOI;

end

if (exist([dirdata, '\pois\'], 'dir') == 0); mkdir([dirdata, '\pois\']); end
poi2.SaveAs([dirdata, '\pois\', 'visfAtlasPOIs_', hemisphere, '_toAVG.poi']);
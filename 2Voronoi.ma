#include(constants.ma)

[Top]
components : voronoiExpansion

[voronoiExpansion]
type : cell
dim : (20,20)
delay : transport
defaultDelayTime  : 0
border : nowrapped
neighbors : voronoiExpansion(-1,-1) voronoiExpansion(-1,0) voronoiExpansion(-1,1)
neighbors : voronoiExpansion(0,-1)  voronoiExpansion(0,0)  voronoiExpansion(0,1)
neighbors : voronoiExpansion(1,-1)  voronoiExpansion(1,0)  voronoiExpansion(1,1)
initialvalue : 0
initialCellsValue : sites.val
localtransition : voronoiSite

[voronoiSite]

% Expand center cell value in a 3x3 square neighbourhood
rule : {(1,0)} #Macro(expansionWaveDelay) { (0,0)=0 and (1,0)!=0 and (1,0)!=? }
rule : {(1,-1)} #Macro(expansionWaveDelay) { (0,0)=0 and (1,-1)!=0  and  (1,-1)!=? }
rule : {(0,-1)} #Macro(expansionWaveDelay) { (0,0)=0 and (0,-1)!=0  and  (0,-1)!=? }
rule : {(-1,-1)} #Macro(expansionWaveDelay) { (0,0)=0 and (-1,-1)!=0  and  (-1,-1)!=? }
rule : {(-1,0)} #Macro(expansionWaveDelay) { (0,0)=0 and (-1,0)!=0  and  (-1,0)!=? }
rule : {(-1,1)} #Macro(expansionWaveDelay) { (0,0)=0 and (-1,1)!=0  and  (-1,1)!=? }
rule : {(0,1)} #Macro(expansionWaveDelay) { (0,0)=0 and (0,1)!=0  and  (0,1)!=? }
rule : {(1,1)} #Macro(expansionWaveDelay) { (0,0)=0 and (1,1)!=0  and  (1,1)!=? }

% Default rule
rule : {(0,0)} 0 { t }

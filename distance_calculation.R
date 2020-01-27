data = read.csv('Cleaned_data_Final.csv')
data$distance = NA
library(geosphere)
library(plyr)
for (i in 1:72145){
  source_loc = c(data$S_Lo[i],data$S_La[i])
  destination_loc = c(data$D_Lo[i],data$D_La[i])
  xy = rbind(source_loc,destination_loc)
  a = distm(xy)
  a = data.frame(a)
  data$distance[i]=a$X2[1]
}

write.csv(data,file="Cleaed.csv",quote=F,row.names = F)

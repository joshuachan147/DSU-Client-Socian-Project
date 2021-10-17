library(readr)
library(tidyverse)
library(hunspell)
data <- read_csv("911_calls_for_service.csv")
#Separating date and time
testData <- data %>%
  separate(callDateTime, into = c("callDate", "callTime"), sep = " ")
testData <- testData %>%
  separate(callTime, into = c("Hour", "Min", "Sec"), sep = ":")
testData$Min <- as.numeric(testData$Min) / 60
testData$Hour <- as.numeric(testData$Hour)
timeOfDay <- testData$Hour + testData$Min
testData <- testData %>%
  add_column(timeOfDay = timeOfDay)
testData <- testData %>%
  select(-c(Hour, Min, Sec))
testData <- testData %>%
  select(-c(X1))
testData <- testData %>%
  separate(location, into = c("Lat", "Long"), sep = ",") %>%
  mutate(Lat = str_remove(Lat, "\\("), Long = str_remove(Long, "\\)"))
testData$Lat <- as.numeric(testData$Lat)
testData$Long <- as.numeric(testData$Long)

#Remove rows missing priority data
naPriority <- is.na(testData$priority)
testData <- testData[-naPriority, ]

#Imputing missing location by district
avgLocation <- testData %>%
  group_by(district) %>%
  summarize(
    Lat = mean(Lat, na.rm = TRUE),
    Long = mean(Long, na.rm = TRUE)
  )

naIdx <- which(is.na(testData$Lat))
imputeLat <- numeric()
imputeLong <- numeric()
for (i in 1:length(naIdx)){
  currDis <- testData$district[naIdx[i]]
  imputeLat[i] <- avgLocation$Lat[which(avgLocation$district == currDis)]
  imputeLong[i] <- avgLocation$Long[which(avgLocation$district == currDis)]
}

testing <- testData

testing$Lat[naIdx] <- imputeLat
testing$Long[naIdx] <- imputeLong
testing$description <- toupper(testing$description)


testing$description <- as.character(testing$description) 

testing <- testing %>%
  mutate(description = str_remove(description, "[*&#?/:\\ | 0-8 | [:punct:]]"))

cleantext = function(x){
  
  sapply(1:length(x),function(y){
    bad = hunspell(x[y])[[1]]
    good = unlist(lapply(hunspell_suggest(bad),`[[`,1))
    
    if (length(bad)){
      for (i in 1:length(bad)){
        x[y] <<- gsub(bad[i],good[i],x[y])
      }}})
  x
}

#removing unwanted characters / words

testing1 <- testing[-(which(str_detect(testing$description, "[\\/`.+ | 0-9]"))),]

#removing incorrect spelling

bad <- hunspell(testing1$description)
correctSpellingIdx <- which(unlist(lapply(bad, is_empty)))
testing1 <- testing1[correctSpellingIdx, ]

testing1$description <- cleanText(testing1$description)


write_csv(testing1, "processed.csv")












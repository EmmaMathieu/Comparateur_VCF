data <- read.table("../../Desktop/le.txt", header = TRUE, sep =";")

x <- list(
  P15 = data$Position[data$Passage == "P15"],
  P30 = data$Position[data$Passage == "P30"],
  P50 = data$Position[data$Passage == "P50"],
  P65 = data$Position[data$Passage == "P65"]
)

library(ggvenn)
ggvenn(x, fill_color = c("skyblue2", "gold2", "brown3", "green4"))

data <- read.table("../../Desktop/Variants_0.9.txt", header = TRUE, sep =";")
dataP50 <- subset(data, Passage == "P50")

hist(dataP50$Position, freq = dataP50$Frequence, xlab = "Position", ylab = "Frequence", main = "Courbe de Frequence en fonction de la Position")

sorted_dataP50 <- dataP50[order(dataP50$Position), ]
plot(sorted_dataP50$Position, sorted_dataP50$Frequence, type = "l", xlab = "Position", ylab = "Frequence", main = "Courbe de Frequence en fonction de la Position")
barplot(sorted_dataP50$Frequence, names.arg = sorted_dataP50$Position, xlab = "Position", ylab = "Frequence", main = "Barres de Frequence en fonction de la Position")

library(ggplot2)
library(gridExtra)
library(ggvenn)

data <- read.table("../Desktop/le.txt", header = TRUE, sep =";")
geneD <- read.table("../Desktop/gene.bed", header = TRUE, sep = "\t")

x <- list(
  P15 = data$Position[data$Passage == "P15"],
  P30 = data$Position[data$Passage == "P30"],
  P50 = data$Position[data$Passage == "P50"],
  P65 = data$Position[data$Passage == "P65"]
)


ggvenn(x, fill_color = c("skyblue2", "gold2", "brown3", "green4"))


dataP15 <- subset(data, Passage == "P15")
dataP30 <- subset(data, Passage == "P30")
dataP50 <- subset(data, Passage == "P50")
dataP65 <- subset(data, Passage == "P65")




# Création du graphique
plot1 <- ggplot() +
  geom_bar(stat = "identity", aes(x = dataP15$Position, y = dataP15$Frequence), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P15") +
  scale_x_continuous(limits = c(0, 300000)) + scale_y_continuous(limits = c(0,1)) +
  theme_minimal()

plot2 <- ggplot() +
  geom_bar(stat = "identity", aes(x = dataP30$Position, y = dataP30$Frequence), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P30") +
  scale_x_continuous(limits = c(0, 300000)) + scale_y_continuous(limits = c(0,1)) +
  theme_minimal()

plot3 <- ggplot() +
  geom_bar(stat = "identity", aes(x = dataP50$Position, y = dataP50$Frequence), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P50") +
  scale_x_continuous(limits = c(0, 300000)) + scale_y_continuous(limits = c(0,1)) +
  theme_minimal()

plot4 <- ggplot() +
  geom_bar(stat = "identity", aes(x = dataP65$Position, y = dataP65$Frequence), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P65") +
  scale_x_continuous(limits = c(0, 300000)) + scale_y_continuous(limits = c(0,1)) +
  theme_minimal()

grid.arrange(plot1, plot2, plot3, plot4, nrow = 2, ncol = 2)
grid.arrange(plot1)


plot1 <- ggplot() +
  geom_bar(stat = "identity", aes(x = dataP15$Position, y = dataP15$Taille), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P15") +
  scale_x_continuous(limits = c(0, 300000)) + 
  theme_minimal()

plot2 <- ggplot() +
  geom_bar(stat = "identity", aes(x = dataP30$Position, y = dataP30$Taille), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P30") +
  scale_x_continuous(limits = c(0, 300000)) + 
  theme_minimal()

plot3 <- ggplot() +
  geom_bar(stat = "identity", aes(x = dataP50$Position, y = dataP50$Taille), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P50") +
  scale_x_continuous(limits = c(0, 300000)) + 
  theme_minimal()

plot4 <- ggplot() +
  geom_bar(stat = "identity", aes(x = dataP65$Position, y = dataP65$Taille), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P65") +
  scale_x_continuous(limits = c(0, 300000)) +
  theme_minimal()

grid.arrange(plot1, plot2, plot3, plot4, nrow = 2, ncol = 2)


temp_dataP15 <- subset(dataP15, abs(Taille) < 100)
temp_dataP30 <- subset(dataP30, abs(Taille) < 100)
temp_dataP50 <- subset(dataP50, abs(Taille) < 100)
temp_dataP65 <- subset(dataP65, abs(Taille) < 100)

plot1 <- ggplot() +
  geom_bar(stat = "identity", aes(x = temp_dataP15$Position, y = temp_dataP15$Taille), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P15") +
  scale_x_continuous(limits = c(0, 300000)) + 
  theme_minimal()

plot2 <- ggplot() +
  geom_bar(stat = "identity", aes(x = temp_dataP30$Position, y = temp_dataP30$Taille), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P30") +
  scale_x_continuous(limits = c(0, 300000)) + 
  theme_minimal()

plot3 <- ggplot() +
  geom_bar(stat = "identity", aes(x = temp_dataP50$Position, y = temp_dataP50$Taille), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P50") +
  scale_x_continuous(limits = c(0, 300000)) + 
  theme_minimal()

plot4 <- ggplot() +
  geom_bar(stat = "identity", aes(x = temp_dataP65$Position, y = temp_dataP65$Taille), fill = "blue", alpha = 0.7, width = 2500) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P65") +
  scale_x_continuous(limits = c(0, 300000)) +
  theme_minimal()

grid.arrange(plot1, plot2, plot3, plot4, nrow = 2, ncol = 2)

xmin <- 250000
xmax <- 261000
zones = data.frame(start = data$debG, end = data$FinG)

xmin <- 95000
xmax <- 105000

zones = data.frame(start = 99382, end = 100830)

xmin = 45000
xmax <- 50000

zones = data.frame(start = c(45570,47474,48534), end = c(48457,48457,49938))


temp_dataP15 <- subset(dataP15, Position > xmin & Position < xmax)
temp_dataP30 <- subset(dataP30, Position > xmin & Position < xmax)
temp_dataP50 <- subset(dataP50, Position > xmin & Position < xmax)
temp_dataP65 <- subset(dataP65, Position > xmin & Position < xmax)


plot1 <- ggplot() +
  geom_bar(stat = "identity", aes(x = temp_dataP15$Position, y = temp_dataP15$Taille), fill = "blue", alpha = 0.7, width = 100) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P15") +
  scale_x_continuous(limits = c(xmin, xmax)) + 
  theme_minimal()

plot2 <- ggplot() +
  geom_bar(stat = "identity", aes(x = temp_dataP30$Position, y = temp_dataP30$Taille), fill = "blue", alpha = 0.7, width = 100) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P30") +
  scale_x_continuous(limits = c(xmin, xmax)) + 
  theme_minimal()

plot3 <- ggplot() +
  geom_bar(stat = "identity", aes(x = temp_dataP50$Position, y = temp_dataP50$Taille), fill = "blue", alpha = 0.7, width = 100) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P50") +
  scale_x_continuous(limits = c(xmin, xmax)) + 
  theme_minimal()

plot4 <- ggplot() +
  geom_bar(stat = "identity", aes(x = temp_dataP65$Position, y = temp_dataP65$Taille), fill = "blue", alpha = 0.7, width = 100) +
  geom_rect(data = zones, aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf), fill = "red", alpha = 0.3) +
  labs(x = "Position des variants", y = "Fréquence", title = "P65") +
  scale_x_continuous(limits = c(xmin, xmax)) + scale_y_discrete(limits=c(-100,15)) +
  theme_minimal()

grid.arrange(plot1, plot2, plot3, plot4, nrow = 2, ncol = 2)


library(ggplot2)

# Figure 3.7

data <- data.frame(Solution =c(1.701190314203404, 1.9460615070150866), Subsystem = c("Glucose feed only (Control)", "All bounds"))

ggplot(data, aes(x=Subsystem,y=Solution,fill=Subsystem))+
  geom_bar(stat = "identity") +
  # scale_fill_gradientn(colors = rev(pal))+
  theme_minimal() +
  ggtitle("All kinetic bounds vs No kinetic bounds") +
  theme(title = element_text(size=13, face="bold", colour = "black"), axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=12, angle=0, vjust=.8, hjust=0.8))


# Figure 3.8

data <- data.frame(Solution =c(1.701190314203404, 1.7011903142043718, 1.7063440378337558, 1.7011757239557674, 1.7011903142449032, 1.701189280562857, 1.701190314203404, 1.701190314203404, 1.946063071698797, 1.7011903142034244, 1.7302265768943261, 1.7274429636888897, 1.7011903142034117), Subsystem = c("Glucose feed only (Control)", "Glucose metabolism", "PPP", "TCA cycle", "OXPHOS", "Exchange reactions", "glucose uptake", "Pi uptake", "Additional reactions for nucleotides and redox cofactor", "ED pathway", "Anapletoric reactions", "Glyoxylate shunt", "Acetate metabolism"))
# ggplot(data, aes(x=Subsystem, y=solution, fill = solution)) + geom_bar(stat = "identity") + scale_fill_continuous(latin_palette(name = 'aventura', type = 'discrete'))
# ggplot(data, aes(x=Subsystem, y=solution, fill = solution)) + geom_bar(stat = "identity") + scale_fill_continuous(low="blue", high="red")

ggplot(data, aes(x=Subsystem,y=Solution,fill=Subsystem))+
  geom_bar(stat = "identity") +
  # scale_fill_gradientn(colors = rev(pal))+
  theme_minimal() +
  ggtitle("Kinetic bounds by subsystem (only one subsystem at a time)") +
  theme(title = element_text(size=13, face="bold", colour = "black"), axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=7, angle=30, vjust=.8, hjust=0.8))



# Figure 3.9

Reaction <- c(rep("ATPM" , 3) , rep("PPCK" , 3) , rep("MALS" , 3))
Subsystem <- rep(c("Removed reaction bounds" , "Added reaction bounds", "Only glucose feed bounds"))
fba_sol <- c(1.7012058080984525, 1.946063071698797, 1.701190314203404, 1.7011903142131537, 1.7302265768943261, 1.701190314203404, 1.701190314320987, 1.727442963688889, 1.701190314203404)

data <- data.frame(Reaction,Subsystem,fba_sol)

ggplot(data, aes(fill=Subsystem, y=fba_sol, x=Reaction)) + 
  geom_bar(position="dodge", stat="identity") + 
  ggtitle("Reactions whose kinetic bounds loosen the constraint-based model") +
  xlab("Reaction") + ylab("FBA solution") +
  theme_minimal() +
  theme(title = element_text(size=13, face="bold", colour = "black"), axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=10, angle=0, vjust=.8, hjust=0.8))

# Figure 3.10

library(ggplot2)
library(peRReo)

pal <- latin_palette('rosalia', 6, 'discrete')

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2394, 106, 0, 0, 13, 74))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "Glcuose feed (Control)
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2394, 106, 0, 0, 12, 75))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "Glucose metabolism
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2424, 76, 0, 0, 11, 76))

data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "PPP
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2399, 103, 0, 0, 11, 74))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "TCA cycle
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2394, 106, 0, 0, 12, 75))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "OXPHOS
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2396, 108, 0, 0, 11, 72))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "Exchange reactions
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2394, 106, 0, 0, 13, 74))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "Glucose uptake
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2394, 106, 0, 0, 13, 74))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "Pi uptake
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(1662, 106, 388, 225, 133, 73))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "Additional reactions for nucleotides and redox cofactor
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2394, 106, 0, 0, 11, 76))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "ED pathway
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2408, 92, 0, 0, 11, 76))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "Anapletoric reactions
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2362, 138, 0, 0, 12, 75))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "Glyoxylate shunt
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))

data <- data.frame( x = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"),            # Create example data
                    y = c(2394, 109, 0, 0, 12, 72))


data1 <- data                                                 # Replicate original data
data1$x <- factor(data1$x,                                    # Change ordering manually
                  levels = c("0-1", "1-10", "10-50", "50-100", "100-1000","> 1000"))

ggplot(data1, aes(x , y, fill=x)) +                                    # Manually ordered barchart
  geom_bar(stat = "identity") +
  labs(title = "Acetate metabolism
",face="bold", x = "Difference interval value",
       y = "Frequency") +
  # scale_fill_gradientn(colors = rev(pal))+
  scale_fill_manual(values=pal, name = "Difference interval value") +
  theme_minimal() +
  theme(axis.title.x = element_text(size=12, face="bold", colour = "black"), axis.title.y = element_text(size=12, face="bold", colour = "black"),
        axis.text.x=element_text(color = "black", size=9, angle=30, vjust=.8, hjust=0.8))



